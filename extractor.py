import textwrap
import langextract as lx


# 1. Define the prompt and extraction rules
def build_prompt() -> str:
    """
    Base Prompt
    """
    return textwrap.dedent(
        """\
        Extract characters, emotions, and relationships in order of appearance.
        Use exact text for extractions. Do not paraphrase or overlap entities.
        Provide meaningful attributes for each entity to add context.
        """
    )

# 2. Provide a high-quality example to guide the model
def build_examples() -> list[lx.data.ExampleData]:
    """
    list of ExampleData
    """
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

# Run the extraction
def run_extractions(input_text: str):
    prompt = build_prompt()
    examples = build_examples()

    result = lx.extract(
        text_or_documents=input_text,
        prompt_description=prompt,
        examples=examples,
        model_id="gpt-oss:20b-cloud",
        fence_output=True,
        use_schema_constraints=False
    )
    return result