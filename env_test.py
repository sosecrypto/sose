import streamlit as st
import os
import json

st.title("환경 변수 테스트")

# 환경 변수 확인
env_vars = os.environ
st.write(f"환경 변수 수: {len(env_vars)}")

# 특정 변수 확인
test_vars = ["ANTHROPIC_API_KEY", "NOTION_API_KEY", "NOTION_DATABASE_ID"]
for var in test_vars:
    if var in env_vars:
        value = env_vars[var]
        masked = value[:3] + "..." + value[-3:] if len(value) > 6 else "***"
        st.write(f"{var}: 설정됨 (값 미리보기: {masked}, 길이: {len(value)})")
    else:
        st.write(f"{var}: 설정되지 않음")

# 기타 환경 변수 확인 (보안 변수 제외)
st.subheader("기타 환경 변수")
safe_vars = {k: v for k, v in env_vars.items() if not any(x in k.lower() for x in ["key", "token", "secret", "password", "auth"])}
st.json(safe_vars) 