from langchain_community.document_loaders import WebBaseLoader, UnstructuredHTMLLoader
# loader = WebBaseLoader(["https://engineering.utdallas.edu" , "https://engineering.utdallas.edu/about/leadership/"])
#loader.requests_per_second = 1
from langchain.text_splitter import RecursiveCharacterTextSplitter

urls = ["https://engineering.utdallas.edu"]

text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size=100,
    chunk_overlap=20,
    length_function=len,
    is_separator_regex=False,
)
loader = WebBaseLoader(urls)
docs = loader.load()
print(docs)
text = text_splitter.create_documents(docs.page_content)
print("Printing Text : " , text)
print("Printing......")
print(docs)
print(len(docs))

# from langchain_text_splitters import RecursiveCharacterTextSplitter

# from langchain.chains import create_extraction_chain
# from langchain_community.document_loaders import AsyncHtmlLoader , AsyncChromiumLoader


# schema = {
#     "properties": {
#         "news_article_title": {"type": "string"},
#         "news_article_summary": {"type": "string"},
#     },
#     "required": ["news_article_title", "news_article_summary"],
# }
# from langchain_community.document_transformers import BeautifulSoupTransformer


# def extract(content: str, schema: dict):
#     return create_extraction_chain(schema=schema, llm=llm).run(content)
# def scrape_with_playwright(urls, schema):
#     loader = AsyncChromiumLoader(urls)
#     docs = loader.load()
#     bs_transformer = BeautifulSoupTransformer()
#     docs_transformed = bs_transformer.transform_documents(
#         docs, tags_to_extract=["span"]
#     )
#     print("Extracting content with LLM")

#     # Grab the first 1000 tokens of the site
#     splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
#         chunk_size=1000, chunk_overlap=0
#     )
#     splits = splitter.split_documents(docs_transformed)

#     # Process the first split
#     extracted_content = extract(schema=schema, content=splits[0].page_content)
#     pprint.pprint(extracted_content)
#     return extracted_content


