from app.config import Settings
import pytest

from app.ingest import PageText, UnsupportedDocumentError, chunk_pages, extract_pages, normalize_text


def test_normalize_text_collapses_whitespace():
    assert normalize_text("Hello\n\nworld   there") == "Hello world there"


def test_chunk_page_text_uses_overlap():
    page = PageText(
        document_name="doc.txt",
        page_number=None,
        text=(
            "Sentence one. Sentence two. Sentence three. Sentence four. "
            "Sentence five. Sentence six. Sentence seven. Sentence eight."
        ),
    )
    settings = Settings(chunk_size=70, chunk_overlap=25)
    chunks = chunk_pages([page], settings)
    assert len(chunks) >= 2
    assert chunks[0].content.split()[-1] in chunks[1].content


def test_extract_pages_rejects_malformed_pdf():
    with pytest.raises(UnsupportedDocumentError, match="could not be read"):
        extract_pages("broken.pdf", b"not a real pdf", "application/pdf")
