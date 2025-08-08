from openai import OpenAI
from dotenv import load_dotenv
import os

# Create OpenAI client with your API key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def ask_snap(question, topic_type="general"):
    prompt = f"""
    You are a helpful assistant. The user will input a topic — typically a short phrase or keyword (like "pizza" or "Manchester United").

    Your task is to provide structured, focused information in this format:

    Topic: {question}

    Summary:
    Write a 1- to 2-line summary of the topic. Do NOT make it personal or speculative.

    Key Points:
    - Include 3 to 5 short, factual bullet points.
    - Keep them general and informative.
    - No opinions, speculation, or deep personalization.

    Follow-up Suggestions:
    Suggest 3 related topics as short phrases — NOT full questions or sentences.

    1. Broader: ...
    2. Related: ...
    3. Deeper: ...
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # or 'gpt-4o'
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
    )

    return response.choices[0].message.content


def main():
    print("🧠 AskSnap — LLM Info Assistant (type 'exit' to quit)")
    last_followups = {}

    while True:
        user_input = input("AskSnap > ").strip()

        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        # Check if user typed a number for follow-up
        if user_input in ["1", "2", "3"] and last_followups:
            followup_topic = last_followups.get(user_input)
            if followup_topic:
                print(f"\n🔁 Exploring follow-up: {followup_topic}")
                user_input = followup_topic
            else:
                print("⚠️ Invalid follow-up number. Ask a new question.")
                continue

        result = ask_snap(user_input)

        print("\n" + result + "\n")

        # Extract follow-up lines from output
        last_followups = {}
        for line in result.splitlines():
            if line.strip().startswith("1. Broader:"):
                last_followups["1"] = line.split(":", 1)[1].strip()
            elif line.strip().startswith("2. Related:"):
                last_followups["2"] = line.split(":", 1)[1].strip()
            elif line.strip().startswith("3. Deeper:"):
                last_followups["3"] = line.split(":", 1)[1].strip()


if __name__ == "__main__":
    main()
