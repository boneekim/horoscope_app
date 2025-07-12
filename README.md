# 🌟 별자리 운세 종합 보기

3개의 한국 주요 사이트에서 별자리 운세를 가져와서 Claude AI로 종합 요약해주는 웹 애플리케이션입니다.

## 📋 지원 사이트

- **마리끌레어 코리아**: 상세한 월별 운세 정보
- **엘르 코리아**: 패션과 라이프스타일을 중심으로 한 운세
- **싱글즈 코리아**: 연애와 인간관계 중심의 운세

## ✨ 주요 기능

- 📅 **날짜 선택**: 오늘 날짜 자동 설정 + 원하는 날짜 선택 가능
- 🌟 **별자리 선택**: 12개 별자리 드롭다운 메뉴
- 🔮 **운세 자동 수집**: 3개 사이트에서 동시에 운세 정보 수집
- 🤖 **AI 종합 요약**: Claude API를 통한 지능형 운세 요약
- 📱 **반응형 웹**: 데스크탑, 태블릿, 모바일 모두 지원

## 🚀 설치 및 실행

### 1. 필요 조건

- Python 3.7 이상
- pip 패키지 매니저

### 2. 설치

```bash
# 저장소 클론
git clone https://github.com/[your-username]/horoscope_app.git
cd horoscope_app

# 필요 패키지 설치
pip install -r requirements.txt
```

### 3. 환경 변수 설정

1. `env_example.txt` 파일을 `.env`로 복사:
```bash
cp env_example.txt .env
```

2. `.env` 파일을 열고 Claude API 키를 설정:
```
CLAUDE_API_KEY=your_actual_api_key_here
```

> **Claude API 키 발급 방법:**
> 1. [Anthropic Console](https://console.anthropic.com/)에 접속
> 2. 계정 생성 후 API 키 발급
> 3. 발급받은 키를 `.env` 파일에 입력

### 4. 실행

```bash
streamlit run main.py
```

브라우저에서 `http://localhost:8501`로 접속하여 사용할 수 있습니다.

## 📖 사용법

1. **날짜 선택**: 왼쪽 사이드바에서 원하는 날짜를 선택 (기본값: 오늘)
2. **별자리 선택**: 12개 별자리 중 하나를 선택
3. **별자리 보기**: 🔮 버튼을 클릭하여 운세 정보 수집
4. **결과 확인**: 3개 사이트별 운세와 AI 종합 요약 확인

## 🎯 화면 구성

- **사이드바**: 날짜 및 별자리 선택 메뉴
- **메인 화면**: 사용법 안내 및 운세 결과 표시
- **3컬럼 레이아웃**: 각 사이트별 운세 정보
- **종합 요약**: Claude AI가 생성한 통합 운세

## 🔧 주요 파일 구조

```
horoscope_app/
├── main.py              # 메인 Streamlit 앱
├── scraper.py           # 웹 스크래핑 모듈
├── claude_api.py        # Claude API 연동 모듈
├── requirements.txt     # 필요 패키지 목록
├── env_example.txt      # 환경 변수 예시
├── README.md           # 프로젝트 설명서
└── .gitignore          # Git 제외 파일 목록
```

## 🌟 12개 지원 별자리

- 물병자리 (1/20-2/18)
- 물고기자리 (2/19-3/20)
- 양자리 (3/21-4/19)
- 황소자리 (4/20-5/20)
- 쌍둥이자리 (5/21-6/21)
- 게자리 (6/22-7/22)
- 사자자리 (7/23-8/22)
- 처녀자리 (8/23-9/22)
- 천칭자리 (9/23-10/22)
- 전갈자리 (10/23-11/22)
- 궁수자리 (11/23-12/21)
- 염소자리 (12/22-1/19)

## 🛠️ 기술 스택

- **Frontend**: Streamlit
- **Web Scraping**: BeautifulSoup4, Requests
- **AI Integration**: Claude API (Anthropic)
- **Language**: Python 3.7+

## 📝 주의사항

1. **API 키 보안**: `.env` 파일은 절대 GitHub에 커밋하지 마세요
2. **사이트 정책**: 웹 스크래핑 시 각 사이트의 robots.txt를 준수합니다
3. **요청 제한**: 서버 부하 방지를 위해 요청 간 딜레이를 설정했습니다
4. **오류 처리**: 네트워크 오류 시 적절한 오류 메시지를 표시합니다

## 🤝 기여하기

1. 이 저장소를 Fork 하세요
2. 새로운 브랜치를 만드세요 (`git checkout -b feature/amazing-feature`)
3. 변경사항을 커밋하세요 (`git commit -m 'Add amazing feature'`)
4. 브랜치에 Push 하세요 (`git push origin feature/amazing-feature`)
5. Pull Request를 만드세요

## 📄 라이센스

이 프로젝트는 MIT 라이센스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

## 🐛 버그 리포트 및 기능 요청

- **버그 리포트**: [Issues](https://github.com/[your-username]/horoscope_app/issues)
- **기능 요청**: [Discussions](https://github.com/[your-username]/horoscope_app/discussions)

## 📞 연락처

- **개발자**: [Your Name]
- **이메일**: [your-email@example.com]
- **GitHub**: [your-github-username]

---

⭐ 이 프로젝트가 도움이 되었다면 GitHub에서 스타를 눌러주세요! 