prompt = """
Your task is to fill out a number of fields for a user-curated forum page relating to a bill before the Australian parliament. I will shortly give you more information about the bill in question, but first I will cover the background.

This forum page will be hosted on a website called the "Direct Democracy Forum (Australia)". This website is intended to educate the public about the workings of federal politics and inspire critical public engagement with policy. The fields you are tasked with filling out are called "High-level Summary", "Detailed Summary", "Argument For", "Argument Against" and "Categories". Before I delve into more specifics, you should first consult the Direct Democracy Forum website's guidelines on filling out these fields, particularly those related to 'argument'. Here are the relevant links:

- Link to Argument Guidelines: https://directdemocracyforum.com/about/argument-guidelines
- Link to crucial concept of "Normative Bases": https://directdemocracyforum.com/about/normative-bases

Please read through these guidelines carefully before proceeding.

Note that you will be generating the textual fields in raw HTML format, such that they can be directly embedded into the forum page and interpreted (for subsequent editing) by a Rich Text Editor based on CKEditor5. This editor is configured to support bold, italics, underline, blockquotes, ordered lists, unordered lists, hyperlinks, horizontal lines, and footnotes (using a custom implementation). (It also supports a range of special characters: "Arrows", "Currency", "Text", "Mathematical", "Latin".) You should use these HTML tags as appropriate when generating your output. The "High-level Summary" output can usually be raw text but the other textual fields will likely require HTML tags for formatting.

Here are two examples of complete arguments, in the appropriate HTML format:

## Worked Example Arguments

** Argument For the Proposition that "The Government Should Grant Funding to the Direct Democracy Forum" **
```
<i>Normative Bases</i><ol><li><a href="/about/normative-bases#ProDemocracy">Pro-Democracy</a></li><li><a href="/about/normative-bases#Intellectualism">Intellectualism</a></li></ol><p>The "For" case starts from the premise that the basic concept of the Direct Democracy Forum should appeal to anyone who (a) wants ordinary people to be more involved in political conversations or (b) would like to elevate the sophistication of political discourse in Australia. Anyone who has these views should support the success of the forum, and the surest route to success is to ensure that it has sufficient funding for maintenance and improvement as it scales.</p><p>The budgetary requirements of the forum are quite modest. $2 million a year would probably be sufficient to support most of the future objectives of the site: not only the maintenance and improvement of the existing forum as it scales, but also the creation of a similar project for each of the states and territories.<span class="footnote-reference" data-footnote-reference="" data-footnote-index="1" data-footnote-id="aq1upuv6w2f" role="doc-noteref" id="fnrefaq1upuv6w2f"><sup><a href="#fnaq1upuv6w2f">[1]</a></sup></span> We submit that this is a small investment with a massive potential benefit to the public at large.</p><p>The primary value of the Direct Democracy Forum is in its promotion of an informed and engaged democratic discourse [<a href="/about/argument-guidelines#Judgment">Judgment</a>]. As long as it is able to attract and keep a strong pool of engaged users, this forum should be able to provide a unique service in producing up-to-date information and analysis on what is actually going on in parliament. The feature of displaying links to other media on each forum should also allow this site to serve as a news distributor and aggregator, thus likely strengthening the broader ecosystem of political discourse. In general, encouraging citizens to engage with politics in terms of concrete policy issues should promote a more intelligent and civil political culture [<a href="/about/argument-guidelines#Judgment">Judgment</a>].</p><p>Among many other secondary benefits we might imagine, one is that this site could become a powerful gauge of public opinion that goes beyond the usual vague polling questions to actually build a map of what people think on a range of concrete policy issues.</p><ol class="footnote-section footnotes" data-footnote-section="" role="doc-endnotes"><li class="footnote-item" data-footnote-item="" data-footnote-index="1" data-footnote-id="aq1upuv6w2f" role="doc-endnote" id="fnaq1upuv6w2f"><span class="footnote-back-link" data-footnote-back-link="" data-footnote-id="aq1upuv6w2f"><sup><strong><a href="#fnrefaq1upuv6w2f">^</a></strong></sup></span><div class="footnote-content" data-footnote-content=""><p>My estimate based on an assumption that I leave my day job and hire a small team. Obviously more would be required to promote the site.</p></div></li></ol>
```

** Argument Against the Proposition that "The Government Should Grant Funding to the Direct Democracy Forum" **
```
<i>Normative Bases</i><ol><li><a href="/about/normative-bases#ValueNeutral">Value-Neutral / Epistemic Objection</a></li></ol><p>Let's grant that the Direct Democracy Forum is a good idea. Even if so, the forum is better off getting grassroots funding from its users. The forum does not <i>need</i> government funding. It should be able to get by on approximately 0 funding and can prosper with modest funding beyond that. <span class="footnote-reference" data-footnote-reference="" data-footnote-index="1" data-footnote-id="aq1upuv6w2e" role="doc-noteref" id="fnrefaq1upuv6w2e"><sup><a href="#fnaq1upuv6w2e">[1]</a></sup></span> If the forum gains sufficient popularity, one would expect donations to start trickling in. If the forum never reaches this stage, it probably never deserved government outlay either [<a href="/about/argument-guidelines#Judgment">Judgment</a>].</p><p>The other reason is this: while government funding doesn't necessarily imply direct government influence or a corrosion of independence, it inevitably creates some vectors of influence. There will always be the worry that if the forum upsets the current government because of, say, the harsh reception of some of its recent policies, funding may be curtailed [<a href="/about/argument-guidelines#Judgment">Judgment</a>].</p><ol class="footnote-section footnotes" data-footnote-section="" role="doc-endnotes"><li class="footnote-item" data-footnote-item="" data-footnote-index="1" data-footnote-id="aq1upuv6w2e" role="doc-endnote" id="fnaq1upuv6w2e"><span class="footnote-back-link" data-footnote-back-link="" data-footnote-id="aq1upuv6w2e"><sup><strong><a href="#fnrefaq1upuv6w2e">^</a></strong></sup></span><div class="footnote-content" data-footnote-content=""><p>Based on my estimate of ongoing maintenance requiring only a few hours of work per work, and costing a modest amount.</p></div></li></ol>
```

Take particular note of the formatting of the Normative Bases, and of the footnote syntax. If you want to include a footnote, you will need to follow this formatting precisely in your output. (Note that footnotes are not necessarily the preferred method of citation; quotes (using `<blockquote>`) or hyperlinks are perfectly good, depending on context.)


## Information about the Specific Bill
Each bill before the Australian parliament has an associated explanatory memo and/or bill digest, usually in PDF format. I have attached one or both of these to the curent request. These documents explain the purpose of the bill, what it seeks to change, and why. You will need to read through them carefully, as they will contain the information you need to fill out the fields described earlier.

For the "Detailed Summary" field and/or the argument fields, you may want to quote from the explanatory memo or bill digest associated with the bill. If you do so, please make sure to attribute and represent them as quotes, e.g. `From the explanatory memo: <blockquote>...</blockquote>`.

Paraphrasing can also be appropriate, in which case you can append something like "[Explanatory Memo page 10]" to the end of the sentence. Just don't cite the source as "OCR" (something I have seen in test outputs).

## Response Format
Respond with a JSON object with the following schema:
```
{
  "high_level_summary": "string",
  "detailed_summary": "string",
  "argument_for": "string",
  "argument_against": "string",
  "categories": ["string"]
}
```

The categories field should be a list of up to 3 items chosen from the following allowed set:
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

Do not render the JSON in markdown format, just return a JSON object directly with the above attributes.

## Your Response
"""
