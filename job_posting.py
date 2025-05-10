import pandas as pd

import pandas as pd

def search_job_postings_by_category(search_term: str) -> pd.DataFrame:
    try:
        # 엑셀 파일을 함수 내부에서 불러오기
        df = pd.read_excel("채용공고40_직종매칭.xlsx", engine="openpyxl")

        # 검색어가 포함된 행 필터링
        filtered_df = df[
            (df['top1'] == search_term) |
            (df['top2'] == search_term) |
            (df['top3'] == search_term)
        ]

        # 결과 추출
        result_df = filtered_df[['공고제목', '링크']].reset_index(drop=True)
        return result_df

    except FileNotFoundError:
        print("엑셀 파일이 존재하지 않습니다.")
        return pd.DataFrame()
    except Exception as e:
        print(f"예기치 못한 오류: {e}")
        return pd.DataFrame()

