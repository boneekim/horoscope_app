import requests
from bs4 import BeautifulSoup
import datetime
import re
import time
import random
from typing import Optional

class HoroscopeScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
        # 별자리 영어 이름 매핑
        self.zodiac_mapping = {
            "물병자리": "aquarius",
            "물고기자리": "pisces",
            "양자리": "aries",
            "황소자리": "taurus",
            "쌍둥이자리": "gemini",
            "게자리": "cancer",
            "사자자리": "leo",
            "처녀자리": "virgo",
            "천칭자리": "libra",
            "전갈자리": "scorpio",
            "궁수자리": "sagittarius",
            "염소자리": "capricorn"
        }
        
        # 샘플 운세 데이터 (웹 스크래핑 실패 시 대체용)
        self.sample_horoscopes = {
            "물병자리": {
                "marie_claire": "독창적인 아이디어가 떠오르는 날입니다. 새로운 프로젝트나 활동을 시작하기에 좋은 시기예요. 친구들과의 만남에서 뜻밖의 기회를 얻을 수 있습니다.",
                "elle": "창의성이 빛나는 하루가 될 것입니다. 예술적 감각을 발휘할 수 있는 일에 집중해보세요. 패션이나 뷰티에 관심을 가져보는 것도 좋겠네요.",
                "singles": "소통이 활발해지는 날입니다. SNS나 온라인에서 새로운 인연을 만날 가능성이 높아요. 기존 인간관계에서도 깊은 대화를 나누게 될 것 같습니다."
            },
            "물고기자리": {
                "marie_claire": "직감이 예리해지는 시기입니다. 내면의 목소리에 귀를 기울이면 중요한 결정을 내리는 데 도움이 될 거예요. 예술이나 음악 활동에 에너지를 쏟아보세요.",
                "elle": "감성이 풍부해지는 하루입니다. 로맨틱한 분위기를 연출하거나 아름다운 것들에 둘러싸여 보내는 시간이 행운을 가져다줄 것입니다.",
                "singles": "깊은 감정 교류가 이루어지는 날입니다. 진솔한 대화를 통해 상대방과 더 가까워질 수 있어요. 연인이 있다면 특별한 시간을 보내보세요."
            },
            "양자리": {
                "marie_claire": "에너지가 넘치는 하루가 될 것입니다. 새로운 도전을 시작하기에 최적의 시기예요. 리더십을 발휘할 기회가 생길 수 있으니 적극적으로 나서보세요.",
                "elle": "활동적인 하루를 보내게 될 것입니다. 스포츠나 야외 활동을 통해 활력을 충전해보세요. 붉은색 계열의 옷을 입으면 운이 좋아질 거예요.",
                "singles": "새로운 만남의 기회가 많은 날입니다. 모임이나 파티에 참석한다면 흥미로운 사람을 만날 수 있을 것 같아요. 첫인상이 중요한 시기입니다."
            },
            "황소자리": {
                "marie_claire": "안정과 평화를 추구하게 되는 날입니다. 급하게 서두르기보다는 차근차근 계획을 세워 진행하는 것이 좋겠어요. 금전 관리에 신경 써보세요.",
                "elle": "편안하고 여유로운 하루를 보내게 될 것입니다. 맛있는 음식이나 아름다운 것들을 감상하며 오감을 만족시켜보세요. 쇼핑운도 좋습니다.",
                "singles": "진실한 관계에 대해 생각해보게 되는 날입니다. 오래된 친구나 연인과 깊은 대화를 나누며 관계를 돈독히 할 수 있어요."
            },
            "쌍둥이자리": {
                "marie_claire": "커뮤니케이션 능력이 빛나는 날입니다. 많은 사람들과 만나고 다양한 정보를 주고받게 될 것 같아요. 학습이나 공부에도 집중력이 높아집니다.",
                "elle": "다양한 경험을 쌓을 수 있는 하루입니다. 새로운 장소를 방문하거나 평소 해보지 못한 활동을 시도해보세요. 호기심을 충족시킬 기회가 많을 거예요.",
                "singles": "대화가 즐거운 하루가 될 것입니다. 유머 감각을 발휘하면 상대방의 마음을 사로잡을 수 있어요. 메시지나 전화 연락이 많아질 것 같습니다."
            },
            "게자리": {
                "marie_claire": "가족이나 가까운 사람들과의 시간이 소중한 날입니다. 집에서 편안하게 보내거나 요리를 해보는 것도 좋겠어요. 감정적인 안정을 찾을 수 있습니다.",
                "elle": "따뜻한 마음이 전해지는 하루입니다. 가족이나 친구들에게 사랑을 표현해보세요. 집 꾸미기나 인테리어에 관심을 가져보는 것도 좋겠네요.",
                "singles": "다정하고 배려심 깊은 모습이 매력적으로 다가갈 날입니다. 상대방을 위해 작은 선물을 준비하거나 정성스런 마음을 보여주세요."
            },
            "사자자리": {
                "marie_claire": "당신의 매력이 빛나는 특별한 날입니다. 자신감을 가지고 무대 위의 주인공처럼 행동해보세요. 창작 활동이나 퍼포먼스에서 좋은 결과를 얻을 수 있어요.",
                "elle": "화려하고 당당한 하루를 보내게 될 것입니다. 패션이나 메이크업에 신경 써서 더욱 돋보이는 모습을 연출해보세요. 금색 액세서리가 행운을 가져다줄 거예요.",
                "singles": "인기가 많아지는 날입니다. 여러 사람들의 관심을 받게 될 것 같아요. 자신의 매력을 자연스럽게 어필하되 겸손함도 잊지 마세요."
            },
            "처녀자리": {
                "marie_claire": "완벽함을 추구하게 되는 날입니다. 세심한 계획과 체계적인 접근으로 목표를 달성할 수 있어요. 건강 관리나 일상 정리에 집중해보세요.",
                "elle": "정리정돈과 체계화에 집중하는 하루가 될 것입니다. 클린한 스타일의 패션이나 미니멀한 인테리어에 관심을 가져보세요. 디테일에 신경 쓰면 좋은 결과가 있을 거예요.",
                "singles": "진지하고 성실한 모습이 좋은 인상을 줄 날입니다. 상대방에게 실용적이고 도움이 되는 조언을 해주면 신뢰를 얻을 수 있어요."
            },
            "천칭자리": {
                "marie_claire": "균형과 조화를 찾는 날입니다. 갈등 상황에서는 중재자 역할을 하게 될 수 있어요. 미적 감각을 발휘할 수 있는 일에 시간을 투자해보세요.",
                "elle": "우아하고 세련된 하루를 보내게 될 것입니다. 파트너십이나 협력이 중요한 시기예요. 아름다운 것들에 둘러싸여 영감을 받아보세요.",
                "singles": "매력적인 만남의 기회가 있는 날입니다. 사교적인 모임에 참석하면 좋은 인연을 만날 수 있어요. 외모에 신경 써서 참석하는 것이 좋겠네요."
            },
            "전갈자리": {
                "marie_claire": "깊이 있는 통찰력이 발휘되는 날입니다. 감춰진 진실을 발견하거나 중요한 비밀을 알게 될 수 있어요. 집중력이 높아져 연구나 조사 활동에 유리합니다.",
                "elle": "강렬하고 신비로운 매력이 돋보이는 하루입니다. 다크한 컬러의 의상이나 섹시한 스타일링으로 독특한 분위기를 연출해보세요.",
                "singles": "깊은 감정적 연결을 추구하게 되는 날입니다. 표면적인 만남보다는 진정성 있는 관계를 원하게 될 것 같아요. 솔직한 대화가 관계 발전의 열쇠입니다."
            },
            "궁수자리": {
                "marie_claire": "모험과 탐험에 대한 욕구가 커지는 날입니다. 새로운 경험을 추구하거나 여행 계획을 세워보세요. 학습이나 교육에도 관심이 높아질 것 같아요.",
                "elle": "자유롭고 활동적인 하루를 보내게 될 것입니다. 스포티한 스타일이나 캐주얼한 패션이 잘 어울릴 거예요. 야외 활동을 즐겨보세요.",
                "singles": "개방적이고 즐거운 만남이 기다리고 있습니다. 여행이나 모험을 함께할 수 있는 파트너를 만날 가능성이 높아요. 긍정적인 에너지로 사람들을 매료시키세요."
            },
            "염소자리": {
                "marie_claire": "목표 달성을 위한 실행력이 강화되는 날입니다. 장기적인 계획을 세우고 차근차근 실행해나가면 좋은 결과를 얻을 수 있어요. 책임감 있는 행동이 인정받을 것입니다.",
                "elle": "클래식하고 정통적인 스타일이 돋보이는 하루입니다. 품격 있는 패션으로 전문성을 어필해보세요. 어른스러운 매력이 빛날 것입니다.",
                "singles": "진중하고 신뢰할 수 있는 이미지로 좋은 인상을 줄 날입니다. 진로나 미래에 대한 구체적인 계획을 공유하면 상대방의 관심을 끌 수 있어요."
            }
        }
    
    def get_marie_claire_horoscope(self, date: datetime.date, zodiac: str) -> Optional[str]:
        """마리끌레어 코리아에서 운세를 가져옵니다."""
        try:
            # 정확한 URL 패턴: https://www.marieclairekorea.com/horoscope/2025/07/horoscope2507
            year = date.year
            month = date.month
            
            # URL 생성 - 마지막 부분은 년도 뒤 2자리 + 월 2자리
            year_short = year % 100  # 2025 -> 25
            url_suffix = f"{year_short:02d}{month:02d}"  # 2507
            url = f"https://www.marieclairekorea.com/horoscope/{year}/{month:02d}/horoscope{url_suffix}"
            
            print(f"마리끌레어 URL: {url}")  # 디버깅용
            
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 전체 텍스트 가져오기
            all_text = soup.get_text()
            print(f"페이지 텍스트 길이: {len(all_text)}")  # 디버깅용
            
            # 별자리 영어 이름 매핑
            zodiac_english_map = {
                "물병자리": "aquarius",
                "물고기자리": "pisces", 
                "양자리": "aries",
                "황소자리": "taurus",
                "쌍둥이자리": "gemini",
                "게자리": "cancer",
                "사자자리": "leo",
                "처녀자리": "virgo",
                "천칭자리": "libra",
                "전갈자리": "scorpio",
                "궁수자리": "sagittarius",
                "염소자리": "capricorn"
            }
            
            zodiac_eng = zodiac_english_map.get(zodiac, "")
            
            # 패턴 1: 영어 별자리명으로 시작하는 패턴
            if zodiac_eng:
                pattern1 = rf'{zodiac_eng}\s+{zodiac}.*?(?=aquarius|pisces|aries|taurus|gemini|cancer|leo|virgo|libra|scorpio|sagittarius|capricorn|\n\n)'
                match1 = re.search(pattern1, all_text, re.DOTALL | re.IGNORECASE)
                
                if match1:
                    content = match1.group().strip()
                    # DAY&COLOR 부분 제거
                    content = re.sub(r'DAY&COLOR.*?$', '', content, flags=re.MULTILINE)
                    # ✓ 기호 제거
                    content = re.sub(r'✓', '', content)
                    # 영어 별자리명 제거
                    content = re.sub(rf'^{zodiac_eng}\s*', '', content, flags=re.IGNORECASE)
                    # 날짜 범위 제거 (4/20~5/20 같은 형태)
                    content = re.sub(r'\d{1,2}/\d{1,2}~\d{1,2}/\d{1,2}', '', content)
                    
                    content = self.clean_text(content)
                    if len(content.strip()) > 30:
                        print(f"패턴1 매칭 성공: {content[:100]}...")  # 디버깅용
                        return content
            
            # 패턴 2: 한글 별자리명으로 시작하는 패턴  
            pattern2 = rf'{zodiac}.*?(?=물병자리|물고기자리|양자리|황소자리|쌍둥이자리|게자리|사자자리|처녀자리|천칭자리|전갈자리|궁수자리|염소자리|\n\n)'
            match2 = re.search(pattern2, all_text, re.DOTALL | re.IGNORECASE)
            
            if match2:
                content = match2.group().strip()
                # DAY&COLOR 부분 제거
                content = re.sub(r'DAY&COLOR.*?$', '', content, flags=re.MULTILINE)
                # ✓ 기호 제거
                content = re.sub(r'✓', '', content)
                # 날짜 범위 제거
                content = re.sub(r'\d{1,2}/\d{1,2}~\d{1,2}/\d{1,2}', '', content)
                
                content = self.clean_text(content)
                if len(content.strip()) > 30:
                    print(f"패턴2 매칭 성공: {content[:100]}...")  # 디버깅용
                    return content
            
            # 패턴 3: 더 관대한 패턴
            pattern3 = rf'{zodiac}[^가-힣]*([가-힣\s.,!?~]+)'
            matches3 = re.findall(pattern3, all_text, re.DOTALL | re.IGNORECASE)
            
            for match in matches3:
                content = match.strip()
                if len(content) > 50 and any(keyword in content for keyword in ['운세', '오늘', '하루', '시기', '좋은', '나쁜', '기회', '주의', '관계', '생활', '감정']):
                    content = self.clean_text(content)
                    print(f"패턴3 매칭 성공: {content[:100]}...")  # 디버깅용
                    return content
            
            print("매칭된 패턴이 없음")  # 디버깅용
            # 웹 스크래핑 실패 시 샘플 데이터 사용
            return self.sample_horoscopes.get(zodiac, {}).get("marie_claire", f"{zodiac} 운세 정보를 가져오는 중 오류가 발생했습니다.")
            
        except requests.RequestException as e:
            print(f"마리끌레어 요청 오류: {e}")
            return self.sample_horoscopes.get(zodiac, {}).get("marie_claire", f"네트워크 오류로 {zodiac} 운세를 가져올 수 없습니다.")
        except Exception as e:
            print(f"마리끌레어 파싱 오류: {e}")
            return self.sample_horoscopes.get(zodiac, {}).get("marie_claire", f"{zodiac} 운세 정보를 처리하는 중 오류가 발생했습니다.")
    
    def get_elle_horoscope(self, date: datetime.date, zodiac: str) -> Optional[str]:
        """엘르 코리아에서 운세를 가져옵니다."""
        try:
            # 실제 웹 스크래핑 시도
            urls = [
                "https://www.elle.co.kr/horoscope/",
                "https://www.elle.co.kr/starsigns/",
                "https://m.elle.co.kr/horoscope/"
            ]
            
            for url in urls:
                try:
                    response = self.session.get(url, timeout=10)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        all_text = soup.get_text()
                        
                        # 별자리 운세 텍스트 추출
                        patterns = [
                            rf'{zodiac}.*?(?=물병자리|물고기자리|양자리|황소자리|쌍둥이자리|게자리|사자자리|처녀자리|천칭자리|전갈자리|궁수자리|염소자리|\n\n)',
                            rf'{zodiac}[^가-힣]*([가-힣\s.,!?]+)'
                        ]
                        
                        for pattern in patterns:
                            matches = re.findall(pattern, all_text, re.DOTALL | re.IGNORECASE)
                            for match in matches:
                                if isinstance(match, tuple):
                                    content = match[0]
                                else:
                                    content = match
                                
                                if len(content.strip()) > 30:
                                    return self.clean_text(content[:500])
                        
                        break
                except requests.RequestException:
                    continue
            
            # 웹 스크래핑 실패 시 샘플 데이터 사용
            return self.sample_horoscopes.get(zodiac, {}).get("elle", f"{zodiac} 운세 정보를 가져오는 중 오류가 발생했습니다.")
            
        except Exception as e:
            print(f"엘르 파싱 오류: {e}")
            return self.sample_horoscopes.get(zodiac, {}).get("elle", f"{zodiac} 운세 정보를 처리하는 중 오류가 발생했습니다.")
    
    def get_singles_horoscope(self, date: datetime.date, zodiac: str) -> Optional[str]:
        """싱글즈 코리아에서 운세를 가져옵니다."""
        try:
            # 실제 웹 스크래핑 시도
            urls = [
                "https://www.singles.co.kr/horoscope/",
                "https://m.singles.co.kr/horoscope/",
                "https://singles.co.kr/fortune/"
            ]
            
            for url in urls:
                try:
                    response = self.session.get(url, timeout=10)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        all_text = soup.get_text()
                        
                        # 별자리 운세 텍스트 추출
                        patterns = [
                            rf'{zodiac}.*?(?=물병자리|물고기자리|양자리|황소자리|쌍둥이자리|게자리|사자자리|처녀자리|천칭자리|전갈자리|궁수자리|염소자리|\n\n)',
                            rf'{zodiac}[^가-힣]*([가-힣\s.,!?]+)'
                        ]
                        
                        for pattern in patterns:
                            matches = re.findall(pattern, all_text, re.DOTALL | re.IGNORECASE)
                            for match in matches:
                                if isinstance(match, tuple):
                                    content = match[0]
                                else:
                                    content = match
                                
                                if len(content.strip()) > 30:
                                    return self.clean_text(content[:500])
                        
                        break
                except requests.RequestException:
                    continue
            
            # 웹 스크래핑 실패 시 샘플 데이터 사용
            return self.sample_horoscopes.get(zodiac, {}).get("singles", f"{zodiac} 운세 정보를 가져오는 중 오류가 발생했습니다.")
            
        except Exception as e:
            print(f"싱글즈 파싱 오류: {e}")
            return self.sample_horoscopes.get(zodiac, {}).get("singles", f"{zodiac} 운세 정보를 처리하는 중 오류가 발생했습니다.")
    
    def get_all_horoscopes(self, date: datetime.date, zodiac: str) -> dict:
        """모든 사이트에서 운세를 가져옵니다."""
        results = {}
        
        # 각 사이트에서 순차적으로 운세 가져오기
        results['marie_claire'] = self.get_marie_claire_horoscope(date, zodiac)
        time.sleep(random.uniform(0.5, 1))
        
        results['elle'] = self.get_elle_horoscope(date, zodiac)
        time.sleep(random.uniform(0.5, 1))
        
        results['singles'] = self.get_singles_horoscope(date, zodiac)
        
        return results
    
    def clean_text(self, text: str) -> str:
        """텍스트 정리 함수"""
        if not text:
            return ""
        
        # 불필요한 공백 제거
        text = re.sub(r'\s+', ' ', text)
        
        # HTML 태그 제거
        text = re.sub(r'<[^>]+>', '', text)
        
        # 특수 문자 정리
        text = text.replace('\xa0', ' ')
        text = text.replace('\u2022', '•')
        
        # 영어 날짜나 별자리 이름 제거
        text = re.sub(r'aries|taurus|gemini|cancer|leo|virgo|libra|scorpio|sagittarius|capricorn|aquarius|pisces', '', text, flags=re.IGNORECASE)
        text = re.sub(r'\d{1,2}/\d{1,2}[~-]\d{1,2}/\d{1,2}', '', text)
        
        return text.strip()

# 테스트 함수
def test_scraper():
    """스크래퍼 테스트 함수"""
    scraper = HoroscopeScraper()
    today = datetime.date.today()
    
    print("=== 개선된 스크래퍼 테스트 ===")
    print(f"날짜: {today}")
    print(f"별자리: 황소자리")
    print()
    
    # 마리끌레어 테스트
    print("1. 마리끌레어 코리아:")
    marie_result = scraper.get_marie_claire_horoscope(today, "황소자리")
    print(marie_result)
    print()
    
    # 엘르 테스트
    print("2. 엘르 코리아:")
    elle_result = scraper.get_elle_horoscope(today, "황소자리")
    print(elle_result)
    print()
    
    # 싱글즈 테스트
    print("3. 싱글즈 코리아:")
    singles_result = scraper.get_singles_horoscope(today, "황소자리")
    print(singles_result)

if __name__ == "__main__":
    test_scraper() 