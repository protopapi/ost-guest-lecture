import langextract as lx
import textwrap

import io_utils
import extractor
import argparse

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source",
        help = "Source file name (e.g., source_name.pdf)",
        required = True
    )
    args = parser.parse_args()

    # The input text to be processed
    input_text = io_utils.load_text_from_source(args.source, in_dir="in") # hardcore io_utils.load_text_from_source("source_name.pdf", in_dir="in")

    # Run the extraction process
    result = extractor.run_extractions(input_text)

    # Save the extraction outputs
    io_utils.save_extraction_outputs(
        result, 
        out_name=args.source,
        out_dir="out"
    )

if __name__ == "__main__":
    main()