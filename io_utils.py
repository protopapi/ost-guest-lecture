from markitdown import MarkItDown
from pathlib import Path
import langextract as lx

md = MarkItDown()

def load_text_from_source(
        source_name: str, # provide the source file name, no default
        in_dir: str = "in", # optional, no default
        md_out_dir: str | None = "out" # optional, default to None, e.g. load_text_from_source("source_name", md_out_dir=None)
):
    """
    Load text from source files, supporting .pdf or .txt formats. Convert to markdown. Save in output directory.
    """

    source_path = Path(in_dir) / source_name # Converts the string in_dir (e.g. "in") into a Path object, / is the join operator

    # check if file exists
    if not source_path.is_file(): # defensive validation check, is_file method of pathlib checks if the path points to a file
        raise FileNotFoundError(f"Source file not found: {source_path}") # raising exception if file not found, f-string
    
    # get suffix 
    suffix = source_path.suffix.lower() # get the file extension, e.g. .pdf or .txt, convert to lowercase for consistency

    # check suffix and convert
    if suffix == ".pdf" or suffix == ".txt":
        result = md.convert(str(source_path)) # conversion to markdown, str() converts Path object to string
        md_text = result.text_content # get text content from the conversion result

        # save markdown text if output directory
        if md_out_dir is not None:
            out_dir = Path(md_out_dir) # convert md_out_dir string to Path object
            out_dir.mkdir(parents=True, exist_ok=True) # create output directory if it doesn't exist, parents=True creates any necessary parent directories, exist_ok=True avoids error if directory exists
            out_path = out_dir / f"{source_path.stem}.md" # create output file path with .md extension"
            out_path.write_text(md_text, encoding = "utf-8") # write markdown text to file with utf-8 encoding
       
        return md_text
    
    # return source_path.read_text(encoding = "utf-8") # if not pdf or txt, read as plain text file


def save_extraction_outputs(
        result, # required parameter
        out_name: str | None = None, # optional parameter, string or None, default = None
        out_dir: str = "out"
) -> tuple[Path, Path]: # returns a tuple (immutable) of Path objects
    """
    Save extraction results in out directory to JSONL and generate HTML visualization.
    """

    out_dir_path = Path(out_dir)
    out_dir_path.mkdir(parents=True, exist_ok=True) # create output directory if it doesn't exist
    
    out_name = Path(out_name).stem if out_name is not None else "extraction_results" # get stem of out_name or default name

    jsonl_path = out_dir_path / f"{out_name}.jsonl"
    html_path = out_dir_path / f"{out_name}.html"

    # Save the results to a JSONL file
    lx.io.save_annotated_documents(
        [result], 
        output_name=jsonl_path.name, #.name important not to only save path
        output_dir=out_dir)

    # Generate the visualization from the file
    html_content = lx.visualize(jsonl_path)
    with open(html_path, "w", encoding="utf-8") as f:
        if hasattr(html_content, 'data'):
            f.write(html_content.data)  # For Jupyter/Colab
        else:
            f.write(html_content)

    return jsonl_path, html_path

