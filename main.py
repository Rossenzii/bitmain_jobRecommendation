import streamlit as st
from survey_questions import questions, category_names
from scoring import calculate_scores
from mbti_input import get_user_mbti
from ui import get_user_answers
from job_recom import calculate_job_satisfaction, convert_scores_to_series
from job_posting import search_job_postings_by_category
import pandas as pd

# 1. ui 환경
st.title("[직무 성향 설문지]")
answers = []

user_mbti=get_user_mbti()
answers = get_user_answers(user_mbti)

# 2. 설문하기
if st.button("제출하기"):
    st.success("설문이 성공적으로 제출되었습니다!")

    st.subheader("카테고리별 점수 (A 응답 기준)")
    category_scores = calculate_scores(answers, category_names)

    for cat, score in category_scores.items():
        st.write(f"{cat}: {score} / 2")

    # 3. 모델 돌리기
    file_path = "직업별_하이브리드3.xlsx"
    try:
        df = pd.read_excel(file_path, sheet_name='Sheet1', engine='openpyxl')
        trait_columns = df.columns[1:]  # 첫 열은 직업명

        # 사용자 입력 기반 추천
        user_traits = convert_scores_to_series(category_scores, trait_columns)
        results = calculate_job_satisfaction(df, user_traits)

        # ------------------------------------------
        st.markdown("## 📌 예상 직업만족도 상위 5개 추천 결과")
        st.markdown("---")
        st.dataframe(results.head(5), use_container_width=True)

        # ------------------------------------------
        st.markdown("## 📌 상위 3개 직업 관련 채용 공고")
        st.markdown("---")

        top_jobs = results['직업명'].head(3).tolist()

        for job in top_jobs:
            with st.expander(f"🔍 {job} 관련 공고 보기", expanded=True):
                postings = search_job_postings_by_category(job)

                if not postings.empty:
                    for _, row in postings.iterrows():
                        st.markdown(f"- [{row['공고제목']}]({row['링크']})")
                else:
                    st.write("❗ 관련 공고가 없습니다.")

    except Exception as e:
        st.error(f"❌ 직업 추천을 위해 엑셀 파일을 불러오지 못했습니다: {e}")