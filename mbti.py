import streamlit as st
import numpy as np
from typing import Dict, List, Tuple

st.set_page_config(
    page_title="🎓 건양대학교 전과 적성 진단 질문지",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 전문적인 CSS 스타일링 적용
st.markdown("""
<style>
body, .main .block-container {
    font-family: 'Gmarket Sans', 'Pretendard', 'Noto Sans KR', sans-serif !important;
    background: linear-gradient(135deg, #fbc2eb 0%, #a7f3d0 100%) !important;
}
.main-header {
    background: linear-gradient(135deg, #a7f3d0 0%, #fbc2eb 100%);
    padding: 2.5rem 2rem 1.5rem 2rem;
    border-radius: 2.5rem;
    margin-bottom: 2rem;
    color: #222;
    text-align: center;
    box-shadow: 0 10px 30px rgba(167,243,208,0.18);
    border: 1.5px solid #fbc2eb;
}
.main-header h1 {
    margin: 0;
    font-size: 2.7rem;
    font-weight: 900;
    text-shadow: 0 2px 16px rgba(167,243,208,0.18);
    letter-spacing: 0.03em;
}
.main-header p {
    margin: 0.5rem 0 0 0;
    font-size: 1.15rem;
    opacity: 0.9;
    font-weight: 500;
}
.info-box {
    background: linear-gradient(90deg, #fef9c3 0%, #bae6fd 100%);
    border-radius: 1.5rem;
    box-shadow: 0 4px 24px rgba(96,165,250,0.10);
    padding: 2rem 1.5rem;
    margin-bottom: 2rem;
    border: 1.5px solid #bae6fd;
}
.info-box h4 {
    color: #38bdf8;
    margin-bottom: 0.8rem;
    font-weight: 700;
}
.question-card {
    background: linear-gradient(135deg, #fbc2eb 0%, #a7f3d0 100%);
    border-radius: 2rem;
    padding: 2rem;
    margin: 1rem 0;
    box-shadow: 0 8px 25px rgba(96,165,250,0.12);
    border: 1.5px solid #fbc2eb;
    transition: transform 0.3s, box-shadow 0.3s;
    position: relative;
}
.question-card:hover {
    transform: scale(1.04) translateY(-2px);
    box-shadow: 0 12px 35px rgba(96,165,250,0.18);
}
.question-number {
    display: inline-block;
    background: linear-gradient(135deg, #38bdf8 60%, #facc15 100%);
    color: #fff;
    width: 44px;
    height: 44px;
    border-radius: 50%;
    text-align: center;
    line-height: 44px;
    font-weight: bold;
    font-size: 1.2rem;
    margin-bottom: 1rem;
    border: 2.5px solid #fff;
    box-shadow: 0 2px 8px rgba(96,165,250,0.12);
}
.question-text {
    font-size: 1.25rem;
    font-weight: 600;
    color: #222;
    line-height: 1.6;
    margin-bottom: 1.5rem;
    text-shadow: 0 2px 8px rgba(96,165,250,0.10);
}
.stRadio > div {
    background: #fff;
    border-radius: 1.2rem;
    box-shadow: 0 2px 8px rgba(96,165,250,0.08);
    border: 2px solid #facc15;
    margin-bottom: 0.7rem;
    padding: 0.7rem 1.2rem;
    font-size: 1.1rem;
    font-weight: 500;
    transition: all 0.25s cubic-bezier(0.4,0,0.2,1);
    position: relative;
}
.stRadio > div:hover {
    background: linear-gradient(90deg, #bae6fd 60%, #fef9c3 100%);
    color: #38bdf8;
    border-color: #38bdf8;
    box-shadow: 0 4px 16px rgba(96,165,250,0.18);
    transform: scale(1.06);
}
.stRadio > div[aria-checked="true"] {
    background: linear-gradient(90deg, #4ade80 60%, #38bdf8 100%);
    color: #fff;
    border-color: #4ade80;
    box-shadow: 0 0 0 4px rgba(74,222,128,0.15);
    font-weight: 700;
}
.stRadio > div[aria-checked="true"]::before {
    content: '✅';
    position: absolute;
    left: 12px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 1.1rem;
}
.result-card {
    background: linear-gradient(135deg, #bae6fd 0%, #fef9c3 100%);
    color: #222;
    padding: 2rem;
    border-radius: 2rem;
    margin: 2rem 0;
    text-align: center;
    box-shadow: 0 10px 30px rgba(96,165,250,0.18);
    border: 1.5px solid #bae6fd;
}
.mbti-result {
    font-size: 3rem;
    font-weight: 800;
    text-shadow: 0 2px 4px rgba(96,165,250,0.10);
    margin-bottom: 1rem;
    letter-spacing: 3px;
    color: #38bdf8;
}
.mbti-description {
    font-size: 1.3rem;
    opacity: 0.9;
    line-height: 1.6;
}
.recommendation-card {
    background: #fff;
    border-radius: 1.5rem;
    padding: 1.5rem;
    margin: 1rem 0;
    box-shadow: 0 6px 20px rgba(96,165,250,0.10);
    border-left: 5px solid #38bdf8;
    transition: transform 0.2s;
}
.recommendation-card:hover {
    transform: scale(1.03) translateX(5px);
}
.recommendation-rank {
    background: linear-gradient(135deg, #38bdf8 0%, #facc15 100%);
    color: #fff;
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
    color: #222;
    margin-bottom: 0.5rem;
}
.recommendation-score {
    color: #7f8c8d;
    font-size: 1rem;
    font-weight: 500;
}
.progress-container {
    background: linear-gradient(90deg, #fef9c3 0%, #bae6fd 100%);
    border-radius: 1rem;
    padding: 1rem;
    margin: 1rem 0;
    text-align: center;
    box-shadow: 0 1px 4px rgba(96,165,250,0.10);
}
.progress-text {
    color: #38bdf8;
    font-weight: 700;
    font-size: 1.1rem;
    letter-spacing: 0.02em;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.progress-text::before {
    content: '📝';
    font-size: 1.1rem;
}
.stButton > button {
    background: linear-gradient(135deg, #38bdf8 0%, #facc15 100%);
    color: #fff;
    border: none;
    border-radius: 1rem;
    padding: 0.8rem 2rem;
    font-size: 1.1rem;
    font-weight: 700;
    transition: transform 0.2s, box-shadow 0.2s;
    box-shadow: 0 4px 15px rgba(56,189,248,0.18);
}
.stButton > button:hover {
    transform: scale(1.07) translateY(-2px);
    box-shadow: 0 6px 20px rgba(56,189,248,0.28);
}
.fade-in {
    animation: fadeIn 0.8s ease-in-out;
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}
@media (max-width: 768px) {
    .main-header h1 { font-size: 2rem; }
    .mbti-result { font-size: 2.2rem; }
    .question-text { font-size: 1.05rem; }
    .question-card { padding: 1.2rem; }
}
</style>
""", unsafe_allow_html=True)

# 메인 헤더
st.markdown("""
<div class="main-header fade-in">
    <h1>🎓 건양대학교 전과 적성 진단 질문지</h1>
</div>
""", unsafe_allow_html=True)

# 안내문 섹션
st.markdown("""
<div class="info-box fade-in">
    <h4>📌 안내문</h4>
    <p style="line-height: 1.8; margin-bottom: 1rem;">
    본 질문지는 건양대학교 재학생의 전과 준비를 지원하기 위해 제작되었습니다.<br>
    학생 개개인의 성향 및 학습 스타일을 간단히 파악하여,<br>
    전과가 가능한 학과 중 학생에게 적합한 전공 방향을 예비적으로 제시하는 것을 목적으로 합니다.
    </p>
    
    <p style="margin-top: 1.5rem; font-weight: 600;"><strong>아래의 내용을 확인한 후 응답해 주시기 바랍니다.</strong></p>
    
    <ol style="margin-left: 1.5rem; line-height: 1.8; margin-bottom: 1.5rem;">
        <li>각 문항은 현재 본인의 모습을 기준으로 선택해 주십시오.</li>
        <li>응답은 가급적 첫 느낌에 가장 가까운 항목으로 선택하는 것을 권장합니다.</li>
        <li>질문지 결과는 전과 지원의 자격 및 선발 여부와 무관하며,<br>
        학생의 전공 탐색을 돕기 위한 참고용 자료로 제공됩니다.</li>
        <li>모든 문항에 응답할 경우, 입력된 답변을 기반으로<br>
        학생의 성향 분석에 따른 전공 추천 결과가 안내됩니다.</li>
    </ol>
    
    <p style="margin-top: 1.5rem; font-weight: 700; color: #38bdf8;">
    학생 여러분의 성실한 응답은 향후 전과 준비 및 전공 선택에 유의미한 도움이 될 것입니다.
    </p>
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
    for idx, q in enumerate(questions["IE"]):
        responses["IE"].append(
            st.radio(q, ["A (I)", "B (E)"], key=f"IE_{idx}", index=None)
        )

    st.subheader("S / N 문항")
    for idx, q in enumerate(questions["SN"]):
        responses["SN"].append(
            st.radio(q, ["A (S)", "B (N)"], key=f"SN_{idx}", index=None)
        )

    st.subheader("T / F 문항")
    for idx, q in enumerate(questions["TF"]):
        responses["TF"].append(
            st.radio(q, ["A (T)", "B (F)"], key=f"TF_{idx}", index=None)
        )

    st.subheader("J / P 문항")
    for idx, q in enumerate(questions["JP"]):
        responses["JP"].append(
            st.radio(q, ["A (J)", "B (P)"], key=f"JP_{idx}", index=None)
        )

    submitted = st.form_submit_button("결과 확인하기")

# ------------------------------------------------------------
# 3) MBTI 계산 함수
# ------------------------------------------------------------

def calc_mbti(res: Dict[str, List[str]]) -> str:
    I = sum([1 for r in res["IE"] if r and "I" in r])
    E = sum([1 for r in res["IE"] if r and "E" in r])
    S = sum([1 for r in res["SN"] if r and "S" in r])
    N = sum([1 for r in res["SN"] if r and "N" in r])
    T = sum([1 for r in res["TF"] if r and "T" in r])
    F = sum([1 for r in res["TF"] if r and "F" in r])
    J = sum([1 for r in res["JP"] if r and "J" in r])
    P = sum([1 for r in res["JP"] if r and "P" in r])

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