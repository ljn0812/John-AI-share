from langchain_community.document_loaders import TextLoader



file_path= r"D:\PythonProject\John-AI-share\rag_practice\data\files\北京有什么好玩的.txt"


text_loader = TextLoader(file_path=file_path, encoding="utf-8")

docs = text_loader.load()

print(type(docs))
print(len(docs))

print(type(docs[0]))


print(docs[0].page_content)
print(docs[0].metadata)
