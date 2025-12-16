import textwrap
import langextract as lx

def base_prompt() -> str:
    """1. Define the prompt and extraction rules"""
    return textwrap.dedent("""\
        Extract characters, emotions, and relationships in order of appearance.
        Use exact text for extractions. Do not paraphrase or overlap entities.
        Provide meaningful attributes for each entity to add context."""
    )

def get_examples() -> list[lx.data.ExampleData]:
    """ 2. Provide a high-quality example to guide the model"""
    return [
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

def extract(input_text: str):
    prompt = base_prompt()
    examples = get_examples()

    # Run the extraction
    result = lx.extract(
        text_or_documents=input_text,
        prompt_description=prompt,
        examples=examples,
        model_id="gpt-oss:20b-cloud",
        fence_output=True,
        use_schema_constraints=False

    )

    return result