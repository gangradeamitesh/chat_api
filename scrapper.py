from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.document_loaders import WebBaseLoader
from langchain.vectorstores import Chroma

class WebScrapper:

    def __init__(self) -> None:
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 1000 , 
            chunk_overlap = 200 ,
            length_function = len,
            is_separator_regex=False,
            separators=["\n\n\n+" , "\n\n","\n","."," ",""],
            strip_whitespace=True,
            add_start_index=True,
        )
        self.embeddings = HuggingFaceEmbeddings(
            model_name = "sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs = {'device' : 'cpu'} , 
            encode_kwargs = {'normalize_embeddings': True}
        )
        self.persist_directory = 'chroma_db',
        self.collection_name = "utd_engineering"

    def store_embeddings(self, texts):
        try:
            vectorDb = Chroma(
                collection_name=self.collection_name,
                persist_directory=self.persist_directory
            )

            vectorDb.add_documents(
                documents=texts,
                ids = [text.metadata['source']+text.metadata['start_index'] for text in texts]
            )
            vectorDb.persist()
            return True
        except Exception as e:
            print(f"Failed to store embedding : {str(e)}")
            return False


    def clean_text(self , text:str)->str:
        text = ' '.join(text.split())
        text = '\n'.join(line for line in text.splitlines() if line.split())
        return text

    def create_embeddings(self , texts:list)->list:
        try:
            embeddings = self.embeddings.embed_documents([text.page_content for text in texts])
            return embeddings
        except Exception as e:
            print(f"Failed to create embeddings :{str(e)}")
            return []

    def scrape_url(self, url):
        documents = self.get_documents(url)
        for doc in documents:
            doc.page_content = self.clean_text(doc.page_content)
        
        texts = self.text_splitter.split_documents(documents)
        print(texts)
        storage_sucess = self.store_embeddings(texts=texts)
        #embeddings = self.create_embeddings(texts)
        #print(embeddings)

        return {
            'url' : url,
            "total_chunks":len(texts),
            "storage_success":storage_sucess,
            "chunks":[
                {
                    'content':text.page_content,
                    'metadata':text.metadata,
                }for text in texts
            ]
        }
        
    def get_documents(self , url):
        try:
            loader = WebBaseLoader(url)
        except Exception as e:
            print(f"Call failed for the URL : {url}")
        return loader.load()
