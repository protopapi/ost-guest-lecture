import langextract as lx
import textwrap

import argparse
from markitdown import MarkItDown
from pathlib import Path

# add CLI
parser = argparse.ArgumentParser()
parser.add_argument(
    "--source",
    required = True
)
args = parser.parse_args()

# 1. Define the prompt and extraction rules
prompt = textwrap.dedent(
    """\
    Extract characters, emotions, and relationships in order of appearance.
    Use exact text for extractions. Do not paraphrase or overlap entities.
    Provide meaningful attributes for each entity to add context.
    """
)

# 2. Provide a high-quality example to guide the model
examples = [
    lx.data.ExampleData(
        text="ROMEO. But soft! What light through yonder window breaks? It is the east, and Juliet is the sun.",
        extractions=[
            lx.data.Extraction(
                extraction_class="character",
                extraction_text="ROMEO",
                attributes={"emotional_state": "wonder"}
            ),
            lx.data.Extraction(
                extraction_class="emotion",
                extraction_text="But soft!",
                attributes={"feeling": "gentle awe"}
            ),
            lx.data.Extraction(
                extraction_class="relationship",
                extraction_text="Juliet is the sun",
                attributes={"type": "metaphor"}
            ),
        ]
    )
]

# add source upload, convert and save
def load_from_source(source_path: str) -> str:
    md = MarkItDown() # calling a class, creating an instance, is an object
    source = Path(str(source_path))

    result = md.convert(source)
    md_text = result.text_content

    output_path = source.with_suffix('.md')
    output_path.write_text(md_text, encoding = 'utf-8')

    return md_text

# The input text to be processed
input_text = load_from_source(args.source)

# Run the extraction
result = lx.extract(
    text_or_documents=input_text,
    prompt_description=prompt,
    examples=examples,
    model_id="gpt-oss:120b-cloud",
)

# Save the results to a JSONL file
lx.io.save_annotated_documents([result], output_name="extraction_results.jsonl", output_dir=".")

# Generate the visualization from the file
html_content = lx.visualize("extraction_results.jsonl")
with open("visualization.html", "w", encoding = "utf-8") as f:
    if hasattr(html_content, 'data'):
        f.write(html_content.data)  # For Jupyter/Colab
    else:
        f.write(html_content)
