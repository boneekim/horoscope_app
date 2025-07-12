import os
import requests
import json
from typing import List, Tuple, Optional
import datetime

class ClaudeAPI:
    def __init__(self):
        self.api_key = os.getenv('CLAUDE_API_KEY')
        self.base_url = "https://api.anthropic.com/v1/messages"
        self.headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01"
        }
    
    def get_summary(self, horoscope_data: List[Tuple[str, str]], zodiac: str, date: datetime.date) -> Optional[str]:
        """
        3개 사이트의 운세 정보를 종합하여 요약을 생성합니다.
        
        Args:
            horoscope_data: (사이트명, 운세내용) 튜플의 리스트
            zodiac: 별자리 이름
            date: 선택된 날짜
            
        Returns:
            종합 요약 텍스트
        """
        if not self.api_key:
            return "Claude API 키가 설정되지 않았습니다. .env 파일을 확인해주세요."
        
        if not horoscope_data:
            return "요약할 운세 정보가 없습니다."
        
        try:
            # 운세 정보 텍스트 준비
            horoscope_text = self._prepare_horoscope_text(horoscope_data)
            
            # 프롬프트 생성
            prompt = self._create_summary_prompt(horoscope_text, zodiac, date)
            
            # Claude API 호출
            response = self._call_claude_api(prompt)
            
            if response:
                return response
            else:
                return "요약을 생성할 수 없습니다. API 호출에 실패했습니다."
                
        except Exception as e:
            print(f"Claude API 오류: {e}")
            return f"요약 생성 중 오류가 발생했습니다: {str(e)}"
    
    def _prepare_horoscope_text(self, horoscope_data: List[Tuple[str, str]]) -> str:
        """운세 데이터를 텍스트로 준비합니다."""
        text_parts = []
        
        for site_name, content in horoscope_data:
            if content and content.strip():
                text_parts.append(f"【{site_name}】\n{content.strip()}")
        
        return "\n\n".join(text_parts)
    
    def _create_summary_prompt(self, horoscope_text: str, zodiac: str, date: datetime.date) -> str:
        """Claude API용 프롬프트를 생성합니다."""
        formatted_date = date.strftime('%Y년 %m월 %d일')
        
        prompt = f"""
다음은 {formatted_date} {zodiac}의 운세 정보입니다. 3개의 다른 사이트에서 가져온 운세 정보를 종합하여 하나의 완성된 운세로 요약해주세요.

{horoscope_text}

요약 시 다음 사항을 고려해주세요:
1. 공통적으로 언급되는 내용은 강조해주세요
2. 서로 다른 관점의 내용은 균형있게 반영해주세요
3. 전체적인 흐름과 조화를 고려해주세요
4. 구체적이고 실용적인 조언을 포함해주세요
5. 긍정적이고 희망적인 톤으로 작성해주세요

다음과 같은 구조로 요약해주세요:
- 전체 운세 (2-3문장)
- 사랑/인간관계 (1-2문장)
- 직업/사업 (1-2문장)
- 건강/라이프스타일 (1-2문장)
- 오늘의 조언 (1-2문장)

자연스럽고 읽기 쉬운 한국어로 작성해주세요.
"""
        return prompt
    
    def _call_claude_api(self, prompt: str) -> Optional[str]:
        """Claude API를 호출합니다."""
        try:
            data = {
                "model": "claude-3-haiku-20240307",  # 비용 효율적인 모델 사용
                "max_tokens": 1000,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }
            
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if 'content' in result and result['content']:
                    return result['content'][0]['text']
                else:
                    print(f"API 응답 형식 오류: {result}")
                    return None
            else:
                print(f"API 오류: {response.status_code} - {response.text}")
                return None
                
        except requests.RequestException as e:
            print(f"네트워크 오류: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"JSON 파싱 오류: {e}")
            return None
        except Exception as e:
            print(f"예상치 못한 오류: {e}")
            return None
    
    def test_api_connection(self) -> bool:
        """API 연결을 테스트합니다."""
        if not self.api_key:
            print("API 키가 설정되지 않았습니다.")
            return False
        
        try:
            test_prompt = "안녕하세요. 연결 테스트입니다."
            response = self._call_claude_api(test_prompt)
            
            if response:
                print("Claude API 연결 성공!")
                return True
            else:
                print("Claude API 연결 실패!")
                return False
                
        except Exception as e:
            print(f"API 연결 테스트 오류: {e}")
            return False

# 대체 요약 생성 함수 (Claude API가 작동하지 않을 때 사용)
def create_simple_summary(horoscope_data: List[Tuple[str, str]], zodiac: str, date: datetime.date) -> str:
    """간단한 요약을 생성합니다 (Claude API 없이)."""
    if not horoscope_data:
        return "운세 정보가 없습니다."
    
    formatted_date = date.strftime('%Y년 %m월 %d일')
    
    summary_parts = [
        f"📅 {formatted_date} {zodiac} 운세 종합",
        "",
        "🌟 **각 사이트별 운세 정보**",
        ""
    ]
    
    for i, (site_name, content) in enumerate(horoscope_data, 1):
        if content and content.strip():
            # 내용이 너무 길면 줄임
            truncated_content = content[:200] + "..." if len(content) > 200 else content
            summary_parts.append(f"{i}. **{site_name}**")
            summary_parts.append(f"   {truncated_content}")
            summary_parts.append("")
    
    summary_parts.extend([
        "💡 **종합 조언**",
        f"오늘은 {zodiac}에게 새로운 기회와 가능성이 열리는 날입니다. ",
        "여러 사이트의 운세를 종합해보면, 긍정적인 에너지와 함께 ",
        "주변 사람들과의 관계에서 좋은 변화가 있을 것으로 보입니다. ",
        "자신감을 가지고 하루를 시작해보세요! ✨"
    ])
    
    return "\n".join(summary_parts)

# 테스트 함수
def test_claude_api():
    """Claude API 테스트 함수"""
    print("=== Claude API 테스트 ===")
    
    claude = ClaudeAPI()
    
    # API 연결 테스트
    if claude.test_api_connection():
        print("✅ API 연결 성공")
        
        # 샘플 데이터로 요약 테스트
        sample_data = [
            ("마리끌레어 코리아", "오늘은 양자리에게 새로운 시작의 날입니다. 용기를 내어 도전해보세요."),
            ("엘르 코리아", "창의적인 에너지가 넘치는 하루입니다. 예술적 활동에 집중해보세요."),
            ("싱글즈 코리아", "인간관계에서 좋은 소식이 있을 것입니다. 소통을 늘려보세요.")
        ]
        
        summary = claude.get_summary(sample_data, "양자리", datetime.date.today())
        print(f"📝 요약 결과:\n{summary}")
        
    else:
        print("❌ API 연결 실패")
        print("대체 요약 생성 테스트:")
        
        sample_data = [
            ("마리끌레어 코리아", "오늘은 양자리에게 새로운 시작의 날입니다. 용기를 내어 도전해보세요."),
            ("엘르 코리아", "창의적인 에너지가 넘치는 하루입니다. 예술적 활동에 집중해보세요."),
            ("싱글즈 코리아", "인간관계에서 좋은 소식이 있을 것입니다. 소통을 늘려보세요.")
        ]
        
        summary = create_simple_summary(sample_data, "양자리", datetime.date.today())
        print(f"📝 대체 요약 결과:\n{summary}")

if __name__ == "__main__":
    test_claude_api() 