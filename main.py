import argparse

import extractor
import io_utils

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source",
        help="Name of source file in 'in/' folder (supports .pdf via MarkItDown, or plain text)",
        required=True,
    )
    args = parser.parse_args()

    input_text = io_utils.load_text_from_source(args.source, in_dir="in")

    result = extractor.run_extraction(input_text)

    jsonl_path, html_path = io_utils.save_extraction_outputs(
        result,
        source_filename=args.source,
        out_dir="out",
    )

    print(f"Extraction complete.\nJSONL: {jsonl_path}\nHTML: {html_path}")

if __name__ == "__main__":
    main()