import streamlit as st
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
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap');
    
    /* 전체 페이지 스타일 */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
        font-family: 'Noto Sans KR', sans-serif;
    }
    
    /* 헤더 스타일 */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 25px;
        margin-bottom: 3rem;
        color: white;
        text-align: center;
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.4);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: pulse 4s ease-in-out infinite;
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 3rem;
        font-weight: 900;
        text-shadow: 0 3px 6px rgba(0,0,0,0.3);
        position: relative;
        z-index: 2;
    }
    
    .main-header p {
        margin: 1rem 0 0 0;
        font-size: 1.3rem;
        opacity: 0.95;
        position: relative;
        z-index: 2;
        font-weight: 400;
    }
    
    /* 질문 카드 스타일 */
    .question-card {
        background: white;
        border-radius: 20px;
        padding: 2.5rem;
        margin: 1.5rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        border: 1px solid rgba(102, 126, 234, 0.1);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
    }
    
    .question-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2);
    }
    
    .question-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 20px 40px rgba(0,0,0,0.15);
    }
    
    .question-number {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        width: 50px;
        height: 50px;
        border-radius: 25px;
        font-weight: 700;
        font-size: 1.2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    .question-text {
        font-size: 1.4rem;
        font-weight: 600;
        color: #2c3e50;
        line-height: 1.7;
        margin-bottom: 2rem;
    }
    
    /* 선택 옵션 스타일 */
    .stSelectbox > div > div {
        border: 2px solid #e8ecf0;
        border-radius: 15px;
        font-size: 1.1rem;
        background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
        padding: 0.8rem;
        transition: all 0.3s ease;
        font-family: 'Noto Sans KR', sans-serif;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #667eea;
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: #667eea;
        box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.15);
        transform: translateY(-2px);
    }
    
    /* 결과 카드 스타일 */
    .result-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 3rem;
        border-radius: 25px;
        margin: 3rem 0;
        text-align: center;
        box-shadow: 0 15px 35px rgba(240, 147, 251, 0.4);
        position: relative;
        overflow: hidden;
    }
    
    .result-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: rotate 20s linear infinite;
    }
    
    .mbti-result {
        font-size: 4rem;
        font-weight: 900;
        text-shadow: 0 3px 6px rgba(0,0,0,0.4);
        margin-bottom: 1rem;
        letter-spacing: 4px;
        position: relative;
        z-index: 2;
    }
    
    .mbti-description {
        font-size: 1.4rem;
        opacity: 0.95;
        line-height: 1.7;
        position: relative;
        z-index: 2;
        font-weight: 400;
    }
    
    /* 추천 학과 카드 */
    .recommendation-card {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        border-left: 6px solid #667eea;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
    }
    
    .recommendation-card::after {
        content: '';
        position: absolute;
        top: 0;
        right: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.05), transparent);
        transition: right 0.5s ease;
    }
    
    .recommendation-card:hover {
        transform: translateX(8px) scale(1.02);
        box-shadow: 0 12px 30px rgba(0,0,0,0.12);
    }
    
    .recommendation-card:hover::after {
        right: 100%;
    }
    
    .recommendation-rank {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-weight: 700;
        font-size: 1rem;
        display: inline-block;
        margin-bottom: 1rem;
        box-shadow: 0 3px 10px rgba(102, 126, 234, 0.3);
    }
    
    .recommendation-major {
        font-size: 1.6rem;
        font-weight: 700;
        color: #2c3e50;
        margin-bottom: 0.8rem;
        line-height: 1.4;
    }
    
    .recommendation-score {
        color: #7f8c8d;
        font-size: 1.1rem;
        font-weight: 500;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .score-bar {
        flex: 1;
        height: 8px;
        background: #e8ecf0;
        border-radius: 4px;
        overflow: hidden;
    }
    
    .score-fill {
        height: 100%;
        background: linear-gradient(90deg, #667eea, #764ba2);
        border-radius: 4px;
        transition: width 1s ease-in-out;
    }
    
    /* 프로그레스 바 */
    .progress-container {
        background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 2rem 0;
        text-align: center;
        border: 2px solid #e8ecf0;
    }
    
    .progress-text {
        color: #667eea;
        font-weight: 700;
        font-size: 1.2rem;
        margin-bottom: 1rem;
    }
    
    .progress-bar-container {
        width: 100%;
        height: 12px;
        background: #e8ecf0;
        border-radius: 6px;
        overflow: hidden;
        margin-top: 1rem;
    }
    
    .progress-bar {
        height: 100%;
        background: linear-gradient(90deg, #667eea, #764ba2);
        border-radius: 6px;
        transition: width 0.5s ease-in-out;
    }
    
    /* 버튼 스타일 */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 15px;
        padding: 1rem 3rem;
        font-size: 1.2rem;
        font-weight: 700;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        font-family: 'Noto Sans KR', sans-serif;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5);
    }
    
    /* 추가 정보 스타일 */
    .info-box {
        background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
        border: 2px solid rgba(23, 162, 184, 0.2);
        position: relative;
        overflow: hidden;
    }
    
    .info-box::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, #17a2b8, #6f42c1);
    }
    
    .info-box h4 {
        color: #17a2b8;
        margin-bottom: 1rem;
        font-weight: 700;
        font-size: 1.3rem;
    }
    
    .info-box ul {
        list-style: none;
        padding: 0;
    }
    
    .info-box li {
        padding: 0.5rem 0;
        position: relative;
        padding-left: 2rem;
    }
    
    .info-box li::before {
        content: '✨';
        position: absolute;
        left: 0;
        top: 0.5rem;
    }
    
    /* 애니메이션 */
    .fade-in {
        animation: fadeIn 1s ease-in-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 0.1; }
        50% { transform: scale(1.1); opacity: 0.2; }
    }
    
    @keyframes rotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* 반응형 디자인 */
    @media (max-width: 768px) {
        .main-header h1 { font-size: 2.2rem; }
        .mbti-result { font-size: 3rem; letter-spacing: 2px; }
        .question-text { font-size: 1.2rem; }
        .question-card { padding: 1.5rem; margin: 1rem 0; }
        .recommendation-card { margin: 1rem 0; }
    }
    
    /* 다크 모드 대응 */
    @media (prefers-color-scheme: dark) {
        .question-card, .recommendation-card, .info-box {
            background: #1e1e1e;
            color: #ffffff;
            border-color: rgba(102, 126, 234, 0.3);
        }
        
        .question-text, .recommendation-major {
            color: #ffffff;
        }
    }
