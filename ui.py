# ui.py
import streamlit as st
from survey_questions import questions

# 실제
# for idx, (q, a1, a2) in enumerate(questions):
#     response = st.radio(
#         f"Q{idx + 1}. {q}",
#         [f"A. {a1}", f"B. {a2}"],
#         key=f"radio_{idx + 1}"
#     )
#     answers.append(response)

# test용
def get_user_answers():
    if "preset" not in st.session_state:
        st.session_state.preset = None

    st.write("각 질문에 대해 본인의 성향에 가까운 답변을 선택하세요.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ 모두 A로 설정"):
            st.session_state.preset = "A"
    with col2:
        if st.button("❌ 모두 B로 설정"):
            st.session_state.preset = "B"

    answers = []
    for idx, (q, a1, a2) in enumerate(questions):
        default = (
            f"A. {a1}" if st.session_state.preset == "A"
            else f"B. {a2}" if st.session_state.preset == "B"
            else None
        )
        response = st.radio(
            f"Q{idx + 1}. {q}",
            [f"A. {a1}", f"B. {a2}"],
            index=0 if default == f"A. {a1}" else 1 if default == f"B. {a2}" else 0,
            key=f"radio_{idx + 1}"
        )
        answers.append(response)

    return answers