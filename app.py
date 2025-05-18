import streamlit as st
import json
import os

# 전역 변수 초기화
ANTHROPIC_AVAILABLE = False
NOTION_AVAILABLE = False

# 세션 상태 초기화
if "analyzed_data" not in st.session_state:
    st.session_state.analyzed_data = None

# 페이지 설정 및 타이틀
st.set_page_config(
    page_title="클로바 노트 → 노션 회의록 변환기",
    page_icon="📝",
    layout="wide"
)

# 앱 타이틀 및 설명
st.title("📝 클로바 노트 → 노션 회의록 변환기")
st.markdown("클로바 노트의 회의록 텍스트를 노션 회의록 템플릿에 자동으로 등록하는 서비스입니다.")

# 모듈 가져오기 시도 (오류 처리 추가)
try:
    from claude_analyzer import analyze_meeting_notes_with_claude
    ANTHROPIC_AVAILABLE = True
except Exception as e:
    st.error(f"Claude 모듈 로딩 중 오류 발생: {e}")
    st.info("API 키 설정을 확인하거나 관리자에게 문의하세요.")

try:
    from notion_connector import add_meeting_notes_to_notion
    NOTION_AVAILABLE = True
except Exception as e:
    st.error(f"Notion 모듈 로딩 중 오류 발생: {e}")
    st.info("API 키 설정을 확인하거나 관리자에게 문의하세요.")

# 환경 변수 확인
api_status = {}
for key in ["ANTHROPIC_API_KEY", "NOTION_API_KEY", "NOTION_DATABASE_ID"]:
    # 보안을 위해 키 값 자체는 표시하지 않음
    api_status[key] = "설정됨" if os.environ.get(key) else "설정되지 않음"

# 사이드바 정보
with st.sidebar:
    st.header("📋 사용 방법")
    st.markdown("""
    1. 클로바 노트의 회의록 텍스트를 왼쪽 텍스트 영역에 붙여넣기
    2. '회의록 분석 및 노션에 등록' 버튼 클릭
    3. 분석 결과와 노션 URL 확인
    """)
    
    st.header("🔍 분석 항목")
    st.markdown("""
    - 회의 리드
    - 참석자
    - 일자
    - 회의 목적
    - 회의 아젠다
    - 주요 논의 내용
    - 주요 결정 사항
    - 후속 액션
    - 회의 피드백
    - 다음 회의 일정
    """)
    
    # API 상태 표시 (디버깅용)
    st.header("🔧 시스템 상태", help="시스템 구성 요소의 상태를 표시합니다")
    st.markdown(f"**Claude API**: {'✅ 사용 가능' if ANTHROPIC_AVAILABLE else '❌ 사용 불가'}")
    st.markdown(f"**Notion API**: {'✅ 사용 가능' if NOTION_AVAILABLE else '❌ 사용 불가'}")
    
    # 환경 변수 상태 표시
    st.expander("API 키 상태", expanded=False).markdown(
        f"""
        - ANTHROPIC_API_KEY: {api_status['ANTHROPIC_API_KEY']}
        - NOTION_API_KEY: {api_status['NOTION_API_KEY']}
        - NOTION_DATABASE_ID: {api_status['NOTION_DATABASE_ID']}
        """
    )

# 기능 사용 가능 여부 확인
service_available = ANTHROPIC_AVAILABLE and NOTION_AVAILABLE

# 메인 컨텐츠 영역
col1, col2 = st.columns([3, 2])

