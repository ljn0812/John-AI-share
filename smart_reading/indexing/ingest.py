import logging
from pathlib import Path
from typing import List
from xml.dom.minidom import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from urllib.parse import urlparse
from langchain_community.document_loaders import PyMuPDFLoader

from config.setting import QaConfig
logger = logging.getLogger(__name__)


class PdfIngestor:

    SEPARATOR = ["(?<=\n)", "(?<=。)", "(?<=！)", "(?<=？)", "(?<=；)", "(?<=，)", " ", ""]

    def __init__(self, config: QaConfig) -> None:
        self._config = config
        self._splitter = RecursiveCharacterTextSplitter(
            chunk_size=self._config.chunk_size,
            chunk_overlap=self._config.chunk_overlap,
            is_separator_regex=True,
            separators=self.SEPARATOR)

    def _split_documents(self, documents: List[Document]) -> List[Document]:
        """
        Split the documents into smaller chunks using the configured splitter.
        """
        if not documents:
            logger.info("No documents found")
            return []

        try:
            chunks = self._splitter.split_documents(documents)
            logger.info(f"Splitted documents done: {len(documents)} 页 -> {len(chunks)} 块")
            return chunks
        except Exception as e:
            raise RuntimeError(f"Error occurred while splitting documents: {e}")

    def ingest(self, pdf_source:str) -> List[Document]:

        if self._is_url(pdf_source):
            return self._ingest_from_url(pdf_source)
        else:
            return self._ingest_from_file(pdf_source)

    def _is_url(self, source: str) -> bool:
        """
        判断字符串是否为 URL
        :param source: 源字符串
        :return: 是否为 URL
        """
        try:
            result = urlparse(source)
            return all([result.scheme in ['http', 'https'], result.netloc])
        except Exception:
            return False


    def _ingest_from_file(self, file_path: str) -> List[Document]:
        """
        从本地文件加载 PDF
        :param file_path: 文件路径
        :return: 切分后的Document列表
        """
        path = Path(file_path)
        # 验证文件存在
        if not path.exists():
            raise FileNotFoundError(f"PDF文件不存在: {file_path}")
        if not path.is_file():
            raise ValueError(f"路径不是文件: {file_path}")

        try:
            documents = PyMuPDFLoader(str(path)).load()
            return self._split_documents(documents)
        except Exception as e:
            raise RuntimeError(f"PDF加载失败 ({file_path}): {e}")

    def _ingest_from_url(self, url: str) -> List[Document]:
        """
        从URL加载PDF
        :param url: PDF文件的URL
        :return: 切分后的Document列表
        """
        # 判断文件是否存在 requests

        try:
            # PyMuPDFLoader 直接支持 URL
            documents = PyMuPDFLoader(url).load()
            return self._split_documents(documents)
        except Exception as e:
            raise RuntimeError(f"从URL加载PDF失败 ({url}): {e}")


if __name__ == '__main__':
    pdf_path = r'D:\PythonProject\John-AI-share\smart_reading\data\files\sample_document.pdf'

    ingestor = PdfIngestor(QaConfig())
    data = ingestor.ingest(pdf_path)
    print(len(data))