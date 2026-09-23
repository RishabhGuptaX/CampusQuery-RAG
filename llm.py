import os

from dotenv import load_dotenv
from groq import Groq


# ============================================================
# CAMPUSQUERY — LLM MODULE
# ============================================================

# Load variables from .env
load_dotenv()


# ============================================================
# API CONFIGURATION
# ============================================================

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError(
        "GROQ_API_KEY not found.\n"
        "Please make sure your .env file contains:\n"
        "GROQ_API_KEY=your_api_key"
    )


# Create Groq client
client = Groq(api_key=api_key)


# Current Groq model
MODEL_NAME = "openai/gpt-oss-20b"


# ============================================================
# GENERATE ANSWER
# ============================================================

def generate_answer(question, context):

    prompt = f"""
You are CampusQuery, an AI assistant for VIT-AP University students.

Your job is to answer the student's question using ONLY the
information provided in the retrieved college documents.

IMPORTANT RULES:

1. Use only the provided context.
2. Do not invent information.
3. Do not use outside knowledge.
4. If the answer cannot be found in the context, say:
   "I couldn't find this information in the available college documents."
5. Give a clear and concise answer.
6. Preserve important dates, timings, course codes, locations,
   and other specific information from the documents.
7. Do not mention information that is not supported by the context.

Retrieved Context:
--------------------------------------------------
{context}
--------------------------------------------------

Student Question:
{question}

Answer:
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,

        messages=[
            {
                "role": "system",
                "content": (
                    "You are CampusQuery, a college information "
                    "assistant. Answer strictly using the provided "
                    "retrieved documents."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],

        temperature=0.1,
    )

    return response.choices[0].message.content


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    question = "When is CAT-1 scheduled?"

    context = """
    The Continuous Assessment Test - 1 (CAT-1) for courses
    offered during the Fall Semester 2026-27 is scheduled
    from 17th to 24th August 2026.

    The examinations are conducted offline in designated
    examination halls.
    """

    answer = generate_answer(
        question,
        context
    )

    print("\n" + "=" * 60)
    print("🤖 CAMPUSQUERY")
    print("=" * 60)

    print(answer)

    print("=" * 60)