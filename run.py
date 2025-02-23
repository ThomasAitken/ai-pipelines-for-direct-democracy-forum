import logging

from openai import OpenAI

from config import settings

logger = logging.getLogger(__name__)

MODEL_NAME = "gpt-4o-mini"
INPUT_FILE_NAME = "bills_before_parliament_for_enrichment.csv"

INSTRUCTIONS = """
You will need to fill out the following fields:

** Field 1: the High-level Summary of the Bill **
A statement, in simple language, of the purpose of the bill and what it proposes to change. Make it clear and concise - ideally 1-2 sentences.

If there is any relevant context or background, include it in the optional second paragraph.


** Field 2: the Detailed Summary of the Bill **
Whereas the high-level summary describes the idea of the bill without necessarily referring to specific legislation, this section should briefly describe which legislation is affected and how. There is currently a word limit of 300 words.

If there is a good bill digest or explanatory memo associated with the bill, you may be able to take guidance from it. If lifting passages from these sources, please make sure to represent them as quotes (using the `blockquote` HTML tag with nested `p` tags). 


** Field 3: the Argument For the Bill **
This field should follow the argument guidelines that you read earlier. It must begin by enumerating appropriate Normative Bases (with hyperlinks) under an italicised heading of this name. This section can be brief if there is not much to say, or longer if there are many reasons to support the bill.


** Field 4: the Argument Against the Bill **
This field should follow the argument guidelines that you read earlier. It must begin by enumerating appropriate Normative Bases (with hyperlinks) under an italicised heading of this name. This section can be brief if there is not much to say, or longer if there are many reasons to oppose the bill.


** Field 5: Categories **
Choose up to 3 categories that best describe the bill from the following list:
```
- Anti-Corruption
- Civics
- Criminal Law Reform
- Family Law Reform
- Education
- Media / Advertising
- Climate Change / Environment
- Democratic Institutions
- Competition Policy
- Consumer Protection
- National Security
- Defence
- Discrimination / Human Rights
- Trade Policy
- Social Support / Welfare
- Poverty
- Labour
- Housing Policy
- Healthcare
- Industrial Policy
- Immigration
- Energy Policy
- Infrastructure
- Foreign Policy
- Financial Regulation
- Agriculture
- Transport
- Science / Technology
- Taxation
- Indigenous
- Fiscal Package (Stimulus / Debt Relief)



Return your answer as a JSON object with the following structure:
```
{
  "high_level_summary": "The bill proposes to...",
  "detailed_summary": "The bill affects...",
  "argument_for": "The bill should be supported because...",
  "argument_against": "The bill should be opposed because...",
  "categories": ["Civics", "Education"]
}
```
Remember that "high_level_summary", "detailed_summary", "argument_for", and "argument_against" should be in HTML, using the same set of tags you have seen in the earlier Worked Example (plus `blockquote` for quotes). Recall that `<ul><li>` will work for bulleted lists and `<ol><li>` for numbered lists, <b> for bold and <u> for underlined. Footnotes should follow the same HTML formatting you saw earlier.

Thank you in advance.
"""


class AIEnrichmentClient:
    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key)


    def generate_completion(self, bill_title: str, argument_guidelines_html: str, normative_bases_html: str, bill_info_web_page_contents: list[str]) -> str:
        """
        Send the context (all relevant texts) and instructions to the LLM.
        Returns the model's output.
        """
        # Join the context texts (you might want to chunk or summarize if too large)
        context_snippet = "\n\n".join(bill_info_web_page_contents)

        # Construct your prompt
        prompt = f"""
        You are given multiple pieces of context from different web pages relating to a given bill before the Australian parliament titled \"{bill_title}\":

        {context_snippet}

        Your task will be to fill out a number of fields on a user-curated forum page relating to this bill. Two of these fields are an "Argument For" and an "Argument Against" the bill. The conventions for these fields are outlined in the following context:

        {argument_guidelines_html}


        {normative_bases_html}


        With all the above information in mind, I can now give the instructions for how to fill out the fields of the forum page. Please follow these precisely.

        {INSTRUCTIONS}

        YOUR RESPONSE:
        """
        print(prompt)

        # Make the API call (OpenAI style)
        # response = self.client.chat.completions.create(
        #     model=MODEL_NAME.replace("_", "-"),
        #     messages=[
        #         {
        #             "role": "system",
        #             "content": "You are a helpful content enrichment assistant."
        #         },
        #         {
        #             "role": "user",
        #             "content": prompt
        #         }
        #     ],
        #     temperature=0.7,
        #     max_tokens=2000,  # Adjust as needed
        # )
        # content = response.choices[0].message.content
        # if not content:
        #     raise RuntimeError(f"No content returned from model. Refusal: {response.choices[0].message.refusal}")
        # return content

def main():
    print("Hello from ddf-ai-enrichment-pipeline!")
    reader = PdfReader("example.pdf")




if __name__ == "__main__":
    main()
