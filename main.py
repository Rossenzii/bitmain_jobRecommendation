# main.py
import streamlit as st
from survey_questions import questions, category_names
from scoring import calculate_scores
from ui import get_user_answers
from job_recom import calculate_job_satisfaction, convert_scores_to_series
import pandas as pd


st.title("직무 성향 설문지")
answers = []
st.write("각 질문에 대해 본인의 성향에 가까운 답변을 선택하세요.")

# ui 환경
answers = get_user_answers()


if st.button("제출하기"):
    st.success("설문이 성공적으로 제출되었습니다!")

    st.subheader("카테고리별 점수 (A 응답 기준)")
    category_scores = calculate_scores(answers, category_names)

    for cat, score in category_scores.items():
        st.write(f"{cat}: {score} / 2")

    # 엑셀 파일 불러오기
    file_path = "직업별_하이브리드2.xlsx"
    try:
        df = pd.read_excel(file_path, sheet_name='Sheet1', engine='openpyxl')
        trait_columns = df.columns[1:]  # 첫 열은 직업명

        #  사용자 입력 변환 후 직업 추천
        user_traits = convert_scores_to_series(category_scores, trait_columns)
        results = calculate_job_satisfaction(df, user_traits)

        st.subheader("📌 예상 직업만족도 상위 5개 추천 결과")
        st.dataframe(results.head(5))
    except Exception as e:
        st.error(f"직업 추천을 위해 엑셀 파일을 불러오지 못했습니다: {e}")

