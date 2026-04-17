from app_func import ask_ai
import sqlite3
import streamlit as st

# Page config
st.set_page_config(page_title="AI Data Analyst", layout="wide")

# DB connection
conn = sqlite3.connect("../sql/final_marketing.db", check_same_thread=False)

# Memory
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("📊 AI Data Analyst")

with st.form(key="chat_form"):
    input_col, btn_col1, btn_col2 = st.columns([6,1,1])

    with input_col:
        question = st.text_input(
            "", 
            placeholder="Type your question..."
        )

    with btn_col1:
        st.markdown("<br>", unsafe_allow_html=True)
        submit = st.form_submit_button("▶ Run")

    with btn_col2:
        st.markdown("<br>", unsafe_allow_html=True)
        clear = st.form_submit_button("🧹 Clear")

if clear:
    st.session_state.chat_history = []

if submit and question:
    try:
        sql, df, explanation = ask_ai(
            question,
            conn,
            st.session_state.chat_history
        )

        # Save chat
        st.session_state.chat_history.append({
            "question": question,
            "sql": sql,
            "answer": explanation
        })

        st.markdown("### 🧠 Generated SQL")
        st.code(sql, language="sql")

        st.markdown("### 📊 Query Result")
        st.dataframe(df, use_container_width=True)

        st.markdown("### 🤖 AI Answer")
        st.write(explanation)

    except Exception as e:
        st.error(e)

if len(st.session_state.chat_history) > 0:

    st.markdown("---")
    st.subheader("💬 Conversation History")

    for chat in st.session_state.chat_history[::-1]:
        st.markdown(f"""
        <div style='background:#1e293b; padding:12px; border-radius:10px; margin-bottom:10px'>
        <b>🧑 You:</b><br>{chat['question']}
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style='background:#0f172a; padding:12px; border-radius:10px; margin-bottom:20px'>
        <b>🤖 AI:</b><br>{chat['answer']}
        </div>
        """, unsafe_allow_html=True)
