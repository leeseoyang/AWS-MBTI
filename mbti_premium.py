import streamlit as st
import plotly.graph_objects as go
import json

# 페이지 설정
st.set_page_config(
    page_title="건양대학교 전과 적성 진단",
    page_icon="🎓",
    layout="wide"
)

# CSS 스타일
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
    
    * {
        font-family: 'Noto Sans KR', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
    }
    
    .title {
        text-align: center;
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .card {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        margin: 1rem 0;
    }
    
    .question {
        font-size: 1.3rem;
        font-weight: 700;
        color: #333;
        margin-bottom: 1.5rem;
    }
    
    .scale-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 2rem 0;
    }
    
    .scale-label {
        font-size: 1rem;
        font-weight: 600;
        color: #666;
    }
    
    .stButton>button {
        width: 100%;
        height: 60px;
        font-size: 1.2rem;
        font-weight: 700;
        border-radius: 15px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    .progress-text {
        text-align: center;
        color: white;
        font-size: 1.2rem;
        font-weight: 600;
        margin: 1rem 0;
    }
    
    .result-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        border-radius: 20px;
        padding: 2rem;
        color: white;
        margin: 1rem 0;
    }
    
    .major-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    .major-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #667eea;
        margin-bottom: 0.5rem;
    }
    
    .major-score {
        font-size: 1.2rem;
        font-weight: 600;
        color: #764ba2;
        margin-bottom: 1rem;
    }
    
    .major-desc {
        font-size: 1rem;
        color: #666;
        line-height: 1.6;
    }
    
    .trait-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #333;
        margin: 1.5rem 0 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# 7단계 척도 버튼 (원형)
def circle_scale(question_num, label):
    st.markdown(f'<div class="question">{question_num}. {label}</div>', unsafe_allow_html=True)
    
    cols = st.columns([2, 1, 1, 1, 1, 1, 1, 1, 2])
    cols[0].markdown('<div class="scale-label">매우 동의</div>', unsafe_allow_html=True)
    
    selected = None
    for i in range(1, 8):
        if cols[i].button("●", key=f"q{question_num}_s{i}", help=f"{i}점"):
            selected = i
    
    cols[8].markdown('<div class="scale-label">매우 비동의</div>', unsafe_allow_html=True)
    
    return selected

# 질문 데이터 (40문항)
questions = [
    # 분석형 (1-8)
    {"id": 1, "text": "데이터를 분석하고 패턴을 찾는 것이 즐겁다", "trait": "분석형"},
    {"id": 2, "text": "논리적으로 문제를 해결하는 것을 선호한다", "trait": "분석형"},
    {"id": 3, "text": "복잡한 수학 문제를 푸는 것이 흥미롭다", "trait": "분석형"},
    {"id": 4, "text": "체계적이고 구조화된 접근을 좋아한다", "trait": "분석형"},
    {"id": 5, "text": "프로그래밍이나 코딩에 관심이 있다", "trait": "분석형"},
    {"id": 6, "text": "통계나 확률 개념이 재미있다", "trait": "분석형"},
    {"id": 7, "text": "원인과 결과를 분석하는 것을 좋아한다", "trait": "분석형"},
    {"id": 8, "text": "새로운 기술을 배우고 적용하는 것이 즐겁다", "trait": "분석형"},
    
    # 창의형 (9-16)
    {"id": 9, "text": "새로운 아이디어를 만들어내는 것이 좋다", "trait": "창의형"},
    {"id": 10, "text": "예술적 표현에 관심이 많다", "trait": "창의형"},
    {"id": 11, "text": "독창적인 해결책을 찾는 것을 선호한다", "trait": "창의형"},
    {"id": 12, "text": "디자인이나 색감에 민감하다", "trait": "창의형"},
    {"id": 13, "text": "상상력을 발휘하는 활동이 즐겁다", "trait": "창의형"},
    {"id": 14, "text": "기존의 틀을 벗어나 생각하는 것을 좋아한다", "trait": "창의형"},
    {"id": 15, "text": "창작 활동(글쓰기, 그림 등)에 흥미가 있다", "trait": "창의형"},
    {"id": 16, "text": "미적 감각이 필요한 작업이 재미있다", "trait": "창의형"},
    
    # 실무형 (17-24)
    {"id": 17, "text": "실제로 만들거나 조립하는 작업이 좋다", "trait": "실무형"},
    {"id": 18, "text": "손으로 직접 작업하는 것을 선호한다", "trait": "실무형"},
    {"id": 19, "text": "기계나 장비를 다루는 것이 흥미롭다", "trait": "실무형"},
    {"id": 20, "text": "실험이나 실습 활동이 즐겁다", "trait": "실무형"},
    {"id": 21, "text": "구체적인 결과물을 만드는 것을 좋아한다", "trait": "실무형"},
    {"id": 22, "text": "도구나 기술을 활용하는 것이 자신있다", "trait": "실무형"},
    {"id": 23, "text": "물리적인 작업에 흥미가 있다", "trait": "실무형"},
    {"id": 24, "text": "실용적인 기술을 배우는 것이 좋다", "trait": "실무형"},
    
    # 소통형 (25-30)
    {"id": 25, "text": "사람들과 대화하고 교류하는 것이 즐겁다", "trait": "소통형"},
    {"id": 26, "text": "팀으로 일하는 것을 선호한다", "trait": "소통형"},
    {"id": 27, "text": "발표나 프레젠테이션이 자신있다", "trait": "소통형"},
    {"id": 28, "text": "다른 사람을 설득하는 것이 재미있다", "trait": "소통형"},
    {"id": 29, "text": "사회적 이슈에 관심이 많다", "trait": "소통형"},
    {"id": 30, "text": "리더십을 발휘하는 것을 좋아한다", "trait": "소통형"},
    
    # 공감형 (31-36)
    {"id": 31, "text": "다른 사람의 감정을 잘 이해한다", "trait": "공감형"},
    {"id": 32, "text": "돕고 봉사하는 활동이 보람있다", "trait": "공감형"},
    {"id": 33, "text": "사람들의 문제를 들어주는 것이 좋다", "trait": "공감형"},
    {"id": 34, "text": "타인의 입장에서 생각하는 것이 자연스럽다", "trait": "공감형"},
    {"id": 35, "text": "돌봄이나 케어 활동에 관심이 있다", "trait": "공감형"},
    {"id": 36, "text": "감정적 교류가 중요하다고 생각한다", "trait": "공감형"},
    
    # 학습·집중형 (37-40)
    {"id": 37, "text": "깊이 있게 연구하고 공부하는 것이 좋다", "trait": "학습·집중형"},
    {"id": 38, "text": "이론적인 내용을 학습하는 것이 즐겁다", "trait": "학습·집중형"},
    {"id": 39, "text": "집중해서 오랜 시간 공부할 수 있다", "trait": "학습·집중형"},
    {"id": 40, "text": "지식을 쌓는 것 자체가 즐거다", "trait": "학습·집중형"},
]

