from openai import OpenAI
from dotenv import load_dotenv
import os

# Create OpenAI client with your API key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def ask_snap(question, topic_type="general"):
    prompt = f"""
You are a helpful assistant. The user is asking about a topic.
Extract:
1. A 1-line summary
2. 3–5 bullet points about the topic, focusing on {topic_type}.

Topic: {question}
"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
    )

    return response.choices[0].message.content


def main():
    print("🧠 AskSnap — LLM Info Assistant (type 'exit' to quit)")
    while True:
        user_input = input("AskSnap > ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        answer = ask_snap(user_input)
        print("\n" + answer + "\n")


if __name__ == "__main__":
    main()
