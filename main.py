import spacy
import re
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

# Load English tokenizer, tagger, parser and NER
nlp = spacy.load("en_core_web_sm")

# Configure the Google Generative AI API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)


def rephrase_with_gemini(requirement):
    """Rephrases the requirement using Google's Gemini model."""
    model = genai.GenerativeModel("gemini-2.0-flash")  # Specify the model
    prompt = (
        f"Rephrase the following software requirement from the perspective of "
        f"the system. Focus on what the system *will do*, not what the user wants. "
        f"Requirement: {requirement}\n"
        f"Rephrased Requirement (System's Perspective): "
    )

    try:
        response = model.generate_content(prompt)
        rephrased_requirement = response.text.strip()
        return rephrased_requirement
    except Exception as e:
        print(f"Error calling Google Generative AI API: {e}")
        return requirement  # Return the original if API call fails


# Read text from the file
try:
    with open("./text.txt", "r") as file:
        text = file.read()
except FileNotFoundError:
    print("Error: 'text.txt' not found in the subdirectory.")
    exit()

doc = nlp(text)

# Extract the numbered requirements sections
requirement_sections = re.findall(r'\d+\.\s+(.*?)(?=\d+\.|$)', text, re.DOTALL)

# Extract functional requirements
functional_requirements = []
req_id = 1

# Process each section to extract functional requirements
for section in requirement_sections:
    # Split into potential sub-requirements
    section = section.strip()

    # Skip if section is empty
    if not section:
        continue

    # Check if there are sub-requirements (a., b., etc.)
    sub_requirements = re.findall(r'([a-z]\.\s+.*?)(?=[a-z]\.|$)', section, re.DOTALL)

    if sub_requirements:
        # Process sub-requirements
        for sub_req in sub_requirements:
            sub_req_doc = nlp(sub_req.strip())
            for sent in sub_req_doc.sents:
                if "should" in sent.text or "must" in sent.text or "will" in sent.text:
                    rephrased_requirement = rephrase_with_gemini(sent.text.strip())
                    functional_requirements.append(f"FR{req_id}: {rephrased_requirement}")
                    req_id += 1

        # Process the main section text for requirements
        section_doc = nlp(section)
        for sent in section_doc.sents:
            if "should" in sent.text or "must" in sent.text or "will" in sent.text:
                # Skip if this is likely a sub-requirement that we've already processed
                if not any(sub_req in sent.text for sub_req in sub_requirements):
                    rephrased_requirement = rephrase_with_gemini(sent.text.strip())
                    functional_requirements.append(f"FR{req_id}: {rephrased_requirement}")
                    req_id += 1


# Print extracted functional requirements
print("FUNCTIONAL REQUIREMENTS (SYSTEM VIEW - Gemini):")
print("=" * 70)
for req in functional_requirements:
    print(req)
