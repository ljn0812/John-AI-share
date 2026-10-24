import hashlib

text="你好，我想要学习Python 和 AI"



hash_value = hashlib.md5(text.encode('utf-8')).hexdigest()

print(hash_value)  #4a266efc1060357fa35a6ade929f7eb4