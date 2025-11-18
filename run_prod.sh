#!/bin/bash

# 건양대학교 MBTI 전공 추천 시스템 - 운영 서버 실행 스크립트
# 작성일: 2024-11-18

set -e

echo "🎓 건양대학교 MBTI 전공 추천 시스템 [운영 모드]"
echo "==============================================="

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 프로젝트 루트로 이동
cd "$(dirname "$0")"

# 환경 변수 설정
export ENVIRONMENT=production
export DEBUG=False

# 가상환경 활성화
if [ -d ".venv" ]; then
    echo -e "${GREEN}✅ 가상환경 활성화 중...${NC}"
    source .venv/bin/activate
else
    echo -e "${RED}❌ 가상환경을 찾을 수 없습니다!${NC}"
    exit 1
fi

# 의존성 설치
echo -e "${GREEN}📦 프로덕션 의존성 설치 중...${NC}"
pip install -r requirements.txt

# 로그 디렉토리 생성
mkdir -p logs

# 프로세스 ID 저장 디렉토리
mkdir -p pids

echo -e "${GREEN}🚀 프로덕션 서버 시작...${NC}"

# Streamlit 서버를 백그라운드에서 실행
nohup streamlit run server/app/mbti_premium.py \
    --server.port 8501 \
    --server.address 0.0.0.0 \
    --server.headless true \
    --browser.gatherUsageStats false \
    > logs/streamlit.log 2>&1 & 
echo $! > pids/streamlit.pid

# 정적 웹서버를 백그라운드에서 실행  
cd client
nohup python -m http.server 8000 \
    > ../logs/static_server.log 2>&1 &
echo $! > ../pids/static_server.pid
cd ..

sleep 3

echo -e "${GREEN}✅ 서버가 성공적으로 시작되었습니다!${NC}"
echo ""
echo -e "${BLUE}📍 서비스 URL:${NC}"
echo -e "   🎯 MBTI 테스트: http://localhost:8501"
echo -e "   📄 정적 사이트: http://localhost:8000"
echo ""
echo -e "${YELLOW}📋 관리 명령어:${NC}"
echo -e "   🔍 상태 확인: ./manage.sh status"
echo -e "   🛑 서버 종료: ./manage.sh stop"
echo -e "   📊 로그 확인: ./manage.sh logs"
echo ""
echo -e "${YELLOW}📁 로그 파일:${NC}"
echo -e "   📄 logs/streamlit.log"
echo -e "   📄 logs/static_server.log"