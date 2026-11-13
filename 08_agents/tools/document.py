import os
from markitdown import MarkItDown, StreamInfo
from io import BytesIO
from pydantic import Field

SUPPORTED_FILE_TYPES = ("pdf", "docx")


def binary_document_to_markdown(binary_data: bytes, file_type: str) -> str:
    """Converts binary document data to markdown-formatted text."""
    md = MarkItDown()
    file_obj = BytesIO(binary_data)
    stream_info = StreamInfo(extension=file_type)
    result = md.convert(file_obj, stream_info=stream_info)
    return result.text_content


def document_path_to_markdown(
    file_path: str = Field(
        description="Absolute path to a PDF (.pdf) or Word (.docx) file on the local filesystem"
    ),
) -> str:
    """Convert a PDF or DOCX file on disk to markdown text.

    Reads the file at the given path and converts its contents to
    markdown, preserving structure such as headings, lists, and tables
    where possible. The file type is determined by the file extension
    (case-insensitive). Relative paths are resolved against the server's
    working directory, so prefer absolute paths.

    When to use:
    - When you need to read the text content of a local PDF or DOCX file

    When not to use:
    - For plain text or markdown files, which can be read directly
    - For other formats (e.g. .doc, .pptx, .xlsx), which are not supported

    Examples:
    >>> document_path_to_markdown("/Users/me/docs/report.docx")
    '# Quarterly Report\\n\\n- Revenue grew 10%...'
    """
    path = os.path.abspath(os.path.expanduser(file_path))

    file_type = os.path.splitext(path)[1].lower().lstrip(".")
    if file_type not in SUPPORTED_FILE_TYPES:
        raise ValueError(
            f"Unsupported file type '{file_type or '(none)'}' for {path}. "
            f"Supported types: {', '.join(SUPPORTED_FILE_TYPES)}"
        )
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    if os.path.isdir(path):
        raise IsADirectoryError(f"Path is a directory, not a file: {path}")

    with open(path, "rb") as f:
        binary_data = f.read()

    return binary_document_to_markdown(binary_data, file_type)
