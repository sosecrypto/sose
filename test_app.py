import streamlit as st
import os

# 페이지 설정 및 타이틀
st.set_page_config(page_title="테스트 앱", page_icon="🧪")

# 앱 타이틀
st.title("🧪 간단한 테스트 앱")
st.markdown("이 앱은 Streamlit Cloud가 제대로 작동하는지 확인하기 위한 테스트 앱입니다.")

# 환경 변수 확인
env_vars = ["ANTHROPIC_API_KEY", "NOTION_API_KEY", "NOTION_DATABASE_ID"]
for var in env_vars:
    value = os.environ.get(var)
    status = "✅ 설정됨" if value else "❌ 설정되지 않음"
    st.write(f"**{var}**: {status}")

# 간단한 상호작용 요소 추가
name = st.text_input("이름을 입력하세요:")
if name:
    st.write(f"안녕하세요, {name}님!")

# 버튼 추가
if st.button("클릭해보세요"):
    st.success("버튼이 잘 작동합니다!")
    st.balloons() 