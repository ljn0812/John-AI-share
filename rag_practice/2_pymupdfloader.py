from langchain_community.document_loaders import PyMuPDFLoader

file_path = r"D:\PythonProject\John-AI-share\rag_practice\data\files\sample_document.pdf"

pdf_loader = PyMuPDFLoader(file_path=file_path)

docs = pdf_loader.load()

print(type(docs))

print(type(docs[0]))


for doc in docs:
    print(doc.page_content)
    print(doc.metadata)