# 학과 데이터
majors = {
    "컴퓨터공학과": {
        "traits": {"분석형": 5, "창의형": 3, "실무형": 4, "소통형": 2, "공감형": 1, "학습·집중형": 4},
        "desc": "소프트웨어 개발, 인공지능, 데이터 분석 등 IT 전문가 양성",
        "url": "https://www.konyang.ac.kr"
    },
    "의료IT공학과": {
        "traits": {"분석형": 4, "창의형": 3, "실무형": 5, "소통형": 2, "공감형": 3, "학습·집중형": 4},
        "desc": "의료 기기 및 헬스케어 IT 융합 기술 전문가",
        "url": "https://www.konyang.ac.kr"
    },
    "간호학과": {
        "traits": {"분석형": 3, "창의형": 2, "실무형": 4, "소통형": 4, "공감형": 5, "학습·집중형": 4},
        "desc": "환자 케어와 건강 증진을 위한 전문 간호사 양성",
        "url": "https://www.konyang.ac.kr"
    },
    "의과대학": {
        "traits": {"분석형": 5, "창의형": 2, "실무형": 4, "소통형": 3, "공감형": 5, "학습·집중형": 5},
        "desc": "임상 진료와 의학 연구를 수행하는 의료 전문가",
        "url": "https://www.konyang.ac.kr"
    },
    "건축학과": {
        "traits": {"분석형": 3, "창의형": 5, "실무형": 4, "소통형": 3, "공감형": 2, "학습·집중형": 3},
        "desc": "공간 디자인과 건축 설계 전문가 양성",
        "url": "https://www.konyang.ac.kr"
    },
    "산업디자인학과": {
        "traits": {"분석형": 2, "창의형": 5, "실무형": 4, "소통형": 3, "공감형": 3, "학습·집중형": 2},
        "desc": "제품 및 시각 디자인 창의적 전문가 양성",
        "url": "https://www.konyang.ac.kr"
    },
    "경영학과": {
        "traits": {"분석형": 4, "창의형": 3, "실무형": 3, "소통형": 5, "공감형": 3, "학습·집중형": 3},
        "desc": "경영 전략, 마케팅, 재무 분야 비즈니스 리더 양성",
        "url": "https://www.konyang.ac.kr"
    },
    "사회복지학과": {
        "traits": {"분석형": 2, "창의형": 3, "실무형": 3, "소통형": 5, "공감형": 5, "학습·집중형": 3},
        "desc": "지역사회와 개인의 복지 향상을 위한 전문가",
        "url": "https://www.konyang.ac.kr"
    },
    "물리치료학과": {
        "traits": {"분석형": 3, "창의형": 2, "실무형": 5, "소통형": 3, "공감형": 4, "학습·집중형": 4},
        "desc": "재활 및 물리치료 전문 의료인 양성",
        "url": "https://www.konyang.ac.kr"
    },
    "기계공학과": {
        "traits": {"분석형": 5, "창의형": 3, "실무형": 5, "소통형": 2, "공감형": 1, "학습·집중형": 4},
        "desc": "기계 설계, 제조, 자동화 기술 엔지니어 양성",
        "url": "https://www.konyang.ac.kr"
    }
}

