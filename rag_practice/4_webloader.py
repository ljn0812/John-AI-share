from langchain_community.document_loaders import WebBaseLoader

loader = WebBaseLoader("https://python.langchain.com/docs/")
documents = loader.load()

print(f"加载了 {len(documents)} 个文档")
print(f"元数据：{documents[0].metadata}")
print(f"标题: {documents[0].metadata.get('title', 'N/A')}")
print(f"URL: {documents[0].metadata['source']}")
print(f"内容长度: {len(documents[0].page_content)} 字符")
print(f"内容: {documents[0].page_content[:1000]}")
