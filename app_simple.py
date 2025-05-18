import streamlit as st

# 페이지 설정 및 타이틀
st.set_page_config(
    page_title="클로바 노트 → 노션 회의록 변환기",
    page_icon="📝"
)

# 앱 타이틀 및 설명
st.title("📝 클로바 노트 → 노션 회의록 변환기")
st.markdown("클로바 노트의 회의록 텍스트를 노션 회의록 템플릿에 자동으로 등록하는 서비스입니다.")

# 텍스트 입력 영역
st.header("회의록 텍스트 입력")
meeting_text = st.text_area(
    "클로바 노트의 회의록 텍스트를 아래에 붙여넣으세요:",
    height=400,
    placeholder="""예시:
회의 제목: 2024년 2분기 신제품 개발 회의
날짜: 2024년 4월 10일 오후 2시
참석자: 이대표, 김팀장, 박연구원, 최디자이너

주요 안건:
1. 신제품 '알파' 프로토타입 리뷰
2. 출시 일정 및 마케팅 전략 논의
...
    """
)

# 분석 버튼 (실제 기능은 없음)
if st.button("회의록 분석하기", type="primary"):
    st.success("현재 데모 버전입니다. API 키 설정 후 실제 분석 기능이 활성화됩니다.")
    
# 환경 변수 상태 표시 (단순화된 버전)
st.markdown("---")
st.markdown("### 시스템 상태")
st.info("아직 API 키가 설정되지 않았습니다. Streamlit Cloud의 Secrets 설정에서 API 키를 설정해주세요.") 