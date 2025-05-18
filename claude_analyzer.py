import anthropic
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# Anthropic API 키 가져오기
API_KEY = os.environ.get("ANTHROPIC_API_KEY")

if not API_KEY:
    print("Anthropic API 키가 설정되지 않았습니다.")
    print("환경 변수 ANTHROPIC_API_KEY를 설정하거나 .env 파일에 추가해주세요.")
    exit()

# Claude 클라이언트 초기화
try:
    client = anthropic.Anthropic(api_key=API_KEY)
    print("Claude 클라이언트가 성공적으로 초기화되었습니다.")
except Exception as e:
    print(f"Claude 클라이언트 초기화 중 오류 발생: {e}")
    exit()

# 회의록을 분석하는 함수
def analyze_meeting_notes_with_claude(meeting_text):
    # 프롬프트 생성
    human_msg = f"다음 회의록 텍스트를 분석하여 아래 항목들을 추출하고, JSON 형식으로 정리해줘. 각 항목의 값이 없다면 빈 문자열(\"\")로 표시해줘.\n\n"
    human_msg += f"회의록 텍스트:\n\"\"\"\n{meeting_text}\n\"\"\"\n\n"
    human_msg += "추출 항목:\n"
    human_msg += "- 회의 리드: (회의 진행자 이름)\n"
    human_msg += "- 참석자: (쉼표로 구분된 참석자 목록)\n"
    human_msg += "- 일자: (YYYY-MM-DD 형식, 알 수 없다면 빈 문자열)\n"
    human_msg += "- 진행 단계: ('시작 전' 또는 '시작 후')\n"
    human_msg += "- 아젠다 사전 공유: (체크된 참석자 목록을 배열 형태로)\n"
    human_msg += "- 회의 목적: (회의 목적 텍스트)\n"
    human_msg += "- 회의 아젠다: (각 아젠다 항목을 객체 배열로 - 항목 제목, 소요시간, 관련 자료 속성 포함)\n"
    human_msg += "- 주요 논의 내용: (각 아젠다 항목별 논의 내용을 객체 배열로 - 아젠다 제목, 논의 내용 배열 속성 포함)\n"
    human_msg += "- 주요 결정 사항: (결정 사항 목록을 객체 배열로 - 제목, 세부 내용 속성 포함)\n"
    human_msg += "- 후속 액션: (후속 조치 목록을 배열로)\n"
    human_msg += "- 회의 피드백: (좋았던 점, 개선할 점, 다음 회의 제안 사항을 속성으로 가진 객체)\n"
    human_msg += "- 다음 회의 일정: (일시, 장소, 주요 아젠다를 속성으로 가진 객체)\n\n"
    human_msg += "결과는 반드시 JSON 형식으로만 반환해야 하며, 다른 설명은 포함하지 마."
    
    # Claude API 호출
    try:
        response_message = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=2048,
            messages=[
                {"role": "user", "content": human_msg}
            ]
        )
        analyzed_data = response_message.content[0].text.strip()
        return analyzed_data
    except Exception as e:
        print(f"Claude API 호출 중 오류 발생: {e}")
        return None

# 메인 실행 블록
if __name__ == "__main__":
    print("Claude 회의록 분석기를 실행합니다...")
    
    # 테스트용 샘플 회의록
    sample_meeting_notes = """
회의 제목: 2024년 2분기 신제품 개발 회의
날짜: 2024년 4월 10일 오후 2시
참석자: 이대표, 김팀장, 박연구원, 최디자이너

주요 안건:
1. 신제품 '알파' 프로토타입 리뷰
2. 출시 일정 및 마케팅 전략 논의
3. 다음 주 시연 준비 사항 점검

논의 내용:
이대표는 '알파' 프로토타입의 완성도에 만족감을 표하며, 사용자 피드백을 빠르게 반영할 것을 주문했다.
김팀장은 현재까지의 개발 진척 상황을 보고하고, 5월 중순 출시 목표를 제시했다.
박연구원은 핵심 기능 시연 중 발생 가능한 기술적 이슈와 해결 방안을 설명했다.
최디자이너는 제품 패키징 디자인 시안 A, B를 선보였고, 참석자들은 B안에 대해 긍정적인 반응을 보였다.

결정 사항:
1. '알파' 프로토타입 사용자 테스트 그룹 모집 시작 (담당자: 김팀장, 기한: 4월 15일)
2. 패키징 디자인은 B안으로 최종 결정하고, 세부 수정 진행 (담당자: 최디자이너, 기한: 4월 12일)
3. 마케팅팀과 협력하여 2분기 홍보 계획 수립 (담당자: 김팀장, 기한: 4월 20일)

다음 액션 아이템:
- 박연구원: 시연용 데모 안정화 및 최종 점검 (기한: 4월 17일)
- 김팀장: 주간 회의에서 마케팅팀 진행 상황 공유 (기한: 매주 월요일)
    """
    
    # 분석 실행
    analysis_result = analyze_meeting_notes_with_claude(sample_meeting_notes)
    
    # 결과 출력
    if analysis_result:
        print("\n--- Claude 분석 결과 (JSON 예상) ---")
        print(analysis_result)
    else:
        print("회의록 분석에 실패했습니다.") 