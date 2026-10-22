from langchain_text_splitters import RecursiveCharacterTextSplitter

text = "这是一个超长超长超长超长超长超长超长超长超长超长超长超长超长超长超长的单词"

splitter = RecursiveCharacterTextSplitter(
    separators=[" ", ""],  # 使用空格作为分隔符
    chunk_size=20,
    chunk_overlap=5
)

chunks = splitter.split_text(text)

for chunk in chunks:
    print(f"'{chunk}'")