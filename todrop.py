import re
from langchain.text_splitter import RecursiveCharacterTextSplitter
from some_module import Document  # Replace with actual import

class TextProcessor:
    def __init__(self, input_path, tokenizer=None, split_kwargs=None, summarization_kwargs=None):
        self.input_path = input_path
        self.tokenizer = tokenizer
        self.split_kwargs = split_kwargs or {}
        self.summarization_kwargs = summarization_kwargs or {}

    @staticmethod
    def preprocess_text(text):
        """Cleans and preprocesses text."""
        text = text.replace("\xa0", " ")
        if re.match(r"^(\.|\,|;)", text):
            text = " ".join(text.split()[1:])
        return text

    def process_articles(self):
        """Processes articles for general text processing."""
        doc_article = Document(self.input_path)
        splitter = RecursiveCharacterTextSplitter.from_huggingface_tokenizer(
            self.tokenizer, **self.split_kwargs
        )
        return [
            split
            for paragraph in doc_article.paragraphs
            for split in splitter.split_text(paragraph.text)
        ]

    def process_articles_summarization(self):
        """Processes articles specifically for summarization."""
        doc_article = Document(self.input_path)
        splitter = RecursiveCharacterTextSplitter(**self.summarization_kwargs)
        chunks = splitter.create_documents(
            texts=[paragraph.text for paragraph in doc_article.paragraphs]
        )
        chunks = splitter.split_documents(chunks)
        return [chunk.page_content for chunk in chunks]

    def get_new_document(self):
        """Returns processed articles after preprocessing."""
        return list(map(self.preprocess_text, self.process_articles()))

    def get_documents_for_summarization(self):
        """Returns processed summarization articles after preprocessing."""
        return list(map(self.preprocess_text, self.process_articles_summarization()))

# Usage Example
if __name__ == "__main__":
    input_path = "path/to/file.txt"
    tokenizer = None  # Provide tokenizer if needed
    split_kwargs = {}  # Define any necessary kwargs
    summarization_kwargs = {}  # Define summarization-specific kwargs

    processor = TextProcessor(input_path, tokenizer, split_kwargs, summarization_kwargs)

    new_document = processor.get_new_document()
    documents_4_summarization = processor.get_documents_for_summarization()

    print("Processed Documents:", new_document)
    print("Summarization Documents:", documents_4_summarization)