with col1:
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
    
    # 분석 및 등록 버튼
    button_disabled = not service_available
    
    if button_disabled:
        st.warning("서비스 구성 요소가 올바르게 로드되지 않아 회의록 분석 기능을 사용할 수 없습니다.")
    
    if st.button("회의록 분석 및 노션에 등록", type="primary", use_container_width=True, disabled=button_disabled):
        if not meeting_text.strip():
            st.error("회의록 텍스트를 입력해주세요.")
        else:
            with st.spinner("회의록 분석 중..."):
                try:
                    # 1. Claude로 회의록 분석
                    analysis_result = analyze_meeting_notes_with_claude(meeting_text)
                    
                    if not analysis_result:
                        st.error("회의록 분석에 실패했습니다.")
                    else:
                        try:
                            # 2. JSON 분석 결과 파싱
                            meeting_data = json.loads(analysis_result)
                            st.success("회의록 분석 완료!")
                            
                            # 세션 상태에 분석 결과 저장
                            st.session_state.analyzed_data = meeting_data
                            
                            # 3. Notion에 회의록 등록
                            with st.spinner("노션에 회의록 등록 중..."):
                                try:
                                    page_id = add_meeting_notes_to_notion(meeting_data)
                                    
                                    if page_id:
                                        notion_url = f"https://notion.so/{page_id.replace('-', '')}"
                                        st.success(f"노션에 회의록이 성공적으로 등록되었습니다!")
                                        st.markdown(f"[노션에서 회의록 보기]({notion_url})")
                                    else:
                                        st.error("노션 회의록 등록에 실패했습니다.")
                                except Exception as e:
                                    st.error(f"노션 등록 중 오류 발생: {e}")
                                    st.info("JSON 분석 결과:")
                                    st.json(meeting_data)
                                    
                        except json.JSONDecodeError as e:
                            st.error(f"분석 결과를 JSON으로 파싱하는 중 오류 발생: {e}")
                            st.text("원본 응답:")
                            st.code(analysis_result)
                except Exception as e:
                    st.error(f"회의록 분석 중 예상치 못한 오류 발생: {e}")

with col2:
    st.header("분석 결과")
    
    # 처음에는 안내 메시지 표시
    if not st.session_state.get("analyzed_data"):
        st.info("왼쪽에 회의록 텍스트를 입력하고 분석 버튼을 클릭하면 결과가 여기에 표시됩니다.")
    else:
        # 분석 결과가 있으면 표시
        analyzed_data = st.session_state.get("analyzed_data")
        
        # 일반 정보 표시
        st.subheader("기본 정보")
        st.markdown(f"**회의 제목:** {analyzed_data.get('회의 제목', '정보 없음')}")
        st.markdown(f"**일시:** {analyzed_data.get('일자', '정보 없음')}")
        st.markdown(f"**진행자:** {analyzed_data.get('회의 리드', '정보 없음')}")
        st.markdown(f"**참석자:** {analyzed_data.get('참석자', '정보 없음')}")
        
        # 아젠다 정보 표시
        st.subheader("회의 아젠다")
        agenda_items = analyzed_data.get("회의 아젠다", [])
        if agenda_items:
            for i, item in enumerate(agenda_items):
                if isinstance(item, dict):
                    st.markdown(f"**{i+1}. {item.get('항목 제목', '')}**")
                    if item.get('소요시간'):
                        st.markdown(f"소요시간: {item['소요시간']}")
                else:
                    st.markdown(f"**{i+1}. {item}**")
        else:
            st.markdown("아젠다 정보 없음")
        
        # 결정 사항 표시
        st.subheader("주요 결정 사항")
        decisions = analyzed_data.get("주요 결정 사항", [])
        if decisions:
            for i, decision in enumerate(decisions):
                if isinstance(decision, dict) and "제목" in decision:
                    st.markdown(f"**{i+1}. {decision['제목']}**")
                    if decision.get("세부 내용"):
                        st.markdown(f"   {decision['세부 내용']}")
                else:
                    st.markdown(f"**{i+1}. {decision}**")
        else:
            st.markdown("결정 사항 정보 없음")
        
        # 액션 아이템 표시
        st.subheader("후속 액션")
        actions = analyzed_data.get("후속 액션", [])
        if actions:
            for i, action in enumerate(actions):
                st.markdown(f"**{i+1}.** {action}")
        else:
            st.markdown("후속 액션 정보 없음")

# 앱 실행 방법 안내 (로컬 실행 시에만 표시)
if os.environ.get("STREAMLIT_DEPLOYMENT") != "cloud":
    st.markdown("---")
    st.markdown("### 앱 실행 방법")
    st.code("streamlit run app.py") 