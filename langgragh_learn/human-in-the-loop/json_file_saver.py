import os
import json
import base64
import threading

from typing import Any, Sequence
from langgraph.checkpoint.memory import InMemorySaver


# ============================================================
# 1. JSON 编码
# ============================================================

def encode_json(obj: Any):

    # bytes 无法直接保存到 JSON
    if isinstance(obj, bytes):
        return {
            "__type__": "bytes",
            "data": base64.b64encode(obj).decode("utf-8")
        }

    # tuple
    if isinstance(obj, tuple):
        return {
            "__type__": "tuple",
            "items": [
                encode_json(item)
                for item in obj
            ]
        }

    # dict
    if isinstance(obj, dict):
        return {
            "__type__": "dict",
            "items": [
                [
                    encode_json(key),
                    encode_json(value)
                ]
                for key, value in obj.items()
            ]
        }

    # list
    if isinstance(obj, list):
        return [
            encode_json(item)
            for item in obj
        ]

    return obj


# ============================================================
# 2. JSON 解码
# ============================================================

def decode_json(obj: Any):

    if isinstance(obj, list):
        return [
            decode_json(item)
            for item in obj
        ]

    if isinstance(obj, dict):

        obj_type = obj.get("__type__")

        # bytes
        if obj_type == "bytes":
            return base64.b64decode(
                obj["data"]
            )

        # tuple
        if obj_type == "tuple":
            return tuple(
                decode_json(item)
                for item in obj["items"]
            )

        # dict
        if obj_type == "dict":
            return {
                decode_json(key): decode_json(value)
                for key, value in obj["items"]
            }

        return {
            key: decode_json(value)
            for key, value in obj.items()
        }

    return obj


# ============================================================
# 3. JSON 文件 Checkpointer
# ============================================================

class JsonFileSaver(InMemorySaver):

    def __init__(self, file_path: str = "checkpoint.json"):

        super().__init__()

        self.file_path = file_path

        # 防止 LangGraph 同时写 checkpoint.json
        self._file_lock = threading.RLock()

        # 启动时加载之前的数据
        self._load()


    # ========================================================
    # 保存
    # ========================================================

    def _save(self):

        with self._file_lock:

            # storage 是多层 defaultdict
            storage_data = {
                thread_id: {
                    namespace: dict(checkpoints)
                    for namespace, checkpoints in namespaces.items()
                }
                for thread_id, namespaces in self.storage.items()
            }

            data = {
                "storage": storage_data,
                "writes": dict(self.writes),
                "blobs": dict(self.blobs)
            }

            json_data = encode_json(data)

            # 直接写 checkpoint.json
            with open(
                self.file_path,
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    json_data,
                    f,
                    ensure_ascii=False,
                    indent=2
                )


    # ========================================================
    # 加载
    # ========================================================

    def _load(self):

        if not os.path.exists(self.file_path):
            return

        if os.path.getsize(self.file_path) == 0:
            return

        with self._file_lock:

            with open(
                self.file_path,
                "r",
                encoding="utf-8"
            ) as f:

                json_data = json.load(f)

            data = decode_json(json_data)


            # 恢复 storage
            for thread_id, namespaces in data.get(
                "storage",
                {}
            ).items():

                for namespace, checkpoints in namespaces.items():

                    self.storage[
                        thread_id
                    ][
                        namespace
                    ].update(
                        checkpoints
                    )


            # 恢复 writes
            self.writes.update(
                data.get(
                    "writes",
                    {}
                )
            )


            # 恢复 blobs
            self.blobs.update(
                data.get(
                    "blobs",
                    {}
                )
            )


    # ========================================================
    # LangGraph 保存 checkpoint
    # ========================================================

    def put(
        self,
        config,
        checkpoint,
        metadata,
        new_versions
    ):

        result = super().put(
            config,
            checkpoint,
            metadata,
            new_versions
        )

        self._save()

        return result


    # ========================================================
    # 保存 pending writes
    # interrupt / resume 会使用
    # ========================================================

    def put_writes(
        self,
        config,
        writes: Sequence[tuple[str, Any]],
        task_id: str,
        task_path: str = ""
    ):

        super().put_writes(
            config,
            writes,
            task_id,
            task_path
        )

        self._save()


    # ========================================================
    # 删除 thread
    # ========================================================

    def delete_thread(
        self,
        thread_id: str
    ):

        super().delete_thread(
            thread_id
        )

        self._save()