import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

# Load env (for local testing)
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

st.set_page_config(page_title="AskSnap", page_icon="📎")
st.title("📎 AskSnap")
st.caption("Structured info explorer powered by OpenAI")

# Session state
if "history" not in st.session_state:
    st.session_state.history = []
if "followups" not in st.session_state:
    st.session_state.followups = {}

def ask_snap(topic):
    prompt = f"""
You are a helpful assistant. The user will input a topic — typically a short phrase or keyword (like "pizza" or "Manchester United").

Your task is to provide structured, focused information in this format:

Topic: {topic}

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
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )

    return response.choices[0].message.content

# Input UI
topic = st.text_input("Enter a topic:", "")

if st.button("🔍 Explore Topic") and topic.strip():
    output = ask_snap(topic)
    st.session_state.history.append((topic, output))

# Follow-up buttons
for i, (topic, output) in enumerate(reversed(st.session_state.history[-1:])):
    st.markdown(f"### 🔎 Topic: `{topic}`")
    st.text(output)

    followups = {}
    for line in output.splitlines():
        if line.strip().startswith("1. Broader:"):
            followups["Broader"] = line.split(":", 1)[1].strip()
        elif line.strip().startswith("2. Related:"):
            followups["Related"] = line.split(":", 1)[1].strip()
        elif line.strip().startswith("3. Deeper:"):
            followups["Deeper"] = line.split(":", 1)[1].strip()

    st.session_state.followups = followups

    cols = st.columns(3)
    for idx, (label, follow_topic) in enumerate(followups.items()):
        with cols[idx]:
            if st.button(f"{label} 👉 {follow_topic}", key=f"{i}-{label}"):
                new_output = ask_snap(follow_topic)
                st.session_state.history.append((follow_topic, new_output))
                st.rerun()

