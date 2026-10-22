from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

file_path = r"D:\PythonProject\John-AI-share\rag_practice\data\files\历史文化.txt"

text_loader = TextLoader(file_path=file_path, encoding="utf-8")

docs = text_loader.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=55,
    chunk_overlap=8,
    separators = ["\n\n", "\n", "。", "，", "、", " ", ""],
    length_function=len
)

chunks = splitter.split_text(docs[0].page_content)

for chunk in chunks:
    print(chunk)