# 세션 상태 초기화
if 'responses' not in st.session_state:
    st.session_state.responses = {}
if 'current_q' not in st.session_state:
    st.session_state.current_q = 0
if 'completed' not in st.session_state:
    st.session_state.completed = False

# 제목
st.markdown('<div class="title">🎓 건양대학교 전과 적성 진단 질문지</div>', unsafe_allow_html=True)

# 안내문
if st.session_state.current_q == 0:
    st.markdown("""
    <div class="card">
        <h2 style="color: #667eea; margin-bottom: 1rem;">📋 안내문</h2>
        <div style="font-size: 1.1rem; line-height: 1.8; color: #333;">
            <p><strong>본 질문지는 건양대학교 재학생의 전과 선택을 돕기 위해 제작되었습니다.</strong></p>
            <ol style="margin-left: 1.5rem;">
                <li>각 문항을 읽고 자신에게 해당하는 정도를 7단계 척도로 선택해주세요.</li>
                <li>정답이 없으니 솔직하게 응답해주세요.</li>
                <li>모든 문항에 빠짐없이 응답해주시기 바랍니다.</li>
                <li>검사 결과는 전과 상담 시 참고자료로 활용됩니다.</li>
            </ol>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("시작하기", key="start_btn"):
        st.session_state.current_q = 1
        st.rerun()

# 질문 진행
elif st.session_state.current_q > 0 and st.session_state.current_q <= 40:
    q_idx = st.session_state.current_q - 1
    q = questions[q_idx]
    
    st.markdown(f'<div class="progress-text">질문 {st.session_state.current_q} / 40</div>', unsafe_allow_html=True)
    st.progress(st.session_state.current_q / 40)
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    # 7단계 척도
    response = circle_scale(st.session_state.current_q, q["text"])
    
    if response:
        st.session_state.responses[q["id"]] = response
        st.session_state.current_q += 1
        if st.session_state.current_q > 40:
            st.session_state.completed = True
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 이전 버튼
    if st.session_state.current_q > 1:
        if st.button("← 이전 질문"):
            st.session_state.current_q -= 1
            st.rerun()

# 결과 화면
elif st.session_state.completed:
    st.markdown('<div class="result-card"><h1 style="text-align: center;">🎉 검사 완료!</h1></div>', unsafe_allow_html=True)
    
    # 특성별 점수 계산
    trait_scores = {
        "분석형": 0,
        "창의형": 0,
        "실무형": 0,
        "소통형": 0,
        "공감형": 0,
        "학습·집중형": 0
    }
    
    for q in questions:
        trait_scores[q["trait"]] += st.session_state.responses[q["id"]]
    
    # 정규화 (각 특성별 문항 수로 나눔)
    trait_counts = {
        "분석형": 8,
        "창의형": 8,
        "실무형": 8,
        "소통형": 6,
        "공감형": 6,
        "학습·집중형": 4
    }
    
    for trait in trait_scores:
        trait_scores[trait] = trait_scores[trait] / trait_counts[trait]
    
    # 레이더 차트
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="trait-title">📊 나의 적성 특성</div>', unsafe_allow_html=True)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=list(trait_scores.values()),
        theta=list(trait_scores.keys()),
        fill='toself',
        name='나의 특성',
        line_color='rgb(102, 126, 234)',
        fillcolor='rgba(102, 126, 234, 0.3)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 7]
            )
        ),
        showlegend=False,
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 학과 추천
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="trait-title">🎯 추천 학과 TOP 3</div>', unsafe_allow_html=True)
    
    # 학과별 매칭 점수 계산
    major_scores = {}
    for major_name, major_info in majors.items():
        score = 0
        for trait, weight in major_info["traits"].items():
            score += trait_scores[trait] * weight
        major_scores[major_name] = score
    
    # 상위 3개 학과
    top_3 = sorted(major_scores.items(), key=lambda x: x[1], reverse=True)[:3]
    
    for rank, (major_name, score) in enumerate(top_3, 1):
        medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉"
        st.markdown(f"""
        <div class="major-card">
            <div class="major-title">{medal} {major_name}</div>
            <div class="major-score">적합도: {score:.1f}점</div>
            <div class="major-desc">{majors[major_name]["desc"]}</div>
            <a href="{majors[major_name]["url"]}" target="_blank" style="color: #667eea; text-decoration: none; font-weight: 600;">학과 홈페이지 →</a>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 다시하기 버튼
    if st.button("🔄 다시 검사하기"):
        st.session_state.responses = {}
        st.session_state.current_q = 0
        st.session_state.completed = False
        st.rerun()
