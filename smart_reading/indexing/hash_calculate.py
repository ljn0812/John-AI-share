import hashlib

class HashCalculate:

    def compute_hash(self, pdf_bytes:bytes) -> str:
        """
        Compute the MD5 hash of the given PDF bytes.

        :param pdf_bytes: The PDF content in bytes.
        :return: The MD5 hash as a hexadecimal string.
        """
        return hashlib.md5(pdf_bytes).hexdigest()

    def compute_hash_from_file(self, pdf_path: str) -> str:
        """
        Compute the MD5 hash of the given PDF file.

        :param pdf_path: The path to the PDF file.
        :return: The MD5 hash as a hexadecimal string.
        """
        hash_md5 = hashlib.md5()
        with open(pdf_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()