</style>
""", unsafe_allow_html=True)

# 메인 헤더
st.markdown("""
<div class="main-header fade-in">
    <h1>🎓 건양대학교 MBTI 전공 추천</h1>
    <p>AI가 분석하는 나만의 완벽한 전공 찾기</p>
</div>
""", unsafe_allow_html=True)

# 소개 섹션
st.markdown("""
<div class="info-box fade-in">
    <h4>🔍 정확한 MBTI 검사를 위한 안내</h4>
    <ul>
        <li>각 질문에 대해 <strong>첫 번째 직감</strong>으로 답변해주세요</li>
        <li>이상적인 모습이 아닌 <strong>현재 실제 모습</strong>을 기준으로 선택해주세요</li>
        <li>32개 질문을 모두 답변하시면 AI가 맞춤형 전공을 추천해드립니다</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# 32개 질문 목록
questions = [
    "새로운 사람들과 만나는 것이 즐겁다",
    "혼자 있는 시간이 더 편안하다", 
    "파티나 모임에 가는 것을 좋아한다",
    "조용한 곳에서 책을 읽는 것이 좋다",
    "많은 사람들과 함께 일하는 것을 선호한다",
    "소수의 깊은 친구를 선호한다",
    "말하기 전에 먼저 생각한다",
    "즉흥적으로 대화하는 것이 자연스럽다",
    "구체적인 사실과 정보에 집중한다",
    "가능성과 잠재력에 더 관심이 있다",
    "실용적이고 현실적인 해결책을 찾는다",
    "창의적이고 혁신적인 아이디어를 선호한다",
    "경험과 전례를 중시한다",
    "새로운 방법을 시도해보고 싶어한다",
    "세부 사항에 주의를 기울인다",
    "전체적인 그림을 보는 것이 중요하다",
    "논리적이고 객관적으로 판단한다",
    "감정과 가치를 고려하여 결정한다",
    "비판적 분석이 중요하다고 생각한다",
    "다른 사람의 감정에 민감하다",
    "공정함과 정의를 중시한다",
    "조화와 협력을 중요하게 여긴다",
    "원칙과 일관성을 중요시한다",
    "상황에 따라 유연하게 대응한다",
    "계획을 세우고 그대로 실행한다",
    "상황에 맞춰 즉흥적으로 행동한다",
    "일정과 데드라인을 잘 지킨다",
    "여러 옵션을 열어두는 것을 선호한다",
    "결정을 빨리 내리는 편이다",
    "마지막 순간까지 선택을 미루기도 한다",
    "체계적이고 조직적인 것을 선호한다",
    "자유롭고 유연한 환경을 좋아한다"
]

