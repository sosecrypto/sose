import json
import os
from notion_client import Client
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# Notion API 키 설정
NOTION_API_KEY = os.environ.get("NOTION_API_KEY")
# 데이터베이스 ID 설정
DATABASE_ID = os.environ.get("NOTION_DATABASE_ID")

# Notion 클라이언트 초기화
def init_notion_client():
    """Notion API 클라이언트를 초기화합니다."""
    if not NOTION_API_KEY:
        print("Notion API 키가 설정되지 않았습니다.")
        print("환경 변수 NOTION_API_KEY를 설정하거나 .env 파일에 추가해주세요.")
        return None
        
    if not DATABASE_ID:
        print("Notion 데이터베이스 ID가 설정되지 않았습니다.")
        print("환경 변수 NOTION_DATABASE_ID를 설정하거나 .env 파일에 추가해주세요.")
        return None
        
    try:
        notion = Client(auth=NOTION_API_KEY)
        return notion
    except Exception as e:
        print(f"Notion 클라이언트 초기화 중 오류 발생: {e}")
        return None

# 결정 사항과 액션 아이템을 노션용 리치 텍스트로 변환
def format_items_for_notion(items):
    """
    결정 사항이나 액션 아이템 목록을 노션 리치 텍스트 형식으로 변환합니다.
    """
    if not items or not isinstance(items, list):
        return []
        
    result = []
    
    for i, item in enumerate(items):
        # 각 항목을 번호가 매겨진 목록으로 변환
        if isinstance(item, dict):
            # 구조화된 형식인 경우 (내용, 담당자, 기한)
            item_text = f"{i+1}. {item.get('내용', '')}"
            if item.get('담당자'):
                item_text += f" (담당자: {item['담당자']}"
                if item.get('기한'):
                    item_text += f", 기한: {item['기한']}"
                item_text += ")"
        else:
            # 단순 문자열인 경우
            item_text = f"{i+1}. {item}"
            
        # 노션 리치 텍스트 블록 구성
        result.append({
            "type": "text",
            "text": {
                "content": item_text,
            }
        })
        
        # 줄바꿈 추가
        result.append({
            "type": "text", 
            "text": {"content": "\n"}
        })
        
    return result

