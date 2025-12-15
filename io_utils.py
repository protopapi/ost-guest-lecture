from markitdown import MarkItDown
from pathlib import Path
import langextract as lx

_md = MarkItDown()

def load_text_from_source(
    source_name: str,
    in_dir: str = "in",
    md_out_dir: str | None = "out",
) -> str:
    """
    Load text from a source file. Supports .pdf files via MarkItDown conversion.
    """
    source_path = Path(in_dir) / source_name

    if not source_path.is_file():
        raise FileNotFoundError(f"Source file not found: {source_path}")

    suffix = source_path.suffix.lower()

    if suffix == ".pdf":
        result = _md.convert(str(source_path))
        md_text = result.text_content

        if md_out_dir is not None:
            out_dir = Path(md_out_dir)
            out_dir.mkdir(parents=True, exist_ok=True)
            out_path = out_dir / f"{source_path.stem}.md"
            out_path.write_text(md_text, encoding="utf-8")

        return md_text

    return source_path.read_text(encoding="utf-8")

def save_extraction_outputs(
    result,
    source_filename: str | None = None,
    output_basename: str | None = None,
    out_dir: str = "out",
) -> tuple[Path, Path]:
    """
    Save extraction results to JSONL and HTML files.
    """
    out_dir_path = Path(out_dir)
    out_dir_path.mkdir(parents=True, exist_ok=True)

    output_basename = output_basename or (Path(source_filename).stem if source_filename else "extraction_results")

    jsonl_path = out_dir_path / f"{output_basename}.jsonl"
    html_path = out_dir_path / f"{output_basename}.html"

    lx.io.save_annotated_documents(
        [result],
        output_name=jsonl_path.name,
        output_dir=out_dir,
    )

    html_content = lx.visualize(str(jsonl_path))
    with html_path.open("w", encoding="utf-8") as f:
        if hasattr(html_content, "data"):
            f.write(html_content.data)
        else:
            f.write(html_content)

    return jsonl_path, html_path