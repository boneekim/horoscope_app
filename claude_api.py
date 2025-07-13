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
    
    def get_comprehensive_summary(self, horoscope_data: List[Tuple[str, str]], zodiac: str, date: datetime.date) -> Optional[str]:
        """
        마리끌레어 운세와 Claude AI가 생성한 추가 운세를 종합하여 완성된 운세를 생성합니다.
        
        Args:
            horoscope_data: (사이트명, 운세내용) 튜플의 리스트
            zodiac: 별자리 이름
            date: 선택된 날짜
            
        Returns:
            종합 운세 텍스트
        """
        if not self.api_key:
            return "Claude API 키가 설정되지 않았습니다. .env 파일을 확인해주세요."
        
        if not horoscope_data:
            return "요약할 운세 정보가 없습니다."
        
        try:
            # 마리끌레어 운세 정보 준비
            marie_claire_content = ""
            for site_name, content in horoscope_data:
                if "마리끌레어" in site_name and content and content.strip():
                    marie_claire_content = content.strip()
                    break
            
            # 종합 운세 생성 프롬프트
            prompt = self._create_comprehensive_prompt(marie_claire_content, zodiac, date)
            
            # Claude API 호출
            response = self._call_claude_api(prompt)
            
            if response:
                return response
            else:
                return "종합 운세를 생성할 수 없습니다. API 호출에 실패했습니다."
                
        except Exception as e:
            print(f"Claude API 오류: {e}")
            return f"종합 운세 생성 중 오류가 발생했습니다: {str(e)}"
    
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
    
    def _create_comprehensive_prompt(self, marie_claire_content: str, zodiac: str, date: datetime.date) -> str:
        """Claude API용 종합 운세 프롬프트를 생성합니다."""
        formatted_date = date.strftime('%Y년 %m월 %d일')
        
        prompt = f"""
당신은 전문 점성술사입니다. {formatted_date} {zodiac}의 완성된 운세를 생성해주세요.

다음은 마리끌레어 코리아에서 제공하는 기본 운세입니다:
【마리끌레어 코리아 운세】
{marie_claire_content}

이 기본 운세를 바탕으로 하되, 다음 영역들을 추가로 보완하여 완성된 하루 운세를 만들어주세요:

**구성 요소:**
1. **전체 운세**: 마리끌레어 내용을 요약하고 하루 전체의 흐름을 제시
2. **사랑/인간관계**: 연애, 가족, 친구 관계에서의 운세
3. **직업/재정**: 일, 학업, 금전과 관련된 운세  
4. **건강/라이프스타일**: 몸과 마음의 건강, 일상 관리
5. **럭키 아이템/컬러**: 오늘 도움이 될 색깔이나 아이템
6. **오늘의 조언**: 하루를 잘 보내기 위한 실용적 조언

**작성 지침:**
- 마리끌레어 내용과 자연스럽게 연결되도록 작성
- {zodiac}의 성격적 특성을 반영
- 구체적이고 실용적인 조언 포함
- 긍정적이고 희망적인 톤 유지
- 자연스럽고 읽기 쉬운 한국어로 작성
- 각 섹션을 명확히 구분하여 정리

완성된 종합 운세를 작성해주세요.
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

# 대체 종합 요약 생성 함수 (Claude API가 작동하지 않을 때 사용)
def create_comprehensive_summary(horoscope_data: List[Tuple[str, str]], zodiac: str, date: datetime.date) -> str:
    """종합 운세를 생성합니다 (Claude API 없이)."""
    if not horoscope_data:
        return "운세 정보가 없습니다."
    
    formatted_date = date.strftime('%Y년 %m월 %d일')
    
    # 마리끌레어 내용 추출
    marie_claire_content = ""
    for site_name, content in horoscope_data:
        if "마리끌레어" in site_name and content and content.strip():
            marie_claire_content = content.strip()
            break
    
    # 별자리별 특성 정의
    zodiac_traits = {
        "물병자리": {"특성": "독창적이고 혁신적", "럭키컬러": "파란색", "럭키아이템": "독특한 액세서리"},
        "물고기자리": {"특성": "감성적이고 직관적", "럭키컬러": "바다색", "럭키아이템": "물 관련 아이템"},
        "양자리": {"특성": "활동적이고 리더십", "럭키컬러": "빨간색", "럭키아이템": "스포츠용품"},
        "황소자리": {"특성": "안정적이고 실용적", "럭키컬러": "초록색", "럭키아이템": "자연 소재 아이템"},
        "쌍둥이자리": {"특성": "소통능력과 호기심", "럭키컬러": "노란색", "럭키아이템": "책이나 펜"},
        "게자리": {"특성": "가정적이고 따뜻함", "럭키컬러": "실버", "럭키아이템": "가족 사진"},
        "사자자리": {"특성": "당당하고 창조적", "럭키컬러": "금색", "럭키아이템": "반짝이는 액세서리"},
        "처녀자리": {"특성": "체계적이고 세심함", "럭키컬러": "베이지", "럭키아이템": "정리용품"},
        "천칭자리": {"특성": "균형감각과 미적감각", "럭키컬러": "핑크", "럭키아이템": "예술 작품"},
        "전갈자리": {"특성": "집중력과 통찰력", "럭키컬러": "검은색", "럭키아이템": "신비로운 소품"},
        "궁수자리": {"특성": "자유롭고 모험적", "럭키컬러": "보라색", "럭키아이템": "여행 관련 아이템"},
        "염소자리": {"특성": "성실하고 목표지향적", "럭키컬러": "갈색", "럭키아이템": "플래너"}
    }
    
    traits = zodiac_traits.get(zodiac, {"특성": "독특하고 매력적", "럭키컬러": "하얀색", "럭키아이템": "개인적인 소품"})
    
    summary_parts = [
        f"# 📅 {formatted_date} {zodiac} 종합 운세",
        "",
        "## 🌟 전체 운세",
        f"{marie_claire_content}" if marie_claire_content else f"오늘은 {zodiac}에게 {traits['특성']}한 면이 돋보이는 하루가 될 것입니다.",
        "",
        "## 💕 사랑/인간관계", 
        f"{zodiac}의 매력이 빛나는 하루입니다. 가까운 사람들과의 관계에서 따뜻한 소통이 이루어질 것 같아요. 진솔한 대화를 나누면 더욱 깊은 유대감을 형성할 수 있습니다.",
        "",
        "## 💼 직업/재정",
        f"차근차근 계획을 세워 진행하는 것이 좋은 날입니다. {traits['특성']}한 {zodiac}의 장점을 살려 업무에 집중해보세요. 금전 관리에도 신중함을 기하는 것이 좋겠습니다.",
        "",
        "## 🌿 건강/라이프스타일", 
        "몸과 마음의 균형을 맞추는 것이 중요한 하루입니다. 충분한 휴식과 함께 가벼운 운동이나 산책을 통해 활력을 충전해보세요. 규칙적인 생활 패턴이 도움이 될 것입니다.",
        "",
        "## ✨ 럭키 아이템/컬러",
        f"**럭키 컬러**: {traits['럭키컬러']}  ",
        f"**럭키 아이템**: {traits['럭키아이템']}  ",
        f"{traits['럭키컬러']} 계열의 소품을 지니거나 의상에 포인트로 활용하면 긍정적인 에너지를 받을 수 있어요.",
        "",
        "## 💡 오늘의 조언",
        f"오늘은 {zodiac}의 {traits['특성']}한 면을 자신있게 표현해보세요. 작은 변화라도 긍정적으로 받아들이고, 주변 사람들에게 따뜻한 마음을 전해보는 하루가 되길 바랍니다. ⭐"
    ]
    
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
        
        # 종합 요약 테스트
        comprehensive_summary = claude.get_comprehensive_summary(sample_data, "양자리", datetime.date.today())
        print(f"📝 종합 요약 결과:\n{comprehensive_summary}")
        
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

        # 대체 종합 요약 테스트
        comprehensive_summary = create_comprehensive_summary(sample_data, "양자리", datetime.date.today())
        print(f"📝 대체 종합 요약 결과:\n{comprehensive_summary}")

if __name__ == "__main__":
    test_claude_api() 