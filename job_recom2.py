import pandas as pd
from sklearn.preprocessing import normalize

# MBTI 기반 직업 추천 목록 필터링
def recommend_jobs_by_mbti_only(df, mbti_df, mbti_input):
    mbti_jobs = mbti_df.loc[mbti_df['MBTI'] == mbti_input, '직업']
    if mbti_jobs.empty:
        return []

    job_list = [job.strip() for job in mbti_jobs.values[0].split(',')]
    return job_list

# 사용자 성격 점수 (dict) → pandas Series 변환
def convert_scores_to_series(category_scores, trait_columns):
    return pd.Series({trait: category_scores.get(trait, 0) for trait in trait_columns})

# 직업 만족도 계산
def calculate_job_satisfaction(df, user_traits, mbti_job_list=None):
    trait_columns = df.columns[1:]

    # MBTI 기반으로 직업 필터링
    if mbti_job_list:
        df = df[df['직업명'].isin(mbti_job_list)].copy()
        if df.empty:
            return pd.DataFrame({'직업명': [], '예상직업만족도': []})

    # L2 정규화
    trait_matrix = df[trait_columns].values
    normalized_matrix = normalize(trait_matrix, axis=1)
    df_l2_normalized = pd.DataFrame(normalized_matrix, columns=trait_columns)
    df_l2_normalized.insert(0, '직업명', df.iloc[:, 0])

    # 만족도 점수 계산
    scores = df_l2_normalized[trait_columns].multiply(user_traits, axis=1).sum(axis=1)
    results = pd.DataFrame({
        '직업명': df_l2_normalized['직업명'],
        '예상직업만족도': scores
    }).sort_values(by='예상직업만족도', ascending=False).reset_index(drop=True)

    return results

