import csv
import logging
import time
from typing import Iterator

from openai import OpenAI

from config import settings
from prompts.bill_enrichment import CORE_INSTRUCTIONS, ARGUMENT_GUIDELINES, NORMATIVE_BASES_DIGEST
from utils import download_text_from_url, get_requests_session

logger = logging.getLogger(__name__)

# MODEL_NAME = "gpt-4o-mini"
MODEL_NAME = "gpt-4o"
INPUT_FILE_NAME = "bills_before_parliament_for_enrichment.csv"

class AIEnrichmentClient:
    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key)


    # def generate_bill_summary_completion(self, bill_title: str, bill_info_web_page_contents: list[str]) -> str:
    #     """
    #     Send the context (all relevant texts) and instructions to the LLM.
    #     Returns the model's output.
    #     """
    #     # Construct your prompt
    #     prompt = f"""
    #     I am going to dump on you the contents of one or two PDFs that relate to a given bill before the Australian parliament. Your task is to summarize the contents of these PDFs in a way that is clear and reasonably detailed. You do not have to include the legislative minutia in your summary, but more so focus on the key points and arguments made in the PDFs. Here is the context for the task:

    #     Title of the bill: {bill_title}

    #     ### PDF Contents ###
        
    #     """


    def generate_bill_completion(self, bill_title: str, bill_info_web_page_contents: list[str]) -> str:
        """
        Send the context (all relevant texts) and instructions to the LLM.
        Returns the model's output.
        """
        bill_info_web_page_contents_str = "\n\n\n".join(bill_info_web_page_contents)[:100000]

        # Construct your prompt
        prompt = f"""
Your task is to fill out a number of fields for a user-curated forum page relating to a bill before the Australian parliament. As I will explain below, some of these fields are argument fields, i.e. an "Argument For" and an "Argument Against" the bill. So let me first give you some information on the guidelines for the argument fields, as this will come in handy for your task:


#### Argument Guidelines ####
{ARGUMENT_GUIDELINES}



#### Normative Bases Digest ####
{NORMATIVE_BASES_DIGEST}




### Instructions ###
With the above guidelines in mind, I can now give the instructions for how to fill out the fields of the forum page. Please follow these precisely.

{CORE_INSTRUCTIONS}



### Information about the Bill ###
Finally, here is some context about the bill itself. The bill is titled \"{bill_title}\". The below is a dump of one or more PDFs that explains more about the bill. You will need to use this information to fill out the fields:

{bill_info_web_page_contents_str}



### Your Response ###
        """
        f = open("last_prompt.txt", "w")
        f.write(prompt)

        # Make the API call (OpenAI style)
        response = self.client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful content enrichment assistant."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            # max_tokens=2000,  # Adjust as needed
        )
        content = response.choices[0].message.content
        if not content:
            raise RuntimeError(f"No content returned from model. Refusal: {response.choices[0].message.refusal}")
        return content

def main():
    client = AIEnrichmentClient()
    session = get_requests_session()
    with open(f"static_data/{INPUT_FILE_NAME}", mode ='r') as file:    
        csv_dict: Iterator[dict[str, str]] = csv.DictReader(file)
        for row in list(csv_dict)[5:]:
            bill_title = row["title"]
            bill_info_web_page_contents: list[str] = []
            if row["explanatory_memo_pdf_url"]:
                bill_info_web_page_contents.append(download_text_from_url(session, row["explanatory_memo_pdf_url"]))
            if row["bill_digest_pdf_url"] != "None":
                bill_info_web_page_contents.append(download_text_from_url(session, row["bill_digest_pdf_url"]))
            completion = client.generate_bill_completion(
                bill_title=bill_title,
                bill_info_web_page_contents=bill_info_web_page_contents
            )
            f = open(f"completions/bill_enrichment/{bill_title.replace(' ', '_')}.txt", "w")
            f.write(completion)

            time.sleep(60)  # Avoid rate limiting
            




if __name__ == "__main__":
    main()
