from app_func import ask_ai
import sqlite3
import streamlit as st

conn = sqlite3.connect("../sql/final_marketing.db", check_same_thread=False)

# Initialize memory
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("📊 AI Data Analyst")

question = st.text_input("Ask your question:")

# Clear chat button
if st.button("🧹 Clear Chat"):
    st.session_state.chat_history = []

if st.button("Run"):

    if question:

        try:
            # Pass history to function
            sql, df, explanation = ask_ai(
                question,
                conn,
                st.session_state.chat_history
            )

            # Store in memory
            st.session_state.chat_history.append({
                "question": question,
                "sql": sql,
                "answer": explanation
            })

            st.subheader("🧠 Generated SQL")
            st.code(sql, language="sql")

            st.subheader("📊 Query Result")
            st.dataframe(df)

            st.subheader("🤖 AI Answer")
            st.write(explanation)

        except Exception as e:
            st.error(e)

# Show conversation history
st.subheader("💬 Conversation History")

for chat in st.session_state.chat_history[::-1]:
    st.markdown(f"**Q:** {chat['question']}")
    st.markdown(f"**A:** {chat['answer']}")
    st.markdown("---")