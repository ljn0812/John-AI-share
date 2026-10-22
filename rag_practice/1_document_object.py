


from langchain_core.documents import Document

doc = Document(
    page_content="文档内容",
    metadata={'source': 'example.txt', 'page': 1}
)

print(doc)
print(doc.page_content)
print(doc.metadata)