from langchain_text_splitters import RecursiveCharacterTextSplitter

text = "今天天气很好。我们去吃饭！你觉得怎么样？走吧。明天还要上班。记得早起！"

splitter1 = RecursiveCharacterTextSplitter(
    separators=["。", "！", "？"],
    is_separator_regex=False,
    chunk_size=10,   # 改小，强制切分
    chunk_overlap=0,
)
chunks1 = splitter1.split_text(text)
print("\n【is_separator_regex=False】切分结果:")
for i, chunk in enumerate(chunks1, 1):
    print(f"  块{i}: '{chunk}'")

splitter2 = RecursiveCharacterTextSplitter(
    separators=["(?<=。)", "(?<=！)", "(?<=？)"],
    is_separator_regex=True,
    chunk_size=10,   # 同样改小
    chunk_overlap=0,
)
chunks2 = splitter2.split_text(text)
print("\n【is_separator_regex=True】切分结果:")
for i, chunk in enumerate(chunks2, 1):
    print(f"  块{i}: '{chunk}'")