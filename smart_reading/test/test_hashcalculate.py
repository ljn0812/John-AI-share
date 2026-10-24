from indexing.hash_calculate import HashCalculate

hash_cal = HashCalculate()

file_path = r"D:\PythonProject\John-AI-share\smart_reading\data\files\sample_document.pdf"

hash_result = hash_cal.compute_hash_from_file(file_path)
print(hash_result)
