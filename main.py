import streamlit as st
import datetime
from scraper import HoroscopeScraper
from claude_api import ClaudeAPI
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# 페이지 설정
st.set_page_config(
    page_title="별자리 운세 종합 보기",
    page_icon="⭐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS 스타일
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #4A90E2;
        font-size: 2.5em;
        margin-bottom: 30px;
    }
    .site-section {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        background-color: #f9f9f9;
    }
    .site-title {
        color: #2C3E50;
        font-size: 1.3em;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .summary-section {
        background-color: #E8F4FD;
        border-radius: 10px;
        padding: 20px;
        margin-top: 30px;
    }
    .summary-title {
        color: #2980B9;
        font-size: 1.5em;
        font-weight: bold;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# 별자리 목록
ZODIAC_SIGNS = {
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

def main():
    st.markdown('<h1 class="main-header">⭐ 별자리 운세 종합 보기 ⭐</h1>', unsafe_allow_html=True)
    
    # 사이드바 설정
    with st.sidebar:
        st.header("설정")
        
        # 날짜 선택
        today = datetime.date.today()
        selected_date = st.date_input(
            "날짜 선택",
            value=today,
            min_value=datetime.date(2020, 1, 1),
            max_value=datetime.date(2030, 12, 31)
        )
        
        # 별자리 선택
        selected_zodiac = st.selectbox(
            "별자리 선택",
            list(ZODIAC_SIGNS.keys())
        )
        
        # 별자리 보기 버튼
        if st.button("🔮 별자리 보기", type="primary"):
            st.session_state.show_horoscope = True
            st.session_state.selected_date = selected_date
            st.session_state.selected_zodiac = selected_zodiac
    
    # 메인 컨텐츠
    if hasattr(st.session_state, 'show_horoscope') and st.session_state.show_horoscope:
        show_horoscope_results()
    else:
        st.info("왼쪽 사이드바에서 날짜와 별자리를 선택하고 '별자리 보기' 버튼을 클릭하세요.")
        
        # 사용법 안내
        st.markdown("""
        ### 📖 사용법
        1. **날짜 선택**: 원하는 날짜를 선택하세요 (기본값: 오늘)
        2. **별자리 선택**: 12개 별자리 중 하나를 선택하세요
        3. **별자리 보기**: 버튼을 클릭하면 3개 사이트에서 운세를 가져옵니다
        4. **종합 요약**: Claude AI가 3개 사이트의 운세를 종합해서 요약해드립니다
        
        ### 🌟 지원 사이트
        - **마리끌레어 코리아**: 상세한 월별 운세 정보
        - **엘르 코리아**: 패션과 라이프스타일을 중심으로 한 운세
        - **싱글즈 코리아**: 연애와 인간관계 중심의 운세
        """)

def show_horoscope_results():
    date = st.session_state.selected_date
    zodiac = st.session_state.selected_zodiac
    
    st.markdown(f"### 📅 {date.strftime('%Y년 %m월 %d일')} - {zodiac} 운세")
    
    # 로딩 상태 표시
    with st.spinner("운세 정보를 가져오는 중입니다..."):
        scraper = HoroscopeScraper()
        
        # 각 사이트에서 운세 가져오기
        col1, col2, col3 = st.columns(3)
        
        horoscope_data = []
        
        with col1:
            st.markdown('<div class="site-section">', unsafe_allow_html=True)
            st.markdown('<div class="site-title">🌸 마리끌레어 코리아</div>', unsafe_allow_html=True)
            try:
                marie_result = scraper.get_marie_claire_horoscope(date, zodiac)
                if marie_result:
                    st.write(marie_result)
                    horoscope_data.append(("마리끌레어 코리아", marie_result))
                else:
                    st.error("운세 정보를 가져올 수 없습니다.")
            except Exception as e:
                st.error(f"오류가 발생했습니다: {str(e)}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="site-section">', unsafe_allow_html=True)
            st.markdown('<div class="site-title">💎 엘르 코리아</div>', unsafe_allow_html=True)
            try:
                elle_result = scraper.get_elle_horoscope(date, zodiac)
                if elle_result:
                    st.write(elle_result)
                    horoscope_data.append(("엘르 코리아", elle_result))
                else:
                    st.error("운세 정보를 가져올 수 없습니다.")
            except Exception as e:
                st.error(f"오류가 발생했습니다: {str(e)}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="site-section">', unsafe_allow_html=True)
            st.markdown('<div class="site-title">💕 싱글즈 코리아</div>', unsafe_allow_html=True)
            try:
                singles_result = scraper.get_singles_horoscope(date, zodiac)
                if singles_result:
                    st.write(singles_result)
                    horoscope_data.append(("싱글즈 코리아", singles_result))
                else:
                    st.error("운세 정보를 가져올 수 없습니다.")
            except Exception as e:
                st.error(f"오류가 발생했습니다: {str(e)}")
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Claude API를 통한 종합 요약
    if horoscope_data:
        st.markdown('<div class="summary-section">', unsafe_allow_html=True)
        st.markdown('<div class="summary-title">🤖 AI 종합 요약</div>', unsafe_allow_html=True)
        
        with st.spinner("Claude AI가 종합 요약을 생성하는 중입니다..."):
            claude_api = ClaudeAPI()
            try:
                summary = claude_api.get_summary(horoscope_data, zodiac, date)
                if summary and "API 키가 설정되지 않았습니다" not in summary:
                    st.write(summary)
                else:
                    # Claude API가 없을 때 대체 요약 사용
                    st.warning("Claude API를 사용할 수 없습니다. 기본 요약을 제공합니다.")
                    from claude_api import create_simple_summary
                    simple_summary = create_simple_summary(horoscope_data, zodiac, date)
                    st.write(simple_summary)
            except Exception as e:
                st.error(f"요약 생성 중 오류가 발생했습니다: {str(e)}")
                # 오류 시에도 기본 요약 제공
                try:
                    from claude_api import create_simple_summary
                    simple_summary = create_simple_summary(horoscope_data, zodiac, date)
                    st.write(simple_summary)
                except Exception as e2:
                    st.error(f"기본 요약 생성도 실패했습니다: {str(e2)}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.error("운세 정보를 가져오지 못했습니다. 나중에 다시 시도해주세요.")

if __name__ == "__main__":
    main() 