#!/bin/bash

# 건양대학교 MBTI 전공 추천 시스템 - 개발 서버 실행 스크립트
# 작성일: 2024-11-18

set -e

echo "🎓 건양대학교 MBTI 전공 추천 시스템"
echo "======================================"

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 프로젝트 루트로 이동
cd "$(dirname "$0")"

echo -e "${BLUE}📁 프로젝트 디렉토리: $(pwd)${NC}"

# 가상환경 활성화
if [ -d ".venv" ]; then
    echo -e "${GREEN}✅ 가상환경 활성화 중...${NC}"
    source .venv/bin/activate
else
    echo -e "${RED}❌ 가상환경을 찾을 수 없습니다!${NC}"
    echo -e "${YELLOW}💡 다음 명령으로 가상환경을 생성하세요: python -m venv .venv${NC}"
    exit 1
fi

# Python 버전 확인
echo -e "${BLUE}🐍 Python 버전: $(python --version)${NC}"

# 의존성 설치 확인
if [ -f "requirements.txt" ]; then
    echo -e "${GREEN}📦 의존성 패키지 확인 중...${NC}"
    pip install -r requirements.txt --quiet
else
    echo -e "${YELLOW}⚠️  requirements.txt 파일이 없습니다${NC}"
fi

# 로그 디렉토리 생성
mkdir -p logs

# 환경 변수 설정
export ENVIRONMENT=development
export DEBUG=True

# 서버 종류 선택
echo ""
echo -e "${YELLOW}🚀 실행할 서버를 선택하세요:${NC}"
echo "1) Streamlit 서버 (기본 버전)"
echo "2) Streamlit 프리미엄 서버"
echo "3) 정적 웹서버 (HTML/CSS/JS)"
echo "4) 모든 서버 동시 실행"

read -p "선택 (1-4): " choice


# 퍼블릭 IP 자동 탐지
PUBLIC_IP=$(curl -s http://checkip.amazonaws.com)

case $choice in
    1)
        echo -e "${GREEN}🎯 Streamlit 기본 서버 실행...${NC}"
        echo -e "${BLUE}🌐 내부: http://localhost:8501${NC}"
        echo -e "${BLUE}🌐 외부: http://$PUBLIC_IP:8501${NC}"
        streamlit run server/app/main.py --server.port 8501 --server.address 0.0.0.0
        ;;
    2)
        echo -e "${GREEN}✨ Streamlit 프리미엄 서버 실행...${NC}"
        echo -e "${BLUE}🌐 내부: http://localhost:8502${NC}"
        echo -e "${BLUE}🌐 외부: http://$PUBLIC_IP:8502${NC}"
        streamlit run server/app/mbti_premium.py --server.port 8502 --server.address 0.0.0.0
        ;;
    3)
        echo -e "${GREEN}📄 정적 웹서버 실행...${NC}"
        echo -e "${BLUE}🌐 내부: http://localhost:8000${NC}"
        echo -e "${BLUE}🌐 외부: http://$PUBLIC_IP:8000${NC}"
        cd client
        python -m http.server 8000 --bind 0.0.0.0
        ;;
    4)
        echo -e "${GREEN}🚀 모든 서버 동시 실행...${NC}"
        echo -e "${BLUE}📍 Streamlit 기본: http://localhost:8501 (외부: http://$PUBLIC_IP:8501)${NC}"
        echo -e "${BLUE}📍 Streamlit 프리미엄: http://localhost:8502 (외부: http://$PUBLIC_IP:8502)${NC}"
        echo -e "${BLUE}📍 정적 웹서버: http://localhost:8000 (외부: http://$PUBLIC_IP:8000)${NC}"
        
        # 백그라운드로 서버들 실행
        streamlit run server/app/main.py --server.port 8501 --server.address 0.0.0.0 &
        streamlit run server/app/mbti_premium.py --server.port 8502 --server.address 0.0.0.0 &
        cd client && python -m http.server 8000 --bind 0.0.0.0 &
        
        echo -e "${GREEN}✅ 모든 서버가 시작되었습니다!${NC}"
        echo -e "${YELLOW}⚠️  종료하려면 Ctrl+C를 누르세요${NC}"
        wait
        ;;
    *)
        echo -e "${RED}❌ 잘못된 선택입니다${NC}"
        exit 1
        ;;
esac