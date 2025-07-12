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
    
    def get_marie_claire_horoscope(self, date: datetime.date, zodiac: str) -> Optional[str]:
        """마리끌레어 코리아에서 운세를 가져옵니다."""
        try:
            # 날짜 포맷 변환
            year = date.year
            month = date.month
            
            # URL 생성 (실제 사이트 패턴에 맞게)
            url = f"https://www.marieclairekorea.com/horoscope/{year}/{month:02d}/horoscope{year%100:02d}{month:02d}/"
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 전체 텍스트에서 별자리 관련 내용 찾기
            all_text = soup.get_text()
            
            # 별자리별 패턴 매칭 (더 긴 내용을 포함하도록 개선)
            zodiac_patterns = {
                "물병자리": r'물병자리.*?DAY&COLOR.*?(?=물고기자리|양자리|황소자리|쌍둥이자리|게자리|사자자리|처녀자리|천칭자리|전갈자리|사수자리|염소자리|잘 맞는다고)',
                "물고기자리": r'물고기자리.*?DAY&COLOR.*?(?=양자리|황소자리|쌍둥이자리|게자리|사자자리|처녀자리|천칭자리|전갈자리|사수자리|염소자리|물병자리|잘 맞는다고)',
                "양자리": r'양자리.*?DAY&COLOR.*?(?=황소자리|쌍둥이자리|게자리|사자자리|처녀자리|천칭자리|전갈자리|사수자리|염소자리|물병자리|물고기자리|잘 맞는다고)',
                "황소자리": r'황소자리.*?DAY&COLOR.*?(?=쌍둥이자리|게자리|사자자리|처녀자리|천칭자리|전갈자리|사수자리|염소자리|물병자리|물고기자리|양자리|잘 맞는다고)',
                "쌍둥이자리": r'쌍둥이자리.*?DAY&COLOR.*?(?=게자리|사자자리|처녀자리|천칭자리|전갈자리|사수자리|염소자리|물병자리|물고기자리|양자리|황소자리|잘 맞는다고)',
                "게자리": r'게자리.*?DAY&COLOR.*?(?=사자자리|처녀자리|천칭자리|전갈자리|사수자리|염소자리|물병자리|물고기자리|양자리|황소자리|쌍둥이자리|잘 맞는다고)',
                "사자자리": r'사자자리.*?DAY&COLOR.*?(?=처녀자리|천칭자리|전갈자리|사수자리|염소자리|물병자리|물고기자리|양자리|황소자리|쌍둥이자리|게자리|잘 맞는다고)',
                "처녀자리": r'처녀자리.*?DAY&COLOR.*?(?=천칭자리|전갈자리|사수자리|염소자리|물병자리|물고기자리|양자리|황소자리|쌍둥이자리|게자리|사자자리|잘 맞는다고)',
                "천칭자리": r'천칭자리.*?DAY&COLOR.*?(?=전갈자리|사수자리|염소자리|물병자리|물고기자리|양자리|황소자리|쌍둥이자리|게자리|사자자리|처녀자리|잘 맞는다고)',
                "전갈자리": r'전갈자리.*?DAY&COLOR.*?(?=사수자리|염소자리|물병자리|물고기자리|양자리|황소자리|쌍둥이자리|게자리|사자자리|처녀자리|천칭자리|잘 맞는다고)',
                "사수자리": r'사수자리.*?DAY&COLOR.*?(?=염소자리|물병자리|물고기자리|양자리|황소자리|쌍둥이자리|게자리|사자자리|처녀자리|천칭자리|전갈자리|잘 맞는다고)',
                "염소자리": r'염소자리.*?DAY&COLOR.*?(?=물병자리|물고기자리|양자리|황소자리|쌍둥이자리|게자리|사자자리|처녀자리|천칭자리|전갈자리|사수자리|잘 맞는다고)'
            }
            
            # 더 정확한 패턴 매칭을 위해 개선된 방식 사용
            zodiac_patterns_improved = [
                rf'aries\s*{zodiac}.*?DAY&COLOR.*?(?=pisces|물고기자리|황소자리|taurus)',
                rf'{zodiac}\s*\([^)]+\).*?DAY&COLOR.*?(?=물고기자리|황소자리|쌍둥이자리|게자리|사자자리|처녀자리|천칭자리|전갈자리|사수자리|염소자리|잘 맞는다고)',
                rf'{zodiac}.*?(?=DAY&COLOR).*?DAY&COLOR.*?(?=물고기자리|황소자리|쌍둥이자리|게자리|사자자리|처녀자리|천칭자리|전갈자리|사수자리|염소자리|잘 맞는다고)'
            ]
            
            for pattern in zodiac_patterns_improved:
                match = re.search(pattern, all_text, re.DOTALL | re.IGNORECASE)
                if match:
                    content = match.group().strip()
                    # 불필요한 공백과 문자 정리
                    content = re.sub(r'\s+', ' ', content)
                    content = re.sub(r'✔️.*?(?=\s|$)', '', content)  # DAY&COLOR 정보 제거
                    # 다른 별자리 이름 제거
                    content = re.sub(r'(물병자리|물고기자리|황소자리|쌍둥이자리|게자리|사자자리|처녀자리|천칭자리|전갈자리|사수자리|염소자리).*$', '', content)
                    if len(content.strip()) > 20:  # 의미 있는 내용인지 확인
                        return self.clean_text(content)
            
            # 대안적 방법: 간단한 패턴 매칭
            simple_pattern = rf'{zodiac}.*?(?=\n.*?자리|\n.*?잘 맞는다고|$)'
            match = re.search(simple_pattern, all_text, re.DOTALL)
            
            if match:
                content = match.group().strip()
                return self.clean_text(content[:500])  # 500자로 제한
            
            return f"{zodiac} 운세 정보를 찾을 수 없습니다."
            
        except requests.RequestException as e:
            print(f"마리끌레어 요청 오류: {e}")
            return "네트워크 오류로 운세를 가져올 수 없습니다."
        except Exception as e:
            print(f"마리끌레어 파싱 오류: {e}")
            return "운세 정보를 처리하는 중 오류가 발생했습니다."
    
    def get_elle_horoscope(self, date: datetime.date, zodiac: str) -> Optional[str]:
        """엘르 코리아에서 운세를 가져옵니다."""
        try:
            # 엘르 코리아 한국어 사이트의 별자리 운세 페이지
            year = date.year
            month = date.month
            day = date.day
            
            # 여러 가능한 URL 시도
            urls = [
                f"https://www.elle.co.kr/starsigns/today/",
                f"https://www.elle.co.kr/horoscopes/",
                f"https://www.elle.co.kr/life/horoscopes/"
            ]
            
            for url in urls:
                try:
                    response = self.session.get(url, timeout=10)
                    response.raise_for_status()
                    
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # 전체 텍스트에서 별자리 관련 내용 찾기
                    all_text = soup.get_text()
                    
                    # 별자리별 패턴 매칭
                    zodiac_patterns = [
                        rf'{zodiac}.*?(?=물병자리|물고기자리|양자리|황소자리|쌍둥이자리|게자리|사자자리|처녀자리|천칭자리|전갈자리|사수자리|염소자리|운세|오늘의)',
                        rf'{zodiac}.*?(?=\n.*?자리|\n.*?운세|$)'
                    ]
                    
                    for pattern in zodiac_patterns:
                        match = re.search(pattern, all_text, re.DOTALL | re.IGNORECASE)
                        if match:
                            content = match.group().strip()
                            if len(content) > 10:  # 최소 길이 체크
                                return self.clean_text(content[:400])  # 400자로 제한
                    
                    break  # 첫 번째 성공한 URL에서 종료
                    
                except requests.RequestException:
                    continue  # 다음 URL 시도
            
            return f"{zodiac} 운세 정보를 찾을 수 없습니다."
            
        except Exception as e:
            print(f"엘르 파싱 오류: {e}")
            return "운세 정보를 처리하는 중 오류가 발생했습니다."
    
    def get_singles_horoscope(self, date: datetime.date, zodiac: str) -> Optional[str]:
        """싱글즈 코리아에서 운세를 가져옵니다."""
        try:
            # 여러 가능한 URL 시도
            urls = [
                "https://m.singleskorea.com/horoscope",
                "https://www.singleskorea.com/horoscope",
                "https://singleskorea.com/horoscope",
                "https://m.singleskorea.com/fortune",
                "https://www.singleskorea.com/fortune"
            ]
            
            for url in urls:
                try:
                    response = self.session.get(url, timeout=10)
                    response.raise_for_status()
                    
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # 전체 텍스트에서 별자리 관련 내용 찾기
                    all_text = soup.get_text()
                    
                    # 별자리별 패턴 매칭
                    zodiac_patterns = [
                        rf'{zodiac}.*?(?=물병자리|물고기자리|양자리|황소자리|쌍둥이자리|게자리|사자자리|처녀자리|천칭자리|전갈자리|사수자리|염소자리|운세|오늘의)',
                        rf'{zodiac}.*?(?=\n.*?자리|\n.*?운세|$)'
                    ]
                    
                    for pattern in zodiac_patterns:
                        match = re.search(pattern, all_text, re.DOTALL | re.IGNORECASE)
                        if match:
                            content = match.group().strip()
                            if len(content) > 10:  # 최소 길이 체크
                                return self.clean_text(content[:400])  # 400자로 제한
                    
                    break  # 첫 번째 성공한 URL에서 종료
                    
                except requests.RequestException:
                    continue  # 다음 URL 시도
            
            # 대안: 한국의 다른 운세 사이트를 사용
            return self._get_alternative_horoscope(zodiac, date)
            
        except Exception as e:
            print(f"싱글즈 파싱 오류: {e}")
            return "운세 정보를 처리하는 중 오류가 발생했습니다."
    
    def _get_alternative_horoscope(self, zodiac: str, date: datetime.date) -> str:
        """대안 운세 사이트에서 정보를 가져옵니다."""
        try:
            # 한국의 다른 운세 사이트들을 시도
            alternative_urls = [
                "https://unse.sportschosun.com/unse/saju/total/form",
                "https://www.koreaetour.com/south-koreans-and-the-importance-of-defining-personalities/"
            ]
            
            for url in alternative_urls:
                try:
                    response = self.session.get(url, timeout=10)
                    response.raise_for_status()
                    
                    soup = BeautifulSoup(response.content, 'html.parser')
                    all_text = soup.get_text()
                    
                    # 별자리 패턴 매칭
                    pattern = rf'{zodiac}.*?(?=\n.*?자리|\n.*?운세|$)'
                    match = re.search(pattern, all_text, re.DOTALL | re.IGNORECASE)
                    
                    if match:
                        content = match.group().strip()
                        if len(content) > 10:
                            return self.clean_text(content[:300])
                    
                except requests.RequestException:
                    continue
            
            return f"{zodiac} 운세 정보를 찾을 수 없습니다."
            
        except Exception as e:
            print(f"대안 사이트 오류: {e}")
            return f"{zodiac} 운세 정보를 찾을 수 없습니다."
    
    def get_all_horoscopes(self, date: datetime.date, zodiac: str) -> dict:
        """모든 사이트에서 운세를 가져옵니다."""
        results = {}
        
        # 각 사이트에서 순차적으로 운세 가져오기 (서버 부하 방지를 위해 약간의 딜레이)
        results['marie_claire'] = self.get_marie_claire_horoscope(date, zodiac)
        time.sleep(random.uniform(1, 2))
        
        results['elle'] = self.get_elle_horoscope(date, zodiac)
        time.sleep(random.uniform(1, 2))
        
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
        
        return text.strip()

# 테스트 함수
def test_scraper():
    """스크래퍼 테스트 함수"""
    scraper = HoroscopeScraper()
    today = datetime.date.today()
    
    print("=== 스크래퍼 테스트 ===")
    print(f"날짜: {today}")
    print(f"별자리: 양자리")
    print()
    
    # 마리끌레어 테스트
    print("1. 마리끌레어 코리아:")
    marie_result = scraper.get_marie_claire_horoscope(today, "양자리")
    print(marie_result[:200] + "..." if len(marie_result) > 200 else marie_result)
    print()
    
    # 엘르 테스트
    print("2. 엘르 코리아:")
    elle_result = scraper.get_elle_horoscope(today, "양자리")
    print(elle_result[:200] + "..." if len(elle_result) > 200 else elle_result)
    print()
    
    # 싱글즈 테스트
    print("3. 싱글즈 코리아:")
    singles_result = scraper.get_singles_horoscope(today, "양자리")
    print(singles_result[:200] + "..." if len(singles_result) > 200 else singles_result)

if __name__ == "__main__":
    test_scraper() 