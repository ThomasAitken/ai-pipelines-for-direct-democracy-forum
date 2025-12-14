from typing import Literal
from pydantic import BaseModel, Field

Categories = Literal[
    "Anti-Corruption",
    "Civics",
    "Criminal Law Reform",
    "Family Law Reform",
    "Education",
    "Media / Advertising",
    "Climate Change / Environment",
    "Democratic Institutions",
    "Competition Policy",
    "Consumer Protection",
    "National Security",
    "Defence",
    "Discrimination / Human Rights",
    "Trade Policy",
    "Social Support / Welfare",
    "Poverty",
    "Labour",
    "Housing Policy",
    "Healthcare",
    "Industrial Policy",
    "Immigration",
    "Energy Policy",
    "Infrastructure",
    "Foreign Policy",
    "Financial Regulation",
    "Agriculture",
    "Transport",
    "Science / Technology",
    "Taxation",
    "Indigenous",
    "Fiscal Package (Stimulus / Debt Relief)"
]

class EnrichedBill(BaseModel):
    high_level_summary: str = Field(
        description="A high-level summary of the bill. Add any relevant context or background in an optional second paragraph.",
    )
    detail_summary: str = Field(
        description="A detailed summary of the bill, covering the key aspects, provisions, and implications. Include appropriate quotes from the explanatory memo or bill digest. Limit to 300 words.",
    )
    argument_for: str = Field(
        description="A persuasive, scholarly argument in favor of the bill. Must begin by enumerating the applicable Normative Bases (with hyperlinks) under an italicised heading of this name.",
    )
    argument_against: str = Field(
        description="A persuasive, scholarly argument against the bill. Must begin by enumerating the applicable Normative Bases (with hyperlinks) under an italicised heading of this name.",
    )
    categories: list[Categories] = Field(
        description="A list of categories chosen from the allowed set. Maximum of 3 items.",
        max_length=3,
    )