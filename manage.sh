#!/bin/bash

# 건양대학교 MBTI 전공 추천 시스템 관리 스크립트
# 작성일: 2024-11-18

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 프로젝트 루트로 이동
cd "$(dirname "$0")"

# PID 파일 경로
STREAMLIT_PID="pids/streamlit.pid"
STATIC_PID="pids/static_server.pid"

# 함수 정의
check_status() {
    echo -e "${BLUE}🔍 서버 상태 확인${NC}"
    echo "===================="
    
    if [ -f "$STREAMLIT_PID" ]; then
        pid=$(cat "$STREAMLIT_PID")
        if ps -p "$pid" > /dev/null; then
            echo -e "${GREEN}✅ Streamlit 서버: 실행 중 (PID: $pid)${NC}"
        else
            echo -e "${RED}❌ Streamlit 서버: 중지됨${NC}"
            rm -f "$STREAMLIT_PID"
        fi
    else
        echo -e "${RED}❌ Streamlit 서버: 중지됨${NC}"
    fi
    
    if [ -f "$STATIC_PID" ]; then
        pid=$(cat "$STATIC_PID")
        if ps -p "$pid" > /dev/null; then
            echo -e "${GREEN}✅ 정적 웹서버: 실행 중 (PID: $pid)${NC}"
        else
            echo -e "${RED}❌ 정적 웹서버: 중지됨${NC}"
            rm -f "$STATIC_PID"
        fi
    else
        echo -e "${RED}❌ 정적 웹서버: 중지됨${NC}"
    fi
    
    echo ""
    echo -e "${BLUE}📊 포트 사용 현황:${NC}"
    echo "포트 8501: $(lsof -ti:8501 > /dev/null && echo -e "${GREEN}사용 중${NC}" || echo -e "${RED}사용 안함${NC}")"
    echo "포트 8000: $(lsof -ti:8000 > /dev/null && echo -e "${GREEN}사용 중${NC}" || echo -e "${RED}사용 안함${NC}")"
}

stop_servers() {
    echo -e "${YELLOW}🛑 서버 종료 중...${NC}"
    
    if [ -f "$STREAMLIT_PID" ]; then
        pid=$(cat "$STREAMLIT_PID")
        if ps -p "$pid" > /dev/null; then
            echo -e "${BLUE}⏹️  Streamlit 서버 종료 (PID: $pid)${NC}"
            kill "$pid"
            sleep 2
            if ps -p "$pid" > /dev/null; then
                kill -9 "$pid"
            fi
        fi
        rm -f "$STREAMLIT_PID"
    fi
    
    if [ -f "$STATIC_PID" ]; then
        pid=$(cat "$STATIC_PID")
        if ps -p "$pid" > /dev/null; then
            echo -e "${BLUE}⏹️  정적 웹서버 종료 (PID: $pid)${NC}"
            kill "$pid"
        fi
        rm -f "$STATIC_PID"
    fi
    
    echo -e "${GREEN}✅ 모든 서버가 종료되었습니다${NC}"
}

show_logs() {
    echo -e "${BLUE}📊 로그 파일 보기${NC}"
    echo "=================="
    echo "1) Streamlit 로그"
    echo "2) 정적 웹서버 로그"
    echo "3) 모든 로그"
    
    read -p "선택 (1-3): " choice
    
    case $choice in
        1)
            if [ -f "logs/streamlit.log" ]; then
                echo -e "${BLUE}📄 Streamlit 로그 (마지막 50줄):${NC}"
                tail -50 logs/streamlit.log
            else
                echo -e "${RED}❌ Streamlit 로그 파일이 없습니다${NC}"
            fi
            ;;
        2)
            if [ -f "logs/static_server.log" ]; then
                echo -e "${BLUE}📄 정적 웹서버 로그 (마지막 50줄):${NC}"
                tail -50 logs/static_server.log
            else
                echo -e "${RED}❌ 정적 웹서버 로그 파일이 없습니다${NC}"
            fi
            ;;
        3)
            echo -e "${BLUE}📄 모든 로그:${NC}"
            if [ -f "logs/streamlit.log" ]; then
                echo -e "${YELLOW}=== Streamlit 로그 ===${NC}"
                tail -25 logs/streamlit.log
            fi
            if [ -f "logs/static_server.log" ]; then
                echo -e "${YELLOW}=== 정적 웹서버 로그 ===${NC}"
                tail -25 logs/static_server.log
            fi
            ;;
    esac
}

restart_servers() {
    echo -e "${YELLOW}🔄 서버 재시작 중...${NC}"
    stop_servers
    sleep 3
    ./run_prod.sh
}

cleanup() {
    echo -e "${BLUE}🧹 시스템 정리 중...${NC}"
    stop_servers
    
    # 로그 파일 정리
    if [ -d "logs" ]; then
        find logs -name "*.log" -type f -mtime +7 -delete
        echo -e "${GREEN}📄 7일 이상된 로그 파일 삭제됨${NC}"
    fi
    
    # 임시 파일 정리
    find . -name "*.pyc" -delete
    find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
    
    echo -e "${GREEN}✅ 정리 완료${NC}"
}

# 메인 명령어 처리
case "$1" in
    status|s)
        check_status
        ;;
    stop)
        stop_servers
        ;;
    restart|r)
        restart_servers
        ;;
    logs|l)
        show_logs
        ;;
    cleanup|clean)
        cleanup
        ;;
    *)
        echo -e "${BLUE}🎓 건양대학교 MBTI 전공 추천 시스템 관리 도구${NC}"
        echo "============================================="
        echo ""
        echo -e "${YELLOW}사용법: $0 [명령어]${NC}"
        echo ""
        echo -e "${GREEN}명령어:${NC}"
        echo "  status, s      - 서버 상태 확인"
        echo "  stop          - 모든 서버 종료"
        echo "  restart, r    - 서버 재시작"
        echo "  logs, l       - 로그 파일 보기"
        echo "  cleanup, clean - 시스템 정리"
        echo ""
        echo -e "${BLUE}예시:${NC}"
        echo "  $0 status     # 서버 상태 확인"
        echo "  $0 stop       # 서버 종료"
        echo "  $0 logs       # 로그 확인"
        ;;
esac