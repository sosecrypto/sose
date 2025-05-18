import os
import json
from claude_analyzer import analyze_meeting_notes_with_claude
from notion_connector import add_meeting_notes_to_notion

def process_meeting_notes(meeting_text):
    """
    회의록 텍스트를 Claude로 분석하고 Notion에 등록합니다.
    """
    print("클로바 노트 회의록 분석 및 노션 등록을 시작합니다...")
    
    # 1. Claude로 회의록 분석
    print("회의록 분석 중...")
    analysis_result = analyze_meeting_notes_with_claude(meeting_text)
    
    if not analysis_result:
        print("회의록 분석에 실패했습니다.")
        return None
    
    # 2. JSON 분석 결과 파싱
    try:
        meeting_data = json.loads(analysis_result)
        print("회의록 분석 완료!")
        print(f"제목: {meeting_data.get('회의 제목', '제목 없음')}")
        print(f"일시: {meeting_data.get('회의 일시', '일시 정보 없음')}")
    except json.JSONDecodeError as e:
        print(f"Claude 응답을 JSON으로 파싱하는 중 오류 발생: {e}")
        print("원본 응답:", analysis_result)
        return None
    
    # 3. Notion에 회의록 등록
    print("\n노션에 회의록 등록 중...")
    page_id = add_meeting_notes_to_notion(meeting_data)
    
    if page_id:
        print(f"노션 회의록 URL: https://notion.so/{page_id.replace('-', '')}")
        return page_id
    else:
        print("노션 회의록 등록에 실패했습니다.")
        return None

def main():
    """
    메인 함수: 사용자에게 회의록 텍스트 입력을 받고 처리합니다.
    """
    print("=" * 50)
    print("클로바 노트 → 노션 회의록 변환기")
    print("=" * 50)
    print("\n회의록 텍스트를 붙여넣으세요. 입력을 마치려면 빈 줄에서 Ctrl+Z(Windows) 또는 Ctrl+D(Linux/Mac)를 누르고 Enter를 누르세요.\n")
    
    # 여러 줄의 텍스트 입력 받기
    lines = []
    while True:
        try:
            line = input()
            lines.append(line)
        except EOFError:
            break
    
    meeting_text = "\n".join(lines)
    
    if not meeting_text.strip():
        print("입력된 회의록 텍스트가 없습니다.")
        return
    
    # 회의록 처리
    page_id = process_meeting_notes(meeting_text)
    
    if page_id:
        print("\n처리 완료! 회의록이 성공적으로 노션에 추가되었습니다.")
    else:
        print("\n처리 실패: 회의록을 노션에 추가하는 과정에서 오류가 발생했습니다.")

if __name__ == "__main__":
    # 환경 변수 체크 제거
    main() 