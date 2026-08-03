import os
from pathlib import Path
from typing import Any

file_io_schema = {
    "type": "function",
    "function": {
        "name": "read_file",
        "description": "Read the contents of a .txt or .pdf file from disk.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Absolute or relative path to the file to read."
                }
            },
            "required": ["path"]
        }
    }
}


def read_file(path: str) -> dict[str, Any]:
    try:
        file_path = Path(path).expanduser().resolve()
        if not file_path.exists():
            return {"error": f"File not found: {path}"}

        if not file_path.is_file():
            return {"error": f"Not a file: {path}"}

        suffix = file_path.suffix.lower()
        if suffix == ".txt":
            content = file_path.read_text(encoding="utf-8")
            return {"content": content, "type": "text"}

        if suffix == ".pdf":
            try:
                import pypdf
            except ImportError:
                return {"error": "pypdf is required to read PDF files"}

            reader = pypdf.PdfReader(str(file_path))
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
            return {"content": text, "type": "pdf"}

        return {"error": f"Unsupported file type: {suffix or 'unknown'}"}
    except Exception as exc:
        return {"error": str(exc)}
