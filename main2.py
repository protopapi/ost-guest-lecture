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
    You are a senior underwriter in a reinsurance company and an excellent linguist.  
    You extract structured fields from treaty documents in markdown format within non-life reinsurance.
    Use exact substrings from the source (no paraphrasing). 
    If a value is missing, omit it.
    Use only the categories defined within examples.
    """
)

# 2. Provide a high-quality example to guide the model
examples = [
    lx.data.ExampleData(
        text=textwrap.dedent(
            """
            Slip 1
            Risk Details
            UMR:
            A661997MP00001
            TYPE:
            Motor Excess of Loss Reinsurance
            REINSURED:
            HYDROBIUS INSURANCE AND REINSURANCE S.A., Athens, Greece
            PERIOD:
            Losses occurring during the period commencing 12 months from 1st January 2024 to 31st December
            2024 both days inclusive Local Standard Time at place where loss occurs.
            CLASS OF BUSINESS:
            Business in respect of Motor Insurances covering Third Party Bodily Injury, Third Party Material
            Damage, Passengers Liability, including Green Cards and losses resulting from Presidential Decree
            1019.
            TERRITORIAL SCOPE:
            Business underwritten in the territory of Greece but extended to cover European Union countries,
            Switzerland, Green Cards and Presidential Decree 1019.
            LIMITS & RETENTIONS:
            1st Layer
            EUR 3,000,000 Ultimate Net Loss each and every accident or loss or series of accidents or losses
            arising out of one event in excess of:
            EUR 2,000,000 Ultimate Net Loss each and every accident or loss or series of accidents or losses
            arising out of one event.
            2nd Layer
            EUR 45,000,000 Ultimate Net Loss each and every accident or loss or series of accidents or losses
            arising out of one event in excess of:
            EUR 5,000,000 Ultimate Net Loss each and every accident or loss or series of accidents or losses
            arising out of one event.
            3rd Layer
            Unlimited Ultimate Net Loss each and every accident or loss or series of accidents or losses arising
            out of one event in excess of:
            EUR 50,000,000 Ultimate Net Loss each and every accident or loss or series of accidents or losses
            arising out of one event.
            PREMIUM:
            1st Layer
            Minimum & Deposit: EUR 115,440
            Premium payable in four equal instalments of EUR 28,860 each at 1st January 2024, 1st April 2024,
            1st July 2024 and 1st October 2024 subject to LSW3000 (60 days) per each instalment.
            2nd Layer
            Minimum & Deposit: EUR 88,800
            Premium payable in four equal instalments of EUR 22,200 each at 1st January 2024, 1st April 2024,
            1st July 2024 and 1st October 2024 subject to LSW3000 (60 days) per each instalment.
            3rd Layer
            Minimum & Deposit: EUR 47,360
            Premium payable in four equal instalments of EUR 11,840 each at 1st January 2024, 1st April 2024,
            1st July 2024 and 1st October 2024 subject to LSW3000 (60 days) per each instalment.
            The term ‘Gross Net Premium Income’ shall mean the original gross premium written by the
            Reinsured, in respect of the business covered hereunder, less return premiums and less the premiums
            for outwards reinsurance, recoveries under which inure to the benefit of reinsurers hereon.
            PREMIUM PAYMENT TERMS:
            The (Re)Insured undertakes that premium will be paid in full to Reinsurers within 60 days of inception
            of this policy (or, in respect of instalment premiums, when due).
            ESTIMATED PREMIUM INCOME:
            Estimated Premium Income for the period 01/01/2024 - 31/12/2024:
            EUR 36,000,000
            TAXES PAYABLE BY THE REINSURED & ADMINISTERED BY
            UNDERWRITERS:
            None
            CONDITIONS:
            •  Reinsurance Clause
            •  Ultimate Net Loss Clause
            •  Net Retained Lines Clause
            •  Premium Clause
            •  Premium Processing Clause LSW3003 - 14/12/09
            •  Claims Reporting and Co-Operation Clause
            •  Loss Settlements Clause
            •  Currency Conversion Clause
            •  Apportionment Clause
            •  Change In Law Clause
            •  Local Jurisdiction Clause
            •  Special Cancellation Clause
            •  Limits and Retentions Clause
            •  Extended Expiration Clause
            •  Amendments and Alterations Clause
            """
        ).strip(),
        extractions=[
            # umr
            lx.data.Extraction(
                extraction_class="umr_nr",
                extraction_text="A661997MP00001"
            ),
            # type
            lx.data.Extraction(
                extraction_class="reinsurance_type",
                extraction_text="Motor Excess of Loss Reinsurance"
            ),
            # reinsured
            lx.data.Extraction(
                extraction_class="company",
                extraction_text="HYDROBIUS INSURANCE AND REINSURANCE S.A., Athens, Greece",
                attributes={"role": "cedent"}
            ),
            # period
            lx.data.Extraction(
                extraction_class="period",
                extraction_text="12 months",
                attributes={"type": "duration"}
            ),
            lx.data.Extraction(
                extraction_class="period",
                extraction_text="1st January 2024",
                attributes={"type": "start"}
            ),
            lx.data.Extraction(
                extraction_class="period",
                extraction_text="31st December 2024",
                attributes={"type": "end"}
            ),
            # class of business
            lx.data.Extraction(
                extraction_class="class_of_business",
                extraction_text="Motor Insurances",
                attributes={"type": "business"}
            ),
            lx.data.Extraction(
                extraction_class="class_of_business",
                extraction_text="Third Party Bodily Injury, Third Party Material Damage, Passengers Liability, including Green Cards and losses resulting from Presidential Decree 1019",
                attributes={"type": "coverage"}
            ),
            # territorial scope
            lx.data.Extraction(
                extraction_class="territory",
                extraction_text="Greece",
                attributes={"type": "main"}
            ),
            lx.data.Extraction(
                extraction_class="territory",
                extraction_text="European Union countries, Switzerland, Green Cards and Presidential Decree 1019",
                attributes={"type": "extended"}
            ),
            # limits & retentions
            lx.data.Extraction(
                extraction_class="limits",
                extraction_text="EUR 3,000,000",
                attributes={"layer": "1st"}
            ),
            lx.data.Extraction(
                extraction_class="retentions",
                extraction_text="EUR 2,000,000",
                attributes={"layer": "1st"}
            ),
            lx.data.Extraction(
                extraction_class="limits",
                extraction_text="EUR 45,000,000",
                attributes={"layer": "2nd"}
            ),
            lx.data.Extraction(
                extraction_class="retentions",
                extraction_text="EUR 5,000,000",
                attributes={"layer": "2nd"}
            ),
            lx.data.Extraction(
                extraction_class="limits",
                extraction_text="Unlimited",
                attributes={"layer": "3rd"}
            ),
            lx.data.Extraction(
                extraction_class="retentions",
                extraction_text="EUR 50,000,000",
                attributes={"layer": "3rd"}
            ),
            # 1st layer premium
            lx.data.Extraction(
                extraction_class="premium",
                extraction_text="EUR 115,440",
                attributes={"part": "minimum & deposit amount", "layer": "1st"}
            ),
            lx.data.Extraction(
                extraction_class="premium",
                extraction_text="four",
                attributes={"part": "instalments", "layer": "1st"}
            ),
            lx.data.Extraction(
                extraction_class="premium",
                extraction_text="EUR 28,860",
                attributes={"part": "instalment amount", "layer": "1st"}
            ),
            lx.data.Extraction(
                extraction_class="premium",
                extraction_text="1st January 2024, 1st April 2024, 1st July 2024 and 1st October 2024",
                attributes={"part": "instalment dates", "layer": "1st"}
            ),
            # 2nd layer premium
            lx.data.Extraction(
                extraction_class="premium",
                extraction_text="EUR 88,800",
                attributes={"part": "minimum & deposit amount", "layer": "2nd"}
            ),
            lx.data.Extraction(
                extraction_class="premium",
                extraction_text="four",
                attributes={"part": "instalments", "layer": "2nd"}
            ),
            lx.data.Extraction(
                extraction_class="premium",
                extraction_text="EUR 22,200",
                attributes={"part": "instalment amount", "layer": "2nd"}
            ),
            lx.data.Extraction(
                extraction_class="premium",
                extraction_text="1st January 2024, 1st April 2024, 1st July 2024 and 1st October 2024",
                attributes={"part": "instalment dates", "layer": "2nd"}
            ),
            # 3rd layer premium
            lx.data.Extraction(
                extraction_class="premium",
                extraction_text="EUR 47,360",
                attributes={"part": "minimum & deposit amount", "layer": "3rd"}
            ),
            lx.data.Extraction(
                extraction_class="premium",
                extraction_text="four",
                attributes={"part": "instalments", "layer": "3rd"}
            ),
            lx.data.Extraction(
                extraction_class="premium",
                extraction_text="EUR 11,840",
                attributes={"part": "instalment amount", "layer": "3rd"}
            ),
            lx.data.Extraction(
                extraction_class="premium",
                extraction_text="1st January 2024, 1st April 2024, 1st July 2024 and 1st October 2024",
                attributes={"part": "instalment dates", "layer": "3rd"}
            ),
            # premium payment terms
            lx.data.Extraction(
                extraction_class="premium_terms",
                extraction_text="within 60 days of inception of this policy"
            ),
            # estimated premium income
            lx.data.Extraction(
                extraction_class="estimated_premium_income",
                extraction_text="01/01/2024",
                attributes={"part": "start"}
            ),
            lx.data.Extraction(
                extraction_class="estimated_premium_income",
                extraction_text="31/12/2024",
                attributes={"part": "end"}
            ),
            lx.data.Extraction(
                extraction_class="estimated_premium_income",
                extraction_text="EUR 36,000,000",
                attributes={"part": "amount"}
            ),
            # taxes
            lx.data.Extraction(
                extraction_class="taxes",
                extraction_text="None"
            ),
            # conditions
            lx.data.Extraction(
                extraction_class="conditions",
                extraction_text="Reinsurance Clause",
                attributes={"type": "clause"}
            ),
            lx.data.Extraction(
                extraction_class="conditions",
                extraction_text="Ultimate Net Loss Clause",
                attributes={"type": "clause"}
            ),
            lx.data.Extraction(
                extraction_class="conditions",
                extraction_text="Net Retained Lines Clause",
                attributes={"type": "clause"}
            ),
            lx.data.Extraction(
                extraction_class="conditions",
                extraction_text="Premium Clause",
                attributes={"type": "clause"}
            ),
            lx.data.Extraction(
                extraction_class="conditions",
                extraction_text="Premium Processing Clause LSW3003 - 14/12/09",
                attributes={"type": "clause"}
            ),
            lx.data.Extraction(
                extraction_class="conditions",
                extraction_text="Claims Reporting and Co-Operation Clause",
                attributes={"type": "clause"}
            ),
            lx.data.Extraction(
                extraction_class="conditions",
                extraction_text="Loss Settlements Clause",
                attributes={"type": "clause"}
            ),
            lx.data.Extraction(
                extraction_class="conditions",
                extraction_text="Currency Conversion Clause",
                attributes={"type": "clause"}
            ),
            lx.data.Extraction(
                extraction_class="conditions",
                extraction_text="Apportionment Clause",
                attributes={"type": "clause"}
            ),
            lx.data.Extraction(
                extraction_class="conditions",
                extraction_text="Change In Law Clause",
                attributes={"type": "clause"}
            ),
            lx.data.Extraction(
                extraction_class="conditions",
                extraction_text="Local Jurisdiction Clause",
                attributes={"type": "clause"}
            ),
            lx.data.Extraction(
                extraction_class="conditions",
                extraction_text="Special Cancellation Clause",
                attributes={"type": "clause"}
            ),
            lx.data.Extraction(
                extraction_class="conditions",
                extraction_text="Limits and Retentions Clause",
                attributes={"type": "clause"}
            ),
            lx.data.Extraction(
                extraction_class="conditions",
                extraction_text="Extended Expiration Clause",
                attributes={"type": "clause"}
            ),
            lx.data.Extraction(
                extraction_class="conditions",
                extraction_text="Amendments and Alterations Clause",
                attributes={"type": "clause"}
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
