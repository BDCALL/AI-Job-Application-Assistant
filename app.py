import streamlit as st
import requests

st.title("🤖 AI Job Application Assistant")

# Chat memory
if "messages" not in st.session_state:
    st.session_state.messages = []

if "score" not in st.session_state:
    st.session_state.score = None

# Upload
cv_file = st.file_uploader("Upload CV", type="pdf")
job_file = st.file_uploader("Upload Job Description", type="pdf")

# Setup backend
if st.button("Setup") and cv_file and job_file:
    with open("data/temp_cv.pdf", "wb") as f:
        f.write(cv_file.read())

    with open("data/temp_job.pdf", "wb") as f:
        f.write(job_file.read())

    res = requests.post("http://localhost:8000/setup")
    data = res.json()

    st.session_state.score = data.get("score")

    st.success("Backend Ready 🚀")

# Show score
if st.session_state.score is not None:
    st.subheader("📊 Fit Score")
    st.progress(st.session_state.score / 100)
    st.write(f"{st.session_state.score}/100")

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Chat input
if prompt := st.chat_input("Ask about your CV & Job"):

    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Call backend
    res = requests.post(
        "http://localhost:8000/ask",
        json={"question": prompt}
    )

    data = res.json()

    # Handle errors
    if "error" in data:
        response = f"❌ Error: {data['error']}"
    else:
        response = data.get("answer", "")
        mode = data.get("mode", "chat")

        # Optional: show mode
        if mode == "career":
            response = "🧠 **Career Mode**\n\n" + response
        else:
            response = "💬 **Chat Mode**\n\n" + response

    # Save + display assistant message
    st.session_state.messages.append({"role": "assistant", "content": response})

    with st.chat_message("assistant"):
        st.write(response)