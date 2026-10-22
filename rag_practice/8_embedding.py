from langchain_community.embeddings import DashScopeEmbeddings

embedding_model = DashScopeEmbeddings()


user_input = "猫坐在垫子上"

result = embedding_model.embed_query(user_input)


# batch embedding for multiple documents
# result = embedding_model.embed_documents([user_input])

print(type(result))
print(len(result))
print(result)