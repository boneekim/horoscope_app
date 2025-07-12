#!/usr/bin/env python3
"""
별자리 운세 종합 보기 실행 스크립트
"""

import os
import sys
import subprocess

def check_requirements():
    """필요 패키지가 설치되어 있는지 확인"""
    try:
        import streamlit
        import requests
        import bs4
        import dotenv
        print("✅ 모든 필요 패키지가 설치되어 있습니다.")
        return True
    except ImportError as e:
        print(f"❌ 필요 패키지가 설치되지 않았습니다: {e}")
        print("다음 명령어를 실행하여 패키지를 설치하세요:")
        print("pip install -r requirements.txt")
        return False

def check_env_file():
    """환경 변수 파일 확인"""
    if os.path.exists('.env'):
        print("✅ .env 파일이 존재합니다.")
        return True
    else:
        print("⚠️  .env 파일이 없습니다.")
        print("env_example.txt 파일을 .env로 복사하고 Claude API 키를 설정하세요.")
        return False

def main():
    print("🌟 별자리 운세 종합 보기 시작 🌟")
    print("=" * 50)
    
    # 요구사항 확인
    if not check_requirements():
        return
    
    # 환경 변수 파일 확인
    check_env_file()
    
    print("\n🚀 Streamlit 앱을 시작합니다...")
    print("브라우저에서 http://localhost:8501 을 열어주세요.")
    print("종료하려면 Ctrl+C를 누르세요.")
    print("=" * 50)
    
    # Streamlit 앱 실행
    try:
        subprocess.run(["python3", "-m", "streamlit", "run", "main.py"])
    except KeyboardInterrupt:
        print("\n\n👋 앱이 종료되었습니다.")
    except Exception as e:
        print(f"\n❌ 오류가 발생했습니다: {e}")

if __name__ == "__main__":
    main() 