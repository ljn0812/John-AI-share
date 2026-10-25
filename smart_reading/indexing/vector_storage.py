import logging
from pathlib import Path
from typing import List
from xml.dom.minidom import Document

from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.vectorstores import Chroma

from config.setting import QaConfig
from indexing.hash_calculate import HashCalculate
logger = logging.getLogger(__name__)

class VectorStorageManager:

    def __init__(self, config: QaConfig, embeddings: DashScopeEmbeddings):
        self._config = config
        self._embeddings = embeddings


    def load_or_build(self, file_hash: str, chunks: List[Document]=None) -> Chroma:

        if not file_hash:
            raise RuntimeError("File hash is empty, cannot load or build vector storage.")

        persist_dir = self._get_persist_dir(file_hash)
        collection_name = self._get_collection_name(file_hash)

        vector_store =  Chroma(
            persist_directory=str(persist_dir),
            collection_name=collection_name,
            embedding_function=self._embeddings,
            collection_metadata={"hnsw:space": "cosine"}
        )

        if self._has_data(vector_store):
            logger.info(f"加载已有向量库: {collection_name}")
            return vector_store

        if not chunks:
            raise RuntimeError("No chunks found, cannot build vector storage.")


        return self._build_vector_store(vector_store, chunks)

    def _build_vector_store(
            self,
            vector_store: Chroma,
            chunks: List[Document]
    ) -> Chroma:
        """构建向量库"""
        if not chunks:
            raise ValueError("文档块列表不能为空")

        try:
            vector_store.add_documents(
                documents=chunks,
                ids=[f"doc-{idx}" for idx in range(1, len(chunks) + 1)]
            )
            logger.info(f"成功添加 {len(chunks)} 个文档块到向量库")
            return vector_store
        except Exception as e:
            logger.error(f"构建向量库失败: {e}")
            raise

    def _get_persist_dir(self, file_hash: str) -> Path:
        # 根据文件路径生成持久化目录
        persist_dir = Path(self._config.chroma_root_dir) / f"pdf_{file_hash}"

        persist_dir.mkdir(parents=True, exist_ok=True)
        return persist_dir

    def _get_collection_name(self, file_hash: str) -> str:
        # 根据文件路径生成集合名称
        return f"{self._config.collection_prefix }_{file_hash}"

    def _has_data(self, vector_store: Chroma) -> bool:
        """ 检查向量库是否已有数据 """
        try:
            return vector_store._collection.count() > 0
        except Exception as e:
            logger.warning(f"检查向量库数据失败: {e}")
            return False