import requests
import os
from langchain_community.document_loaders import PyPDFLoader


def download_paper(url):

    os.makedirs("papers", exist_ok=True)

    filename = url.split("/")[-1] + ".pdf"

    path = os.path.join("papers", filename)

    r = requests.get(url)

    with open(path, "wb") as f:
        f.write(r.content)

    return path


def load_pdf(path):

    loader = PyPDFLoader(path)

    docs = loader.load()

    return docs