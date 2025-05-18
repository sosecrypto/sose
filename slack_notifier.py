import os
import json
import requests
from datetime import datetime

# Slack API 웹훅 URL 설정
SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")

def notify_slack_meeting_notes(meeting_data, notion_page_id=None):
    """
    노션 회의록이 생성되었을 때 슬랙으로 알림을 보냅니다.
    
    Args:
        meeting_data (dict): 회의록 데이터
        notion_page_id (str, optional): 노션 페이지 ID
    
    Returns:
        bool: 알림 전송 성공 여부
    """
    if not SLACK_WEBHOOK_URL:
        print("Slack 웹훅 URL이 설정되지 않았습니다.")
        print("PowerShell에서 $env:SLACK_WEBHOOK_URL=\"여러분의_웹훅_URL\" 명령으로 설정해주세요.")
        return False
    
    try:
        # 회의 제목 및 일시 정보 가져오기
        meeting_title = meeting_data.get("회의 제목", "무제 회의록")
        meeting_date = meeting_data.get("일자", "")
        meeting_lead = meeting_data.get("회의 리드", "")
        participants = meeting_data.get("참석자", "")
        
        # 결정 사항 및 액션 아이템 준비
        decisions = meeting_data.get("주요 결정 사항", [])
        action_items = meeting_data.get("후속 액션", [])
        
        # 슬랙 메시지 본문 구성
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"📝 새 회의록: {meeting_title}",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*일시:*\n{meeting_date}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*진행자:*\n{meeting_lead}"
                    }
                ]
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*참석자:*\n{participants}"
                    }
                ]
            },
            {
                "type": "divider"
            }
        ]
        
        # 결정 사항이 있을 경우 추가
        if decisions:
            decision_text = "*주요 결정 사항:*\n"
            
            if isinstance(decisions, list):
                for i, decision in enumerate(decisions):
                    if isinstance(decision, dict) and "제목" in decision:
                        decision_text += f"• {decision['제목']}\n"
                    else:
                        decision_text += f"• {decision}\n"
            else:
                decision_text += f"{decisions}\n"
                
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": decision_text
                }
            })
        
        # 액션 아이템이 있을 경우 추가
        if action_items:
            action_text = "*후속 액션:*\n"
            
            if isinstance(action_items, list):
                for i, action in enumerate(action_items):
                    action_text += f"• {action}\n"
            else:
                action_text += f"{action_items}\n"
                
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": action_text
                }
            })
        
        # 노션 링크가 있을 경우 추가
        if notion_page_id:
            notion_url = f"https://notion.so/{notion_page_id.replace('-', '')}"
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "자세한 내용은 노션 회의록에서 확인하세요:"
                }
            })
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"<{notion_url}|📋 노션에서 회의록 보기>"
                }
            })
        
        # 슬랙 메시지 전체 구성
        slack_data = {
            "blocks": blocks
        }
        
        # Slack API 호출
        response = requests.post(
            SLACK_WEBHOOK_URL,
            data=json.dumps(slack_data),
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            print("슬랙 알림이 성공적으로 전송되었습니다.")
            return True
        else:
            print(f"슬랙 알림 전송 실패. 상태 코드: {response.status_code}, 응답: {response.text}")
            return False
            
    except Exception as e:
        print(f"슬랙 알림 전송 중 오류 발생: {e}")
        return False

# 테스트 코드
if __name__ == "__main__":
    # 샘플 회의 데이터로 테스트
    sample_meeting_data = {
        "회의 제목": "2024년 2분기 신제품 개발 회의",
        "일자": "2024-04-10",
        "회의 리드": "김팀장",
        "참석자": "이대표, 김팀장, 박연구원, 최디자이너",
        "주요 결정 사항": [
            {"제목": "'알파' 프로토타입 사용자 테스트 그룹 모집 시작", "세부 내용": "테스트 참가자 10명 모집"},
            {"제목": "패키징 디자인은 B안으로 최종 결정", "세부 내용": "세부 수정 진행"}
        ],
        "후속 액션": [
            "시연용 데모 안정화 및 최종 점검 (박연구원)",
            "주간 회의에서 마케팅팀 진행 상황 공유 (김팀장)"
        ]
    }
    
    # 가상의 노션 페이지 ID
    fake_notion_page_id = "1234abcd5678efgh9012ijkl"
    
    # 슬랙 알림 테스트
    notify_slack_meeting_notes(sample_meeting_data, fake_notion_page_id) 