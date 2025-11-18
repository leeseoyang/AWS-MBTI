import streamlit as st
import numpy as np
from typing import Dict, List, Tuple

st.set_page_config(
    page_title="✨ 건양대학교 MBTI 전공 추천 시스템",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 전문적인 CSS 스타일링 적용
st.markdown("""
<style>
    /* 전체 페이지 스타일 */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* 헤더 스타일 */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    .main-header p {
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
        opacity: 0.9;
    }
    
    /* 질문 카드 스타일 */
    .question-card {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        border: 1px solid #e8ecf0;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .question-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 35px rgba(0,0,0,0.15);
    }
    
    .question-number {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        text-align: center;
        line-height: 40px;
        font-weight: bold;
        font-size: 1.1rem;
        margin-bottom: 1rem;
    }
    
    .question-text {
        font-size: 1.2rem;
        font-weight: 600;
        color: #2c3e50;
        line-height: 1.6;
        margin-bottom: 1.5rem;
    }
    
    /* 선택 옵션 스타일 */
    .stSelectbox > div > div {
        border: 2px solid #e8ecf0;
        border-radius: 10px;
        font-size: 1rem;
        background: #f8f9fa;
    }
    
    .stSelectbox > div > div:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* 결과 카드 스타일 */
    .result-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        margin: 2rem 0;
        text-align: center;
        box-shadow: 0 10px 30px rgba(240, 147, 251, 0.3);
    }
    
    .mbti-result {
        font-size: 3rem;
        font-weight: 800;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        margin-bottom: 1rem;
        letter-spacing: 3px;
    }
    
    .mbti-description {
        font-size: 1.3rem;
        opacity: 0.9;
        line-height: 1.6;
    }
    
    /* 추천 학과 카드 */
    .recommendation-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 6px 20px rgba(0,0,0,0.1);
        border-left: 5px solid #667eea;
        transition: transform 0.2s ease;
    }
    
    .recommendation-card:hover {
        transform: translateX(5px);
    }
    
    .recommendation-rank {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.9rem;
        display: inline-block;
        margin-bottom: 0.8rem;
    }
    
    .recommendation-major {
        font-size: 1.4rem;
        font-weight: 700;
        color: #2c3e50;
        margin-bottom: 0.5rem;
    }
    
    .recommendation-score {
        color: #7f8c8d;
        font-size: 1rem;
        font-weight: 500;
    }
    
    /* 프로그레스 바 */
    .progress-container {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        text-align: center;
    }
    
    .progress-text {
        color: #667eea;
        font-weight: 600;
        font-size: 1.1rem;
    }
    
    /* 버튼 스타일 */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.8rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* 추가 정보 스타일 */
    .info-box {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #17a2b8;
    }
    
    .info-box h4 {
        color: #17a2b8;
        margin-bottom: 0.8rem;
        font-weight: 600;
    }
    
    /* 애니메이션 */
    .fade-in {
        animation: fadeIn 0.8s ease-in-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* 반응형 디자인 */
    @media (max-width: 768px) {
        .main-header h1 { font-size: 2rem; }
        .mbti-result { font-size: 2.5rem; }
        .question-text { font-size: 1.1rem; }
    }
</style>
""", unsafe_allow_html=True)

# 메인 헤더
st.markdown("""
<div class="main-header fade-in">
    <h1>🎓 건양대학교 MBTI 전공 추천 시스템</h1>
    <p>AI가 분석하는 나만의 완벽한 전공 찾기 ✨</p>
</div>
""", unsafe_allow_html=True)

# 소개 섹션
st.markdown("""
<div class="info-box fade-in">
    <h4>🔍 정확한 MBTI 검사를 위한 안내</h4>
    <p>• 각 질문에 대해 <strong>첫 번째 직감</strong>으로 답변해주세요</p>
    <p>• 이상적인 모습이 아닌 <strong>현재 실제 모습</strong>을 기준으로 선택해주세요</p>
    <p>• 32개 질문을 모두 답변하시면 AI가 맞춤형 전공을 추천해드립니다</p>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# 1) 32개 문항
# ------------------------------------------------------------

questions = {
    "IE": [
        "혼자서 집중하는 시간이 편하다.",
        "깊고 진지한 대화를 선호한다.",
        "조용한 곳에서 공부가 잘 된다.",
        "발표보다 글로 표현하는 것이 익숙하다.",
        "혼자서 문제를 해결하는 편이다.",
        "대답하기 전에 한 번 생각한다.",
        "새로운 사람을 만나는 데 시간이 필요하다.",
        "개인 시간 확보가 중요하다."
    ],
    "SN": [
        "실제 데이터와 사실 기반 정보를 선호한다.",
        "단계별 절차를 따르는 것이 편하다.",
        "손으로 만져보고 배우는 게 빠르다.",
        "현재 실천 가능한 것이 중요하다.",
        "구체적인 예시가 있어야 이해가 된다.",
        "현실적이고 실용적인 선택을 한다.",
        "기존 방식이 안정적이다.",
        "세부 사항을 꼼꼼히 살핀다."
    ],
    "TF": [
        "결정을 할 때 논리·분석이 우선이다.",
        "데이터 중심의 판단을 선호한다.",
        "솔직하고 직선적인 말이 좋다.",
        "효율이 중요하다.",
        "갈등을 논리로 해결한다.",
        "경쟁적 환경이 동기부여된다.",
        "문제를 해결할 때 감정 배제 가능하다.",
        "결과가 중요한 편이다."
    ],
    "JP": [
        "계획을 세우고 움직인다.",
        "마감 전에 미리 끝내는 편이다.",
        "해야 할 일을 목록으로 정리한다.",
        "정리정돈이 잘 되어 있어야 한다.",
        "루틴이 중요하다.",
        "한 번 정하면 지키려 한다.",
        "안정성과 확실함이 중요하다.",
        "계획적인 일정이 편하다."
    ]
}

# ------------------------------------------------------------
# 2) Streamlit UI - 질문 출력
# ------------------------------------------------------------

st.header("📝 32문항 MBTI 성향 체크")

responses: Dict[str, List[str]] = {"IE": [], "SN": [], "TF": [], "JP": []}

with st.form("mbti_test"):
    st.subheader("I / E 문항")
    for q in questions["IE"]:
        responses["IE"].append(
            st.radio(q, ["A (I)", "B (E)"], key=q)
        )

    st.subheader("S / N 문항")
    for q in questions["SN"]:
        responses["SN"].append(
            st.radio(q, ["A (S)", "B (N)"], key=q)
        )

    st.subheader("T / F 문항")
    for q in questions["TF"]:
        responses["TF"].append(
            st.radio(q, ["A (T)", "B (F)"], key=q)
        )

    st.subheader("J / P 문항")
    for q in questions["JP"]:
        responses["JP"].append(
            st.radio(q, ["A (J)", "B (P)"], key=q)
        )

    submitted = st.form_submit_button("결과 확인하기")

# ------------------------------------------------------------
# 3) MBTI 계산 함수
# ------------------------------------------------------------

def calc_mbti(res: Dict[str, List[str]]) -> str:
    I = sum([1 for r in res["IE"] if "I" in r])
    E = sum([1 for r in res["IE"] if "E" in r])
    S = sum([1 for r in res["SN"] if "S" in r])
    N = sum([1 for r in res["SN"] if "N" in r])
    T = sum([1 for r in res["TF"] if "T" in r])
    F = sum([1 for r in res["TF"] if "F" in r])
    J = sum([1 for r in res["JP"] if "J" in r])
    P = sum([1 for r in res["JP"] if "P" in r])

    type_IE = "I" if I > E else "E"
    type_SN = "S" if S > N else "N"
    type_TF = "T" if T > F else "F"
    type_JP = "J" if J > P else "P"

    return type_IE + type_SN + type_TF + type_JP

# ------------------------------------------------------------
# 4) MBTI → 28개 학과 매핑 테이블
# ------------------------------------------------------------

MBTI_TO_MAJOR = {
    "ISTJ": ["의료신소재학과", "의료공학과", "국방반도체공학과", "방위산업공학부", "국방경찰행정학부"],
    "ISFJ": ["스포츠의학전공", "재활퍼스널트레이닝학과", "사회복지학과", "유아교육과", "특수교육과"],
    "INFJ": ["심리상담치료학과", "사회복지학과", "임상의약바이오학과"],
    "INTJ": ["인공지능학과", "의료IT공학과", "제약생명공학과", "식품생명공학과"],
    "ISTP": ["유무인항공공학과", "스마트보안학과", "국방XR학부", "의료공학과", "국방반도체공학과"],
    "ISFP": ["의료공간디자인학과", "ND산업디자인학부", "재활퍼스널트레이닝학과", "스포츠의학전공"],
    "INFP": ["임상의약바이오학과", "식품생명공학과", "심리상담치료학과", "특수교육과"],
    "INTP": ["인공지능학과", "기업소프트웨어학부", "스마트보안학과", "의료IT공학과"],
    "ESTP": ["재난안전소방학전공", "군사학과", "국방경찰행정학부", "유무인항공공학과", "스포츠의학전공"],
    "ESFP": ["유아교육과", "스포츠의학전공", "글로벌의료뷰티학전공", "재활퍼스널트레이닝학과"],
    "ENFP": ["스마트팜학부", "의료공간디자인학과", "ND산업디자인학부", "국방XR학부"],
    "ENTP": ["인공지능학과", "스마트보안학과", "기업소프트웨어학부", "의료IT공학과"],
    "ESTJ": ["국방산업경영학부", "군사학과", "방위산업공학부", "의료신소재학과"],
    "ESFJ": ["사회복지학과", "심리상담치료학과", "유아교육과", "글로벌의료뷰티학전공"],
    "ENFJ": ["국방경찰행정학부", "사회복지학과", "교육계열", "스포츠의학전공"],
    "ENTJ": ["인공지능학과", "스마트보안학과", "공학계열 전체", "국방산업경영학부"]
}

# ------------------------------------------------------------
# 5) 학과 성향 벡터 (AI 점수 계산용)
# ------------------------------------------------------------

major_vectors: Dict[str, List[float]] = {
    "의료신소재학과": [1,1,1,1],
    "의료공학과": [1,1,1,1],
    "의료IT공학과": [1,0,1,1],
    "의료공간디자인학과": [0.5,0,0,0],
    "ND산업디자인학부": [0.5,0,0,0],
    "제약생명공학과": [1,0,1,1],
    "식품생명공학과": [1,0,1,1],
    "임상의약바이오학과": [1,0,0.5,1],
    "인공지능학과": [1,0,1,0.6],
    "스마트보안학과": [1,0.5,1,1],
    "기업소프트웨어학부": [1,0,1,0],
    "국방XR학부": [0.5,0,1,0],
    "스마트팜학부": [0.5,0,1,0],
    "유무인항공공학과": [0.7,1,1,0],
    "국방반도체공학과": [1,1,1,1],
    "국방산업경영학부": [0,0.5,1,1],
    "국방경찰행정학부": [0,1,1,1],
    "재난안전소방학전공": [0,1,1,0],
    "군사학과": [0,1,1,1],
    "사회복지학과": [0,0.5,0,1],
    "심리상담치료학과": [0,0,0,1],
    "유아교육과": [0,0,0,1],
    "특수교육과": [0,0,0,1],
    "글로벌의료뷰티학전공": [0,0,0,0],
    "재활퍼스널트레이닝학과": [0,1,0,0.5],
    "스포츠의학전공": [0,1,0,0]
}

# ------------------------------------------------------------
# 6) 유사도 계산 함수 (코사인 유사도)
# ------------------------------------------------------------

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """코사인 유사도를 계산하는 함수"""
    dot_product = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    
    if norm_a == 0 or norm_b == 0:
        return 0.0
        
    return float(dot_product / (norm_a * norm_b))

# ------------------------------------------------------------
# 7) 결과 출력
# ------------------------------------------------------------

if submitted:
    # MBTI 계산
    mbti = calc_mbti(responses)
    st.success(f"📌 당신의 MBTI 유형: **{mbti}**")

    st.subheader("🎓 1차 추천 학과 (MBTI 기반)")
    first_majors = MBTI_TO_MAJOR.get(mbti, [])
    st.write(first_majors)

    # 2차 추천 (코사인 유사도)
    # MBTI → 벡터 변환
    mbti_vec = [
        1 if mbti[0]=="I" else 0,
        1 if mbti[1]=="S" else 0,
        1 if mbti[2]=="T" else 0,
        1 if mbti[3]=="J" else 0,
    ]

    scores: List[Tuple[str, float]] = []
    for major, vec in major_vectors.items():
        sim = cosine_similarity(np.array(mbti_vec), np.array(vec))
        scores.append((major, sim))

    scores = sorted(scores, key=lambda x: x[1], reverse=True)

    st.subheader("🏆 AI 기반 최종 추천 TOP 3")
    for i, (major, score) in enumerate(scores[:3], start=1):
        st.markdown(f"**{i}. {major}** (유사도: {score:.3f})")

    st.subheader("📌 추가 고려 학과")
    st.write([m for m, _ in scores[3:6]])