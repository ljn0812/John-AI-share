from langchain_community.embeddings import DashScopeEmbeddings

llm = DashScopeEmbeddings()

vector = llm.embed_query(text="你是谁")

print(type(vector))
print(vector)