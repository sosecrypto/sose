# 회의록 변환기 (Meeting Notes Converter)

클로바 노트에 기록된 회의 내용을 분석하여 노션 회의록 템플릿에 자동으로 등록하고 슬랙으로 알림을 보내는 웹 애플리케이션입니다.

## 기능

- 회의록 텍스트 분석 (Claude API 활용)
- 노션 데이터베이스에 자동 등록
- 웹 인터페이스를 통한 간편한 사용
- 회의 제목, 참석자, 안건, 결정사항, 액션 아이템 등 자동 추출
- (예정) 슬랙 알림 기능

## 설치 및 실행 방법

### 로컬 환경에서 실행

1. 저장소 클론
   ```
   git clone https://github.com/sosecrypto/sose.git
   cd sose
   ```

2. 필요한 패키지 설치
   ```
   pip install -r requirements.txt
   ```

3. 환경 변수 설정
   - `.env` 파일 생성:
     ```
     ANTHROPIC_API_KEY=your_anthropic_api_key
     NOTION_API_KEY=your_notion_api_key
     NOTION_DATABASE_ID=your_notion_database_id
     ```

4. 애플리케이션 실행
   ```
   streamlit run app.py
   ```

### Streamlit Cloud에서 실행

1. GitHub 저장소와 Streamlit Cloud 연결
2. 다음 환경 변수 설정 (Streamlit Cloud 대시보드의 Secrets 섹션):
   ```toml
   [general]
   ANTHROPIC_API_KEY = "your_anthropic_api_key"
   NOTION_API_KEY = "your_notion_api_key"
   NOTION_DATABASE_ID = "your_notion_database_id"
   ```

## API 키 획득 방법

### Anthropic API 키
1. [Anthropic Console](https://console.anthropic.com/)에 가입
2. API 키 발급 (Claude API 사용을 위함)

### Notion API 키
1. [Notion Developers](https://developers.notion.com/)에서 통합 생성
2. 통합을 회의록 데이터베이스에 연결
3. API 키 및 데이터베이스 ID 획득

## 사용 방법

1. 웹 인터페이스에서 회의록 텍스트 입력
2. "회의록 분석 및 노션에 등록" 버튼 클릭
3. 분석 결과와 노션 URL 확인

## 문제 해결

API 키 관련 문제가 발생하면:
1. 환경 변수가 올바르게 설정되었는지 확인
2. API 키 값이 정확한지 확인
3. Notion 통합이 데이터베이스에 접근 권한이 있는지 확인

## 라이센스

MIT 