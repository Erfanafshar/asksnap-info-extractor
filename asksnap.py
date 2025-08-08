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

1. Provide a 1-line summary of the topic.
2. Provide 3 to 5 key points in bullet format.
3. Suggest 3 follow-up topics:
   - One BROADER (more general)
   - One RELATED (same level, same context)
   - One DEEPER (more detailed or niche)

Use this format exactly:

Topic: {question}

Summary:
...

Key Points:
- ...
- ...
- ...

Follow-up Suggestions:
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
