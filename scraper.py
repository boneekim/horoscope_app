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
            
            # URL 생성 (예시 URL에 맞게 수정)
            url = f"https://www.marieclairekorea.com/horoscope/{year}/{month:02d}/horoscope{year}{month:02d}/"
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 별자리별 운세 찾기 - 실제 사이트 구조에 맞게 수정 필요
            zodiac_sections = soup.find_all('div', class_='horoscope-item')
            
            for section in zodiac_sections:
                # 별자리 이름 찾기
                title = section.find('h3') or section.find('h2') or section.find('h4')
                if title and zodiac in title.get_text():
                    content = section.find('p') or section.find('div', class_='content')
                    if content:
                        return content.get_text().strip()
            
            # 대안적 방법: 전체 텍스트에서 별자리 관련 내용 찾기
            all_text = soup.get_text()
            zodiac_pattern = rf'{zodiac}.*?(?=\n|\.|(?:[가-힣]{{2,}}자리))'
            match = re.search(zodiac_pattern, all_text, re.DOTALL)
            
            if match:
                return match.group().strip()
            
            return "현재 해당 날짜의 운세 정보를 찾을 수 없습니다."
            
        except requests.RequestException as e:
            print(f"마리끌레어 요청 오류: {e}")
            return "네트워크 오류로 운세를 가져올 수 없습니다."
        except Exception as e:
            print(f"마리끌레어 파싱 오류: {e}")
            return "운세 정보를 처리하는 중 오류가 발생했습니다."
    
    def get_elle_horoscope(self, date: datetime.date, zodiac: str) -> Optional[str]:
        """엘르 코리아에서 운세를 가져옵니다."""
        try:
            url = "https://www.elle.co.kr/horoscopes"
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 별자리별 운세 찾기
            horoscope_items = soup.find_all('div', class_='horoscope-item') or \
                             soup.find_all('article') or \
                             soup.find_all('div', class_='item')
            
            for item in horoscope_items:
                # 별자리 이름 찾기
                title_elem = item.find('h3') or item.find('h2') or item.find('h4') or item.find('strong')
                if title_elem and zodiac in title_elem.get_text():
                    content_elem = item.find('p') or item.find('div', class_='content') or item.find('div', class_='text')
                    if content_elem:
                        return content_elem.get_text().strip()
            
            # 대안적 방법
            all_text = soup.get_text()
            zodiac_pattern = rf'{zodiac}.*?(?=\n|\.|(?:[가-힣]{{2,}}자리))'
            match = re.search(zodiac_pattern, all_text, re.DOTALL)
            
            if match:
                return match.group().strip()
            
            return "현재 해당 날짜의 운세 정보를 찾을 수 없습니다."
            
        except requests.RequestException as e:
            print(f"엘르 요청 오류: {e}")
            return "네트워크 오류로 운세를 가져올 수 없습니다."
        except Exception as e:
            print(f"엘르 파싱 오류: {e}")
            return "운세 정보를 처리하는 중 오류가 발생했습니다."
    
    def get_singles_horoscope(self, date: datetime.date, zodiac: str) -> Optional[str]:
        """싱글즈 코리아에서 운세를 가져옵니다."""
        try:
            url = "https://m.singleskorea.com/horoscope"
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 별자리별 운세 찾기
            horoscope_sections = soup.find_all('div', class_='horoscope-section') or \
                                soup.find_all('li') or \
                                soup.find_all('div', class_='item')
            
            for section in horoscope_sections:
                # 별자리 이름 찾기
                title_elem = section.find('h3') or section.find('h2') or section.find('strong') or section.find('span')
                if title_elem and zodiac in title_elem.get_text():
                    content_elem = section.find('p') or section.find('div', class_='content')
                    if content_elem:
                        return content_elem.get_text().strip()
            
            # 대안적 방법
            all_text = soup.get_text()
            zodiac_pattern = rf'{zodiac}.*?(?=\n|\.|(?:[가-힣]{{2,}}자리))'
            match = re.search(zodiac_pattern, all_text, re.DOTALL)
            
            if match:
                return match.group().strip()
            
            return "현재 해당 날짜의 운세 정보를 찾을 수 없습니다."
            
        except requests.RequestException as e:
            print(f"싱글즈 요청 오류: {e}")
            return "네트워크 오류로 운세를 가져올 수 없습니다."
        except Exception as e:
            print(f"싱글즈 파싱 오류: {e}")
            return "운세 정보를 처리하는 중 오류가 발생했습니다."
    
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