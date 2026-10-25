from typing import Tuple, List
from xml.dom.minidom import Document

from langchain_community.vectorstores import Chroma


def recall_with_scores(query:str,vectorstore: Chroma, k: int=30) -> Tuple[List[Document], List[float]]:


    if not query or not vectorstore:
        return [], []

    try:

        results = vectorstore.similarity_search_with_relevance_scores(query,k)

        docs= []
        scores = []

        for doc, score in results:
            doc.page_content = doc.page_content.strip()
            docs.append(doc)
            scores.append(score)

        return docs, scores
    except Exception as e:
        print(f"Error during recall_with_scores: {e}")
        return [], []

