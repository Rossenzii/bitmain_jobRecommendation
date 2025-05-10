# # job_recom.py
# import pandas as pd
# from sklearn.preprocessing import normalize

# def calculate_job_satisfaction(df, user_traits):
#     # 성격 특성 열만 추출
#     trait_columns = df.columns[1:]  # 첫 열은 직업명
#     trait_matrix = df[trait_columns].values

#     # L2 정규화 수행
#     normalized_matrix = normalize(trait_matrix, axis=1)
#     df_l2_normalized = pd.DataFrame(normalized_matrix, columns=trait_columns)
#     df_l2_normalized.insert(0, '직업명', df.iloc[:, 0])

#     # 만족도 계산
#     scores = df_l2_normalized[trait_columns].multiply(user_traits, axis=1).sum(axis=1)
#     results = pd.DataFrame({
#         '직업명': df_l2_normalized['직업명'],
#         '예상직업만족도': scores
#     }).sort_values(by='예상직업만족도', ascending=False).reset_index(drop=True)
#     return results

# # 설문 점수(dict) → Series로 변환
# def convert_scores_to_series(category_scores, trait_columns):
#     user_input = {}
#     for trait in trait_columns:
#         if trait in category_scores:
#             user_input[trait] = category_scores[trait]
#         else:
#             # 엑셀에는 있지만 설문에는 없는 항목 → 0점 처리
#             user_input[trait] = 0
#     return pd.Series(user_input)


import pandas as pd
from sklearn.preprocessing import normalize

# 엑셀 trait → 설문 category 매핑
trait_to_category = {
    "성취": "성취/노력",
    "노력": "성취/노력",
    "인내심": "인내",
    "끈기": "인내",
    "진취성": "책임성과 진취성",
    "책임감": "책임성과 진취성",
    "리더십": "리더십",
    "협력": "협조",
    "배려": "타인에 대한 배려",
    "사회성": "사회성",
    "자기조절": "자기통제",
    "스트레스 내성": "스트레스 감내성",
    "융통성": "적응성/융통성",
    "성실성": "신뢰성",
    "계획성": "꼼꼼함",
    "정직성": "정직성",
    "독립성": "독립성",
    "창의성": "혁신",
    "분석력": "분석적 사고"
}

# 사용자 점수 변환
def convert_scores_to_series(category_scores, trait_columns):
    user_input = {}
    for trait in trait_columns:
        if trait in trait_to_category:
            category = trait_to_category[trait]
            user_input[trait] = category_scores.get(category, 0)
        else:
            user_input[trait] = 0
    return pd.Series(user_input)

# 만족도 계산
def calculate_job_satisfaction(df, user_traits):
    trait_columns = df.columns[1:]
    trait_matrix = df[trait_columns].values
    normalized_matrix = normalize(trait_matrix, axis=1)
    df_l2_normalized = pd.DataFrame(normalized_matrix, columns=trait_columns)
    df_l2_normalized.insert(0, '직업명', df.iloc[:, 0])

    scores = df_l2_normalized[trait_columns].multiply(user_traits, axis=1).sum(axis=1)
    results = pd.DataFrame({
        '직업명': df_l2_normalized['직업명'],
        '예상직업만족도': scores
    }).sort_values(by='예상직업만족도', ascending=False).reset_index(drop=True)
    return results
