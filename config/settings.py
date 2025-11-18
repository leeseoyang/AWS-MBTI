"""
건양대학교 MBTI 전공 추천 시스템 설정 파일
"""
import os
from pathlib import Path
from typing import Dict, List, Any, Union

# 프로젝트 루트 디렉토리
BASE_DIR = Path(__file__).resolve().parent.parent

# 환경 설정
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'

# 서버 설정
SERVER_HOST = os.getenv('SERVER_HOST', '0.0.0.0')
SERVER_PORT = int(os.getenv('SERVER_PORT', '8501'))

# Streamlit 설정
STREAMLIT_CONFIG: Dict[str, Union[int, str, bool]] = {
    'server.port': SERVER_PORT,
    'server.address': SERVER_HOST,
    'server.headless': True,
    'browser.gatherUsageStats': False,
    'theme.primaryColor': '#667eea',
    'theme.backgroundColor': '#ffffff',
    'theme.secondaryBackgroundColor': '#f8f9fa',
    'theme.textColor': '#2c3e50'
}

# 데이터베이스 설정 (향후 확장용)
DATABASE_CONFIG: Dict[str, Union[str, int]] = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', '5432')),
    'name': os.getenv('DB_NAME', 'mbti_db'),
    'user': os.getenv('DB_USER', 'admin'),
    'password': os.getenv('DB_PASSWORD', 'password')
}

# 로깅 설정
LOGGING_CONFIG: Dict[str, Any] = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'detailed': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
        'simple': {
            'format': '%(levelname)s - %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'simple'
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'app.log',
            'level': 'DEBUG',
            'formatter': 'detailed'
        }
    },
    'loggers': {
        'app': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False
        }
    }
}

# MBTI 관련 설정
MBTI_CONFIG: Dict[str, Union[int, List[str], float]] = {
    'total_questions': 32,
    'question_categories': ['EI', 'SN', 'TF', 'JP'],
    'questions_per_category': 8,
    'similarity_threshold': 0.7,
    'max_recommendations': 5
}

# 보안 설정
SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# API 설정 (향후 확장용)
API_CONFIG: Dict[str, Union[str, int]] = {
    'rate_limit': '100/hour',
    'timeout': 30,
    'max_retries': 3
}

# 정적 파일 경로
STATIC_DIRS = {
    'client': BASE_DIR / 'client' / 'static',
    'server': BASE_DIR / 'server' / 'app' / 'static'
}

# 템플릿 경로
TEMPLATE_DIR = BASE_DIR / 'server' / 'app' / 'templates'

# 캐시 설정
CACHE_CONFIG: Dict[str, Union[str, int]] = {
    'type': 'simple',
    'ttl': 3600,  # 1시간
    'max_size': 1000
}