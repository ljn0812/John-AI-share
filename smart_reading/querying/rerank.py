import re
from dataclasses import dataclass
from typing import List, Tuple, Optional

from langchain_community.chat_models import ChatTongyi
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from config.setting import QaConfig
from querying.query_prompt import RERANK_PROMPT





@dataclass
class RetrievedEvidence:
    """检索到的证据片段（经过重排序后输出的结构化信息）"""
    content: str
    source: str
    page: Optional[int]
    score: float
    vector_score: float
    llm_score: Optional[float] = None


class RerankPipeline:

    def __init__(self, config: QaConfig, llm: ChatTongyi ):
        self.__config = config
        self.__llm = llm
        self.__prompt = ChatPromptTemplate.from_messages([
            ("system", RERANK_PROMPT),
            ("human",
             "问题:{question}\n\n{chunks}\n\n请为以上每个候选片段打分（0-10分），按以下格式输出：\n候选片段 1: X.X\n候选片段 2: X.X\n...\n分数:")
        ])
        self.__batch_chain = self.__prompt | self.__llm | StrOutputParser()


    def rerank(self, query:str, recalled_docs: List[Document],  vec_scores: List[float], final_top_n: int=4) -> Tuple[List[RetrievedEvidence], str]:
        pre_docs = self.__filter(recalled_docs)

        score_map = {doc.page_content: s for doc, s in zip(recalled_docs, vec_scores)}
        final_docs, llm_scores = self.__llm_rerank_batch(query, pre_docs, vec_scores, final_top_n)

        evidence_list = []
        for i, doc in enumerate(final_docs):
            content = doc.page_content
            meta = doc.metadata or {}
            ev = RetrievedEvidence(
                content=content,
                source=meta.get("source", "Unknown"),
                page=meta.get("page"),
                score=llm_scores[i],
                vector_score=score_map.get(content, 0),
                llm_score=llm_scores[i]
            )
            evidence_list.append(ev)
        context_lines = []
        for idx, ev in enumerate(evidence_list, 1):
            page_str = f"第{ev.page + 1}页" if ev.page is not None else "未知页"
            context_lines.append(f"[证据{idx} | 来源：{ev.source} | {page_str}]\n{ev.content}")
        context = "\n\n".join(context_lines)

        return evidence_list, context
    def __filter(self, docs: List[Document], min_len:int=40, max_len:int=2000) -> List[Document]:
        filtered = []
        for doc in docs:
            text = doc.page_content
            if min_len <=len(text)<=max_len:
                filtered.append(doc)
        seen = set()
        kept = []
        for doc in filtered:
            key = doc.page_content
            if key not in seen:
                seen.add(key)
                kept.append(doc)
        return kept

    def __llm_rerank_batch(self, question: str, documents: List[Document], vector_scores: List[float], top_n: int=4) -> Tuple[List[Document],List[float]]:
        if not documents:
            return [], []

        chunk_text = []
        for idx, doc in enumerate(documents, 1):
            content = doc.page_content[:1000] if len(doc.page_content) > 1000 else doc.page_content
            chunk_text.append(f"候选片段 {idx}:\n{content}")
        chunk_text = "\n\n".join(chunk_text)

        try:
            result_text = self.__batch_chain.invoke({
                "question": question,
                "chunks": chunk_text
            })

            scores = self.__parse_batch_scores(result_text, len(documents))
            scores = [max(0.0, min(10.0, score)) for score in scores]

            scored = list(zip(scores, documents))
            scored.sort(key=lambda x: x[0], reverse=True)
            docs = [d for _, d in scored[:top_n]]
            final_scores = [s for s, _ in scored[:top_n]]

            return docs, final_scores

        except Exception as e:
            print(f"LLM rerank failed: {e}")
            return [],[]



    def __parse_batch_scores(self, text: str, expected_count: int) -> List[float]:
        """
        解析批量打分结果

        :param text: LLM 返回的文本
        :param expected_count: 期望的分数数量
        :return: 分数列表
        """
        scores = []

        # 尝试标准格式：候选片段 1: 8.5 或 候选片段1:8.5
        pattern = r'候选片段\s*(\d+)[:：]\s*(\d+(?:\.\d+)?)'
        matches = re.findall(pattern, text)

        if matches:
            # 如果成功匹配，按索引组织
            score_dict = {int(idx): float(score) for idx, score in matches}
            """
            {1: 3.0, 2: 5.0, 3: 0.0, 4: 3.0, 5: 10.0, 6: 3.0, 7: 0.0, 8: 0.0, 9: 0.0, 10: 0.0}
            """
            scores = [score_dict.get(i + 1, 0.0) for i in range(expected_count)]
            # [3.0, 5.0, 0.0, 3.0, 10.0, 3.0, 0.0, 0.0, 0.0, 0.0]
        else:
            # 完全解析失败，返回默认分数
            scores = [0.0] * expected_count

        return scores