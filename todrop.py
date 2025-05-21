@staticmethod
def preprocess_text(text):
    """Cleans and preprocesses text."""
    # If it's a LangChain Document or similar, extract the actual text
    if hasattr(text, "page_content"):
        text = text.page_content

    # Now text is a string
    text = text.replace("\xa0", " ")
    if re.match(r"[\.\!\,\;]", text):
        text = " ".join(text.split()[1:])
    return text
