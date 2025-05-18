import streamlit as st
import os
import toml

# 페이지 설정 및 타이틀
st.set_page_config(page_title="환경 변수 디버그", page_icon="🔍")

# 앱 타이틀
st.title("🔍 환경 변수 디버그 앱")
st.markdown("이 앱은 Streamlit Cloud의 환경 변수 설정을 디버깅하기 위한 도구입니다.")

# 환경 변수 상태 및 값 확인
st.header("환경 변수 상태")

# API 키 확인 (보안을 위해 일부만 표시)
env_vars = ["ANTHROPIC_API_KEY", "NOTION_API_KEY", "NOTION_DATABASE_ID"]
for var in env_vars:
    value = os.environ.get(var, "")
    status = "✅ 설정됨" if value else "❌ 설정되지 않음"
    
    st.write(f"**{var}**: {status}")
    
    # 값이 있으면 처음 5자와 길이 표시 (보안을 위해 전체 키는 표시하지 않음)
    if value:
        masked_value = value[:5] + "..." + value[-3:] if len(value) > 8 else value
        st.code(f"길이: {len(value)}자, 미리보기: {masked_value}")

# TOML 예시 표시
st.header("올바른 설정 방법")
st.markdown("""
Streamlit Cloud의 Secrets는 TOML 형식으로 작성해야 합니다:
""")

example_toml = """
[general]
ANTHROPIC_API_KEY = "sk-ant-api03-xxxYOUR_ACTUAL_KEYxxx"
NOTION_API_KEY = "secret_xxxYOUR_ACTUAL_KEYxxx"
NOTION_DATABASE_ID = "ntn_xxxYOUR_ACTUAL_IDxxx"
"""
st.code(example_toml, language="toml")

st.markdown("""
주의사항:
- `[general]` 섹션이 반드시 있어야 합니다
- 문자열은 큰따옴표(`"`)로 감싸야 합니다
- 값에 따옴표나 특수문자가 있다면 이스케이프 처리가 필요할 수 있습니다
- 각 줄 사이에 공백 줄이 없어야 합니다
""")

# 테스트 입력 필드
st.header("TOML 검증기")
user_toml = st.text_area("TOML 형식을 여기에 붙여넣어 검증하세요:", height=200)

if st.button("검증하기"):
    if user_toml:
        try:
            parsed = toml.loads(user_toml)
            st.success("✅ 유효한 TOML 형식입니다!")
            st.json(parsed)
        except Exception as e:
            st.error(f"❌ TOML 파싱 오류: {e}")
    else:
        st.warning("TOML을 입력해주세요.") 