import streamlit as st
from survey_questions import questions, category_names
from scoring import calculate_scores
from mbti_input import get_user_mbti
from ui import get_user_answers
from job_recom2 import calculate_job_satisfaction, convert_scores_to_series, recommend_jobs_by_mbti_only
from job_posting import search_job_postings_by_category
import pandas as pd

# 0. 파일 구조
file_path = "직업별_하이브리드3.xlsx"
mbti_file="mbti_job.xlsx"

try:
    job_df = pd.read_excel(file_path, engine='openpyxl')
    mbti_df = pd.read_excel(mbti_file, engine='openpyxl')
except Exception as e:
    st.error(f"❌ 파일 로딩 실패: {e}")
    st.stop()

# 1. ui 환경
st.title("[MBTI및 직무 성향을 고려한 커리어 제안]")
answers = []

user_mbti=get_user_mbti()
answers = get_user_answers(user_mbti)

# 2. 설문하기
if st.button("제출하기"):
    st.success("설문이 성공적으로 제출되었습니다!")
    category_scores = calculate_scores(answers, category_names)


    # 3. 모델 돌리기
    try:
        df = pd.read_excel(file_path, sheet_name='Sheet1', engine='openpyxl')
        trait_columns = df.columns[1:]  # 첫 열은 직업명

        trait_columns = job_df.columns[1:]
        user_traits = convert_scores_to_series(category_scores, trait_columns)

        # MBTI 기반 추천 직업 목록 추출
        mbti_jobs = recommend_jobs_by_mbti_only(job_df, mbti_df, user_mbti)

        results = calculate_job_satisfaction(df, user_traits)

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