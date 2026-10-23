from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.documents import Document

chroma = Chroma(
    persist_directory="./chroma_db",
    collection_name="test-collection1",
    embedding_function=DashScopeEmbeddings(),
    collection_metadata={"hnsw:space":"cosine"}
)


data = [
    Document(page_content="猫坐在垫子上"),
    Document(page_content="一只猫在垫子上休息"),
    Document(page_content="今天天气很好")
]

chroma.add_documents(
    documents=data,
    ids=[f"id-{i}" for i in range(len(data)+1)]
)

user_input = "猫在哪里"

result = chroma.similarity_search_with_relevance_scores(user_input,k=3)

print(type(result))
print(result)
