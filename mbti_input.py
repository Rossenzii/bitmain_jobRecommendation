import streamlit as st
import base64
from pathlib import Path

def get_user_mbti():
    img_path = Path("bg4.jpg")
    if img_path.exists():
        st.image(str(img_path), use_column_width=True)
    else:
        st.error("bg2.jpg 이미지가 존재하지 않습니다.")

    # 이미지 아래 MBTI 안내 텍스트
    st.markdown("## 🧠 MBTI를 입력해주세요")
    st.write("MBTI는 성격을 기반으로 직업을 추천하는 데 사용됩니다.")

    # 선택박스
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        m1 = st.selectbox("에너지 방향", ["E", "I"], key="mbti1")
    with col2:
        m2 = st.selectbox("인식 방식", ["S", "N"], key="mbti2")
    with col3:
        m3 = st.selectbox("판단 기준", ["T", "F"], key="mbti3")
    with col4:
        m4 = st.selectbox("생활 양식", ["J", "P"], key="mbti4")

    mbti = m1 + m2 + m3 + m4
    return mbti