# 세션 상태 초기화
if "answers" not in st.session_state:
    st.session_state.answers = ["선택하세요"] * len(questions)

# 프로그레스 표시
answered_count = sum(1 for answer in st.session_state.answers if answer != "선택하세요")
progress_percentage = (answered_count / len(questions)) * 100

st.markdown(f"""
<div class="progress-container fade-in">
    <div class="progress-text">
        📊 진행률: {answered_count}/{len(questions)} ({progress_percentage:.1f}%)
    </div>
    <div class="progress-bar-container">
        <div class="progress-bar" style="width: {progress_percentage}%"></div>
    </div>
</div>
""", unsafe_allow_html=True)

# 질문 표시
for i, question in enumerate(questions):
    st.markdown(f"""
    <div class="question-card fade-in">
        <div class="question-number">{i+1}</div>
        <div class="question-text">{question}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.session_state.answers[i] = st.selectbox(
        f"질문 {i+1}",
        ["선택하세요", "매우 그렇다", "그렇다", "보통이다", "그렇지 않다", "매우 그렇지 않다"],
        index=0 if st.session_state.answers[i] == "선택하세요" else 
              ["선택하세요", "매우 그렇다", "그렇다", "보통이다", "그렇지 않다", "매우 그렇지 않다"].index(st.session_state.answers[i]),
        key=f"q_{i}",
        label_visibility="collapsed"
    )

# 모든 질문에 답변했는지 확인
all_answered = all(answer != "선택하세요" for answer in st.session_state.answers)

if all_answered:
    st.markdown("---")
    
    # 결과 계산 버튼
    if st.button("🎯 MBTI 결과 확인하기", type="primary"):
        
        # MBTI 계산 로직
        def calculate_mbti(answers: List[str]) -> Tuple[str, Dict[str, int]]:
            scores = {'E': 0, 'I': 0, 'S': 0, 'N': 0, 'T': 0, 'F': 0, 'J': 0, 'P': 0}
            
            # 질문별 가중치 (매우 그렇다: 2, 그렇다: 1, 보통: 0, 그렇지 않다: -1, 매우 그렇지 않다: -2)
            weights = {
                "매우 그렇다": 2,
                "그렇다": 1,
                "보통이다": 0,
                "그렇지 않다": -1,
                "매우 그렇지 않다": -2
            }
            
            # E/I 문항 (0,2,4,6은 E형, 1,3,5,7은 I형)
            ei_questions = [0, 1, 2, 3, 4, 5, 6, 7]
            ei_types = ['E', 'I', 'E', 'I', 'E', 'I', 'I', 'E']
            
            # S/N 문항 (8,10,12,14는 S형, 9,11,13,15는 N형)
            sn_questions = [8, 9, 10, 11, 12, 13, 14, 15]
            sn_types = ['S', 'N', 'S', 'N', 'S', 'N', 'S', 'N']
            
            # T/F 문항 (16,18,20,22는 T형, 17,19,21,23은 F형)
            tf_questions = [16, 17, 18, 19, 20, 21, 22, 23]
            tf_types = ['T', 'F', 'T', 'F', 'T', 'F', 'T', 'F']
            
            # J/P 문항 (24,26,28,30은 J형, 25,27,29,31은 P형)
            jp_questions = [24, 25, 26, 27, 28, 29, 30, 31]
            jp_types = ['J', 'P', 'J', 'P', 'J', 'P', 'J', 'P']
            
            # 점수 계산
            for i, q_type in zip(ei_questions, ei_types):
                scores[q_type] += weights[answers[i]]
            
            for i, q_type in zip(sn_questions, sn_types):
                scores[q_type] += weights[answers[i]]
                
            for i, q_type in zip(tf_questions, tf_types):
                scores[q_type] += weights[answers[i]]
                
            for i, q_type in zip(jp_questions, jp_types):
                scores[q_type] += weights[answers[i]]
            
            # MBTI 유형 결정
            mbti = ""
            mbti += "E" if scores['E'] > scores['I'] else "I"
            mbti += "S" if scores['S'] > scores['N'] else "N"
            mbti += "T" if scores['T'] > scores['F'] else "F"
            mbti += "J" if scores['J'] > scores['P'] else "P"
            
            return mbti, scores
        
        mbti_result, scores = calculate_mbti(st.session_state.answers)
        
        # MBTI 유형별 설명
        mbti_descriptions = {
            "INTJ": "건축가 - 상상력이 풍부하고 전략적인 사고를 하는 완벽주의자",
            "INTP": "논리술사 - 지식에 대한 갈증이 강하고 혁신적인 발명가",
            "ENTJ": "통솔자 - 대담하고 상상력이 풍부하며 의지가 강한 지도자",
            "ENTP": "토론자 - 똑똑하고 호기심이 많은 사상가",
            "INFJ": "옹호자 - 선의를 지닌 이상주의자이자 원칙주의자",
            "INFP": "중재자 - 친절하고 이타적이며 언제나 좋은 대의를 찾는 사람",
            "ENFJ": "선도자 - 카리스마 있고 영감을 주는 지도자",
            "ENFP": "활동가 - 열정적이고 창의적인 자유로운 영혼",
            "ISTJ": "현실주의자 - 실용적이고 신중하며 신뢰할 수 있는 사람",
            "ISFJ": "수호자 - 따뜻한 마음과 헌신적인 성격의 보호자",
            "ESTJ": "경영자 - 뛰어난 관리 능력을 지닌 전통과 질서의 대표자",
            "ESFJ": "영사 - 배려심이 많고 사교적이며 인기가 많은 사람",
            "ISTP": "장인 - 대담하면서도 현실적인 사고를 하는 만능 재주꾼",
            "ISFP": "모험가 - 유연하고 매력적인 예술가 기질의 탐험가",
            "ESTP": "사업가 - 영리하고 에너지 넘치며 지각이 뛰어난 사람",
            "ESFP": "연예인 - 즉흥적이고 열정적이며 사교적인 자유로운 영혼"
        }
        
        # 결과 표시
        st.markdown(f"""
        <div class="result-card fade-in">
            <div class="mbti-result">{mbti_result}</div>
            <div class="mbti-description">{mbti_descriptions.get(mbti_result, "당신만의 독특한 성격 유형입니다!")}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # 건양대학교 학과 추천 시스템
        def recommend_majors(mbti_type: str) -> List[Tuple[str, float]]:
            major_recommendations = {
                "INTJ": [
                    ("컴퓨터공학과", 0.95),
                    ("전자공학과", 0.90),
                    ("건축학과", 0.88),
                    ("경영학과", 0.82),
                    ("수학과", 0.80)
                ],
                "INTP": [
                    ("수학과", 0.95),
                    ("물리학과", 0.92),
                    ("컴퓨터공학과", 0.90),
                    ("철학과", 0.85),
                    ("전자공학과", 0.82)
                ],
                "ENTJ": [
                    ("경영학과", 0.95),
                    ("법학과", 0.90),
                    ("정치외교학과", 0.88),
                    ("경제학과", 0.85),
                    ("건축학과", 0.80)
                ],
                "ENTP": [
                    ("마케팅학과", 0.95),
                    ("광고홍보학과", 0.92),
                    ("경영학과", 0.88),
                    ("심리학과", 0.85),
                    ("정치외교학과", 0.82)
                ],
                "INFJ": [
                    ("심리학과", 0.95),
                    ("사회복지학과", 0.90),
                    ("상담학과", 0.88),
                    ("교육학과", 0.85),
                    ("간호학과", 0.82)
                ],
                "INFP": [
                    ("문예창작학과", 0.95),
                    ("예술학과", 0.92),
                    ("심리학과", 0.88),
                    ("사회복지학과", 0.85),
                    ("상담학과", 0.82)
                ],
                "ENFJ": [
                    ("교육학과", 0.95),
                    ("상담학과", 0.90),
                    ("사회복지학과", 0.88),
                    ("심리학과", 0.85),
                    ("간호학과", 0.82)
                ],
                "ENFP": [
                    ("광고홍보학과", 0.95),
                    ("마케팅학과", 0.92),
                    ("예술학과", 0.88),
                    ("심리학과", 0.85),
                    ("교육학과", 0.82)
                ],
                "ISTJ": [
                    ("회계학과", 0.95),
                    ("법학과", 0.90),
                    ("행정학과", 0.88),
                    ("경영학과", 0.85),
                    ("토목공학과", 0.82)
                ],
                "ISFJ": [
                    ("간호학과", 0.95),
                    ("사회복지학과", 0.90),
                    ("교육학과", 0.88),
                    ("유아교육과", 0.85),
                    ("상담학과", 0.82)
                ],
                "ESTJ": [
                    ("경영학과", 0.95),
                    ("행정학과", 0.90),
                    ("법학과", 0.88),
                    ("회계학과", 0.85),
                    ("정치외교학과", 0.82)
                ],
                "ESFJ": [
                    ("교육학과", 0.95),
                    ("간호학과", 0.90),
                    ("사회복지학과", 0.88),
                    ("유아교육과", 0.85),
                    ("상담학과", 0.82)
                ],
                "ISTP": [
                    ("기계공학과", 0.95),
                    ("전자공학과", 0.90),
                    ("컴퓨터공학과", 0.88),
                    ("토목공학과", 0.85),
                    ("건축학과", 0.82)
                ],
                "ISFP": [
                    ("예술학과", 0.95),
                    ("문예창작학과", 0.90),
                    ("디자인학과", 0.88),
                    ("음악학과", 0.85),
                    ("심리학과", 0.80)
                ],
                "ESTP": [
                    ("체육학과", 0.95),
                    ("마케팅학과", 0.90),
                    ("경영학과", 0.88),
                    ("광고홍보학과", 0.85),
                    ("관광학과", 0.82)
                ],
                "ESFP": [
                    ("연극영화학과", 0.95),
                    ("체육학과", 0.90),
                    ("예술학과", 0.88),
                    ("광고홍보학과", 0.85),
                    ("관광학과", 0.82)
                ]
            }
            
            default_recommendations: List[Tuple[str, float]] = [
                ("종합적 검토 필요", 0.70),
                ("상담을 통한 결정", 0.65),
                ("다양한 분야 탐색", 0.60),
                ("적성검사 병행", 0.55),
                ("진로상담 권장", 0.50)
            ]
            return major_recommendations.get(mbti_type, default_recommendations)
        
        recommendations = recommend_majors(mbti_result)
        
        st.markdown("### 🎯 AI 기반 맞춤 전공 추천")
        
        for i, (major, score) in enumerate(recommendations, 1):
            score_percentage = score * 100
            st.markdown(f"""
            <div class="recommendation-card fade-in">
                <div class="recommendation-rank">{i}위 추천</div>
                <div class="recommendation-major">{major}</div>
                <div class="recommendation-score">
                    매칭도: {score_percentage:.1f}%
                    <div class="score-bar">
                        <div class="score-fill" style="width: {score_percentage}%"></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # 추가 안내
        st.markdown("""
        <div class="info-box fade-in">
            <h4>💡 추천 결과 활용 가이드</h4>
            <ul>
                <li>이 결과는 AI 분석을 기반으로 한 <strong>참고자료</strong>입니다</li>
                <li><strong>진로상담</strong>과 함께 종합적으로 검토하시길 권장합니다</li>
                <li>관심 분야와 적성을 함께 고려하여 <strong>최종 결정</strong>하세요</li>
                <li>추가 정보가 필요하시면 건양대학교 <strong>진로상담센터</strong>를 방문하세요</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
else:
    st.markdown(f"""
    <div class="info-box">
        <h4>📝 아직 {len(questions) - answered_count}개의 질문이 남았습니다</h4>
        <p>모든 질문에 답변하시면 정확한 MBTI 분석과 전공 추천을 받으실 수 있습니다.</p>
    </div>
    """, unsafe_allow_html=True)

# 푸터
st.markdown("""
---
<div style="text-align: center; color: #7f8c8d; font-size: 0.9rem; margin-top: 3rem;">
    <p>🎓 건양대학교 MBTI 전공 추천 시스템 | Made with ❤️ by AI</p>
    <p>본 서비스는 참고용이며, 최종 진로 결정은 전문 상담을 통해 하시길 권장합니다.</p>
</div>
""", unsafe_allow_html=True)