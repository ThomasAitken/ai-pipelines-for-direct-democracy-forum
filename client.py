from typing import Any
from config import settings

from google import genai
from google.genai.types import GenerateContentConfig, Part, ToolListUnion


MODEL_NAME = "gemini-2.5-flash"

class AIClient:
    """
    Client to interact with an API provider for various AI tasks.

    Right now, this is specifically for Google Gemini via the GenAI API.
    """

    def __init__(self, api_key: str = settings.api_key):
        self.client = genai.Client(api_key=api_key)

    def generate_content(self, prompt: str, response_schema: dict[str, Any], pdfs: list[bytes], use_url_context: bool = True) -> str:
        """
        Send the context (all relevant texts) and instructions to the LLM.
        Returns the model's output.
        """
        f = open("last_prompt.txt", "w")
        f.write(prompt)

        tools: ToolListUnion = [] # pyright: ignore[reportUnknownVariableType]
        if use_url_context:
            # Enable the URL context tool so the model can fetch & read the PDFs
            tools = [ # pyright: ignore[reportUnknownVariableType]
                {"url_context": {}},
            ]

        response = self.client.models.generate_content( # pyright: ignore[reportUnknownMemberType]
            model=MODEL_NAME,
            contents=[
                prompt,
                *(Part.from_bytes(data=pdf, mime_type="application/pdf") for pdf in pdfs),
            ],
            config=GenerateContentConfig(
                tools=tools,
                # For some reason, using response_mime_type in conjunction with tools causes a 400 response
                # See forum: https://discuss.ai.google.dev/t/why-is-using-a-response-schema-not-supported-when-using-grounded-search/92327/20
                # response_mime_type="application/json",
                response_json_schema=response_schema,
            ),
        )

        if not response.text:
            # Print out the full response for debugging
            print("Full response:", response)
            raise ValueError("No text in response from model")
        return response.text