# 노션 데이터베이스에 회의록 추가
def add_meeting_notes_to_notion(meeting_data):
    """
    회의록 데이터를 노션 데이터베이스에 추가합니다.
    meeting_data는 JSON 형식의 문자열 또는 Python 딕셔너리 형태의 회의록 데이터입니다.
    """
    # 1. JSON 문자열이면 파이썬 딕셔너리로 변환
    if isinstance(meeting_data, str):
        try:
            meeting_data = json.loads(meeting_data)
        except json.JSONDecodeError as e:
            print(f"JSON 파싱 오류: {e}")
            return None
    
    # 2. Notion 클라이언트 초기화
    notion = init_notion_client()
    if not notion:
        print("Notion 클라이언트를 초기화할 수 없습니다.")
        return None
    
    try:
        # 3. 메인 속성 (제목) 설정
        properties = {
            "이름": {  # 실제 노션 데이터베이스의 제목 속성 이름에 맞게 변경하세요 ("이름", "회의 제목" 등)
                "title": [
                    {
                        "type": "text",
                        "text": {
                            "content": meeting_data.get("회의 제목", "무제 회의록")
                        }
                    }
                ]
            }
        }
        
        # 4. 회의 일시 설정 (날짜 속성)
        if meeting_data.get("회의 일시"):
            properties["회의 일시"] = {  # 실제 노션 데이터베이스의 날짜 속성 이름에 맞게 변경하세요
                "date": {
                    "start": meeting_data["회의 일시"].replace(" ", "T")  # ISO 형식으로 변환
                }
            }
        
        # 5. 참석자 설정 (다중 선택 또는 리치 텍스트)
        if meeting_data.get("참석자"):
            # 다중 선택인 경우:
            # properties["참석자"] = {
            #     "multi_select": [{"name": name.strip()} for name in meeting_data["참석자"].split(',')]
            # }
            
            # 리치 텍스트인 경우:
            properties["참석자"] = {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": meeting_data["참석자"]
                        }
                    }
                ]
            }
        
        # 6. 주요 안건 설정 (리치 텍스트)
        if meeting_data.get("주요 안건"):
            안건_내용 = ""
            if isinstance(meeting_data["주요 안건"], list):
                # 리스트인 경우 번호를 붙여서 텍스트로 변환
                for i, item in enumerate(meeting_data["주요 안건"]):
                    안건_내용 += f"{i+1}. {item}\n"
            else:
                안건_내용 = meeting_data["주요 안건"]
                
            properties["주요 안건"] = {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": 안건_내용
                        }
                    }
                ]
            }
        
        # 7. 논의 내용 요약 설정 (리치 텍스트)
        if meeting_data.get("논의된 내용 요약"):
            properties["논의 내용 요약"] = {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": meeting_data["논의된 내용 요약"]
                        }
                    }
                ]
            }
        
        # 8. 결정 사항 설정 (리치 텍스트)
        if meeting_data.get("결정 사항"):
            if isinstance(meeting_data["결정 사항"], list):
                # 복잡한 리스트 형태의 결정 사항 처리
                결정_내용 = format_items_for_notion(meeting_data["결정 사항"])
                properties["결정 사항"] = {
                    "rich_text": 결정_내용 if 결정_내용 else [{"type": "text", "text": {"content": ""}}]
                }
            else:
                # 단순 문자열 형태인 경우
                properties["결정 사항"] = {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": meeting_data["결정 사항"]
                            }
                        }
                    ]
                }
        
        # 9. 다음 액션 아이템 설정 (리치 텍스트)
        if meeting_data.get("다음 액션 아이템"):
            if isinstance(meeting_data["다음 액션 아이템"], list):
                # 복잡한 리스트 형태의 액션 아이템 처리
                액션_내용 = format_items_for_notion(meeting_data["다음 액션 아이템"])
                properties["다음 액션 아이템"] = {
                    "rich_text": 액션_내용 if 액션_내용 else [{"type": "text", "text": {"content": ""}}]
                }
            else:
                # 단순 문자열 형태인 경우
                properties["다음 액션 아이템"] = {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": meeting_data["다음 액션 아이템"]
                            }
                        }
                    ]
                }
        
        # 10. 데이터베이스에 페이지 생성
        response = notion.pages.create(
            parent={"database_id": DATABASE_ID},
            properties=properties
        )
        
        print(f"노션에 회의록이 성공적으로 추가되었습니다. 페이지 ID: {response['id']}")
        return response["id"]
        
    except Exception as e:
        print(f"노션에 회의록 추가 중 오류 발생: {e}")
        return None

# 테스트 코드
if __name__ == "__main__":
    # 샘플 회의록 데이터
    sample_meeting_data = {
        "회의 제목": "2024년 2분기 신제품 개발 회의",
        "회의 일시": "2024-04-10 14:00",
        "참석자": "이대표, 김팀장, 박연구원, 최디자이너",
        "주요 안건": [
            "신제품 '알파' 프로토타입 리뷰",
            "출시 일정 및 마케팅 전략 논의",
            "다음 주 시연 준비 사항 점검"
        ],
        "논의된 내용 요약": "이대표는 '알파' 프로토타입의 완성도에 만족감을 표하며, 사용자 피드백을 빠르게 반영할 것을 주문했다. 김팀장은 현재까지의 개발 진척 상황을 보고하고, 5월 중순 출시 목표를 제시했다.",
        "결정 사항": [
            {
                "내용": "'알파' 프로토타입 사용자 테스트 그룹 모집 시작",
                "담당자": "김팀장",
                "기한": "2024-04-15"
            },
            {
                "내용": "패키징 디자인은 B안으로 최종 결정하고, 세부 수정 진행",
                "담당자": "최디자이너",
                "기한": "2024-04-12"
            }
        ],
        "다음 액션 아이템": [
            {
                "내용": "시연용 데모 안정화 및 최종 점검",
                "담당자": "박연구원",
                "기한": "2024-04-17"
            },
            {
                "내용": "주간 회의에서 마케팅팀 진행 상황 공유",
                "담당자": "김팀장",
                "기한": "매주 월요일"
            }
        ]
    }
    
    # 노션에 회의록 추가 테스트
    page_id = add_meeting_notes_to_notion(sample_meeting_data)
    if page_id:
        print(f"회의록 페이지 URL: https://notion.so/{page_id.replace('-', '')}") 