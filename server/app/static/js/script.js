// 건양대학교 MBTI 기반 전공 추천 시스템
class MBTITest {
    constructor() {
        this.currentQuestion = 0;
        this.answers = [];
        this.questions = this.initializeQuestions();
        this.initializeElements();
        this.bindEvents();
    }

    initializeQuestions() {
        return [
            // I/E 문항 (8개)
            { question: "혼자서 집중하는 시간이 편하다.", type: "IE", options: ["그렇다 (I)", "아니다 (E)"] },
            { question: "깊고 진지한 대화를 선호한다.", type: "IE", options: ["그렇다 (I)", "아니다 (E)"] },
            { question: "조용한 곳에서 공부가 잘 된다.", type: "IE", options: ["그렇다 (I)", "아니다 (E)"] },
            { question: "발표보다 글로 표현하는 것이 익숙하다.", type: "IE", options: ["그렇다 (I)", "아니다 (E)"] },
            { question: "혼자서 문제를 해결하는 편이다.", type: "IE", options: ["그렇다 (I)", "아니다 (E)"] },
            { question: "대답하기 전에 한 번 생각한다.", type: "IE", options: ["그렇다 (I)", "아니다 (E)"] },
            { question: "새로운 사람을 만나는 데 시간이 필요하다.", type: "IE", options: ["그렇다 (I)", "아니다 (E)"] },
            { question: "개인 시간 확보가 중요하다.", type: "IE", options: ["그렇다 (I)", "아니다 (E)"] },
            
            // S/N 문항 (8개)
            { question: "실제 데이터와 사실 기반 정보를 선호한다.", type: "SN", options: ["그렇다 (S)", "아니다 (N)"] },
            { question: "단계별 절차를 따르는 것이 편하다.", type: "SN", options: ["그렇다 (S)", "아니다 (N)"] },
            { question: "손으로 만져보고 배우는 게 빠르다.", type: "SN", options: ["그렇다 (S)", "아니다 (N)"] },
            { question: "현재 실천 가능한 것이 중요하다.", type: "SN", options: ["그렇다 (S)", "아니다 (N)"] },
            { question: "구체적인 예시가 있어야 이해가 된다.", type: "SN", options: ["그렇다 (S)", "아니다 (N)"] },
            { question: "현실적이고 실용적인 선택을 한다.", type: "SN", options: ["그렇다 (S)", "아니다 (N)"] },
            { question: "기존 방식이 안정적이다.", type: "SN", options: ["그렇다 (S)", "아니다 (N)"] },
            { question: "세부 사항을 꼼꼼히 살핀다.", type: "SN", options: ["그렇다 (S)", "아니다 (N)"] },
            
            // T/F 문항 (8개)
            { question: "결정을 할 때 논리·분석이 우선이다.", type: "TF", options: ["그렇다 (T)", "아니다 (F)"] },
            { question: "데이터 중심의 판단을 선호한다.", type: "TF", options: ["그렇다 (T)", "아니다 (F)"] },
            { question: "솔직하고 직선적인 말이 좋다.", type: "TF", options: ["그렇다 (T)", "아니다 (F)"] },
            { question: "효율이 중요하다.", type: "TF", options: ["그렇다 (T)", "아니다 (F)"] },
            { question: "갈등을 논리로 해결한다.", type: "TF", options: ["그렇다 (T)", "아니다 (F)"] },
            { question: "경쟁적 환경이 동기부여된다.", type: "TF", options: ["그렇다 (T)", "아니다 (F)"] },
            { question: "문제를 해결할 때 감정 배제 가능하다.", type: "TF", options: ["그렇다 (T)", "아니다 (F)"] },
            { question: "결과가 중요한 편이다.", type: "TF", options: ["그렇다 (T)", "아니다 (F)"] },
            
            // J/P 문항 (8개)
            { question: "계획을 세우고 움직인다.", type: "JP", options: ["그렇다 (J)", "아니다 (P)"] },
            { question: "마감 전에 미리 끝내는 편이다.", type: "JP", options: ["그렇다 (J)", "아니다 (P)"] },
            { question: "해야 할 일을 목록으로 정리한다.", type: "JP", options: ["그렇다 (J)", "아니다 (P)"] },
            { question: "정리정돈이 잘 되어 있어야 한다.", type: "JP", options: ["그렇다 (J)", "아니다 (P)"] },
            { question: "루틴이 중요하다.", type: "JP", options: ["그렇다 (J)", "아니다 (P)"] },
            { question: "한 번 정하면 지키려 한다.", type: "JP", options: ["그렇다 (J)", "아니다 (P)"] },
            { question: "안정성과 확실함이 중요하다.", type: "JP", options: ["그렇다 (J)", "아니다 (P)"] },
            { question: "계획적인 일정이 편하다.", type: "JP", options: ["그렇다 (J)", "아니다 (P)"] }
        ];
    }

    initializeElements() {
        this.mainPage = document.getElementById('main-page');
        this.testPage = document.getElementById('test-page');
        this.resultPage = document.getElementById('result-page');
        this.startBtn = document.getElementById('start-btn');
        this.questionTitle = document.getElementById('question-title');
        this.optionBtns = document.querySelectorAll('.option-btn');
        this.prevBtn = document.getElementById('prev-btn');
        this.nextBtn = document.getElementById('next-btn');
        this.progressFill = document.querySelector('.progress-fill');
        this.progressText = document.querySelector('.progress-text');
        this.restartBtn = document.getElementById('restart-btn');
        this.shareBtn = document.getElementById('share-btn');
    }

    bindEvents() {
        this.startBtn.addEventListener('click', () => this.startTest());
        this.prevBtn.addEventListener('click', () => this.previousQuestion());
        this.nextBtn.addEventListener('click', () => this.nextQuestion());
        this.restartBtn.addEventListener('click', () => this.restartTest());
        this.shareBtn.addEventListener('click', () => this.shareResult());
        
        this.optionBtns.forEach(btn => {
            btn.addEventListener('click', (e) => this.selectOption(e));
            // 키보드 지원
            btn.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    this.selectOption(e);
                }
                // 화살표 키로 옵션 간 이동
                if (e.key === 'ArrowDown' || e.key === 'ArrowRight') {
                    e.preventDefault();
                    const nextBtn = btn.nextElementSibling;
                    if (nextBtn) nextBtn.focus();
                }
                if (e.key === 'ArrowUp' || e.key === 'ArrowLeft') {
                    e.preventDefault();
                    const prevBtn = btn.previousElementSibling;
                    if (prevBtn) prevBtn.focus();
                }
            });
        });
        
        // 키보드 단축키
        document.addEventListener('keydown', (e) => {
            if (this.testPage.classList.contains('active')) {
                if (e.key === 'ArrowLeft' && !this.prevBtn.disabled) {
                    this.previousQuestion();
                }
                if (e.key === 'ArrowRight' && !this.nextBtn.disabled) {
                    this.nextQuestion();
                }
                if (e.key === '1') {
                    this.optionBtns[0].click();
                }
                if (e.key === '2') {
                    this.optionBtns[1].click();
                }
            }
        });
    }

    startTest() {
        this.currentQuestion = 0;
        this.answers = [];
        this.showPage(this.testPage);
        this.displayQuestion();
        this.updateProgress();
    }

    showPage(page) {
        document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
        page.classList.add('active');
    }

    displayQuestion() {
        const question = this.questions[this.currentQuestion];
        this.questionTitle.textContent = question.question;
        
        this.optionBtns[0].textContent = question.options[0];
        this.optionBtns[0].dataset.type = question.type;
        this.optionBtns[0].dataset.answer = question.options[0].includes('(I)') ? 'I' : 
                                          question.options[0].includes('(S)') ? 'S' :
                                          question.options[0].includes('(T)') ? 'T' :
                                          question.options[0].includes('(J)') ? 'J' : 'A';
        
        this.optionBtns[1].textContent = question.options[1];
        this.optionBtns[1].dataset.type = question.type;
        this.optionBtns[1].dataset.answer = question.options[1].includes('(E)') ? 'E' : 
                                          question.options[1].includes('(N)') ? 'N' :
                                          question.options[1].includes('(F)') ? 'F' :
                                          question.options[1].includes('(P)') ? 'P' : 'B';
        
        // 기존 선택 상태 초기화
        this.optionBtns.forEach(btn => {
            btn.classList.remove('selected');
            btn.setAttribute('aria-checked', 'false');
        });
        
        // 이전 답변이 있다면 표시
        if (this.answers[this.currentQuestion]) {
            const selectedAnswer = this.answers[this.currentQuestion];
            const selectedBtn = Array.from(this.optionBtns).find(btn => btn.dataset.answer === selectedAnswer);
            if (selectedBtn) {
                selectedBtn.classList.add('selected');
                selectedBtn.setAttribute('aria-checked', 'true');
            }
        }
        
        this.updateNavigationButtons();
    }

    selectOption(e) {
        // 이전 선택 해제
        this.optionBtns.forEach(btn => {
            btn.classList.remove('selected');
            btn.setAttribute('aria-checked', 'false');
        });
        
        // 새로운 선택 설정
        e.target.classList.add('selected');
        e.target.setAttribute('aria-checked', 'true');
        
        this.answers[this.currentQuestion] = e.target.dataset.answer;
        this.updateNavigationButtons();
    }

    updateNavigationButtons() {
        this.prevBtn.disabled = this.currentQuestion === 0;
        this.nextBtn.disabled = !this.answers[this.currentQuestion];
    }

    updateProgress() {
        const progress = ((this.currentQuestion + 1) / this.questions.length) * 100;
        this.progressFill.style.width = `${progress}%`;
        this.progressText.textContent = `질문 ${this.currentQuestion + 1} / ${this.questions.length}`;
        
        // 진행률 바 접근성 업데이트
        const progressBar = document.querySelector('.progress-bar');
        progressBar.setAttribute('aria-valuenow', Math.round(progress));
        progressBar.setAttribute('aria-valuetext', `${this.currentQuestion + 1}번째 질문, 전체 ${this.questions.length}문항 중`);
    }

    nextQuestion() {
        if (this.currentQuestion < this.questions.length - 1) {
            this.currentQuestion++;
            this.displayQuestion();
            this.updateProgress();
        } else {
            this.calculateResult();
        }
    }

    previousQuestion() {
        if (this.currentQuestion > 0) {
            this.currentQuestion--;
            this.displayQuestion();
            this.updateProgress();
        }
    }

    calculateResult() {
        const scores = { I: 0, E: 0, S: 0, N: 0, T: 0, F: 0, J: 0, P: 0 };
        
        this.answers.forEach(answer => {
            scores[answer]++;
        });
        
        const mbtiType = [
            scores.I > scores.E ? 'I' : 'E',
            scores.S > scores.N ? 'S' : 'N',
            scores.T > scores.F ? 'T' : 'F',
            scores.J > scores.P ? 'J' : 'P'
        ].join('');
        
        this.showResult(mbtiType);
    }

    showResult(mbtiType) {
        this.showPage(this.resultPage);
        
        const mbtiData = this.getKonYangMBTIData(mbtiType);
        
        document.getElementById('mbti-type').textContent = mbtiType;
        document.getElementById('mbti-description').textContent = mbtiData.description;
        
        this.displayKonYangDepartments(mbtiData.firstChoice, mbtiData.aiRecommendations);
    }

    displayKonYangDepartments(firstChoice, aiRecommendations) {
        const container = document.getElementById('recommended-departments');
        container.innerHTML = '';
        
        // 1차 추천 섹션
        const firstSection = document.createElement('div');
        firstSection.className = 'recommendation-section';
        firstSection.innerHTML = `
            <h3>🎯 1차 MBTI 기반 추천 학과</h3>
            <div class="first-choice-departments">
                ${firstChoice.map(dept => `
                    <div class="department-card primary">
                        <h4>${dept}</h4>
                        <div class="match-rate">우선 추천</div>
                        <p>당신의 MBTI 유형에 가장 적합한 전공입니다.</p>
                        <div class="department-features">
                            <span class="feature-tag">최적 매칭</span>
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
        
        // AI 추천 섹션
        const aiSection = document.createElement('div');
        aiSection.className = 'recommendation-section';
        aiSection.innerHTML = `
            <h3>🤖 AI 기반 최종 추천 TOP 3</h3>
            <div class="ai-recommendations">
                ${aiRecommendations.slice(0, 3).map((dept, index) => `
                    <div class="department-card ai-recommended">
                        <h4>${index + 1}. ${dept.name}</h4>
                        <div class="match-rate">유사도 ${(dept.similarity * 100).toFixed(1)}%</div>
                        <p>AI 분석을 통한 성향 매칭 결과입니다.</p>
                        <div class="department-features">
                            <span class="feature-tag">AI 추천</span>
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
        
        // 추가 고려 학과 섹션
        if (aiRecommendations.length > 3) {
            const additionalSection = document.createElement('div');
            additionalSection.className = 'recommendation-section';
            additionalSection.innerHTML = `
                <h3>📋 추가 고려 학과</h3>
                <div class="additional-departments">
                    ${aiRecommendations.slice(3, 6).map(dept => `
                        <span class="additional-dept">${dept.name}</span>
                    `).join('')}
                </div>
            `;
            container.appendChild(additionalSection);
        }
        
        container.appendChild(firstSection);
        container.appendChild(aiSection);
    }

    restartTest() {
        this.showPage(this.mainPage);
    }

    shareResult() {
        const mbtiType = document.getElementById('mbti-type').textContent;
        const text = `나의 MBTI는 ${mbtiType}! 당신도 MBTI 기반 학과 추천을 받아보세요!`;
        const url = window.location.href;
        
        if (navigator.share) {
            navigator.share({
                title: 'MBTI 학과 추천 결과',
                text: text,
                url: url
            }).catch((error) => {
                console.log('공유 실패:', error);
                this.fallbackShare(text, url);
            });
        } else {
            this.fallbackShare(text, url);
        }
    }
    
    fallbackShare(text, url) {
        const shareText = text + ' ' + url;
        if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(shareText).then(() => {
                this.showNotification('결과가 클립보드에 복사되었습니다! 📋');
            }).catch(() => {
                this.showShareModal(shareText);
            });
        } else {
            this.showShareModal(shareText);
        }
    }
    
    showNotification(message) {
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #10b981;
            color: white;
            padding: 12px 24px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            z-index: 9999;
            font-weight: 500;
            animation: slideInRight 0.3s ease;
        `;
        notification.textContent = message;
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.style.animation = 'slideOutRight 0.3s ease forwards';
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }
    
    showShareModal(text) {
        const modal = document.createElement('div');
        modal.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.7);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 10000;
        `;
        
        const content = document.createElement('div');
        content.style.cssText = `
            background: white;
            padding: 24px;
            border-radius: 12px;
            max-width: 400px;
            width: 90%;
            text-align: center;
        `;
        
        content.innerHTML = `
            <h3 style="margin: 0 0 16px 0;">결과 공유하기</h3>
            <textarea readonly style="
                width: 100%;
                height: 80px;
                border: 1px solid #ddd;
                border-radius: 6px;
                padding: 8px;
                resize: none;
                font-size: 14px;
                margin-bottom: 16px;
            ">${text}</textarea>
            <button onclick="this.parentElement.parentElement.remove()" style="
                background: #6366f1;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                cursor: pointer;
            ">닫기</button>
        `;
        
        modal.appendChild(content);
        document.body.appendChild(modal);
        
        // 텍스트 선택
        const textarea = content.querySelector('textarea');
        textarea.select();
        textarea.setSelectionRange(0, 99999);
        
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.remove();
            }
        });
    }

    getKonYangMBTIData(mbtiType) {
        // 건양대학교 MBTI → 학과 매핑
        const mbtiToMajor = {
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
            "ENFJ": ["국방경찰행정학부", "사회복지학과", "심리상담치료학과", "스포츠의학전공"],
            "ENTJ": ["인공지능학과", "스마트보안학과", "국방산업경영학부", "의료IT공학과"]
        };

        // 학과별 성향 벡터 (I/E, S/N, T/F, J/P)
        const majorVectors = {
            "의료신소재학과": [1,1,1,1], "의료공학과": [1,1,1,1], "의료IT공학과": [1,0,1,1],
            "의료공간디자인학과": [0.5,0,0,0], "ND산업디자인학부": [0.5,0,0,0],
            "제약생명공학과": [1,0,1,1], "식품생명공학과": [1,0,1,1], "임상의약바이오학과": [1,0,0.5,1],
            "인공지능학과": [1,0,1,0.6], "스마트보안학과": [1,0.5,1,1], "기업소프트웨어학부": [1,0,1,0],
            "국방XR학부": [0.5,0,1,0], "스마트팜학부": [0.5,0,1,0], "유무인항공공학과": [0.7,1,1,0],
            "국방반도체공학과": [1,1,1,1], "국방산업경영학부": [0,0.5,1,1], "국방경찰행정학부": [0,1,1,1],
            "재난안전소방학전공": [0,1,1,0], "군사학과": [0,1,1,1], "사회복지학과": [0,0.5,0,1],
            "심리상담치료학과": [0,0,0,1], "유아교육과": [0,0,0,1], "특수교육과": [0,0,0,1],
            "글로벌의료뷰티학전공": [0,0,0,0], "재활퍼스널트레이닝학과": [0,1,0,0.5], "스포츠의학전공": [0,1,0,0]
        };

        // MBTI → 벡터 변환
        const mbtiVector = [
            mbtiType[0] === 'I' ? 1 : 0,
            mbtiType[1] === 'S' ? 1 : 0,
            mbtiType[2] === 'T' ? 1 : 0,
            mbtiType[3] === 'J' ? 1 : 0
        ];

        // 코사인 유사도 계산
        const aiRecommendations = Object.entries(majorVectors).map(([major, vector]) => ({
            name: major,
            similarity: this.cosineSimilarity(mbtiVector, vector)
        })).sort((a, b) => b.similarity - a.similarity);

        const descriptions = {
            "ISTJ": "체계적이고 신뢰할 수 있으며, 전통을 중시하고 책임감이 강한 성격입니다.",
            "ISFJ": "따뜻하고 배려심 많으며, 다른 사람을 돕는 것을 좋아하는 성격입니다.",
            "INFJ": "통찰력 있고 이상주의적이며, 깊이 있는 관계를 추구하는 성격입니다.",
            "INTJ": "독립적이고 전략적 사고를 하며, 혁신을 추구하는 성격입니다.",
            "ISTP": "실용적이고 융통성 있으며, 손으로 만들기를 좋아하는 성격입니다.",
            "ISFP": "온화하고 친근하며, 조화와 개인적 가치를 중시하는 성격입니다.",
            "INFP": "이상주의적이고 충성심 강하며, 개인의 가치와 일치하는 일에 열정적인 성격입니다.",
            "INTP": "논리적이고 창의적이며, 이론과 추상적 아이디어에 관심이 많은 성격입니다.",
            "ESTP": "활동적이고 현실적이며, 즉흥적이고 적응력이 좋은 성격입니다.",
            "ESFP": "외향적이고 친근하며, 사람들과 함께하는 것을 좋아하는 성격입니다.",
            "ENFP": "열정적이고 창의적이며, 새로운 가능성을 탐구하는 것을 좋아하는 성격입니다.",
            "ENTP": "혁신적이고 호기심 많으며, 새로운 아이디어와 도전을 즐기는 성격입니다.",
            "ESTJ": "실용적이고 조직적이며, 효율성과 결과를 중시하는 성격입니다.",
            "ESFJ": "사교적이고 협력적이며, 다른 사람의 필요를 잘 파악하는 성격입니다.",
            "ENFJ": "카리스마 있고 영감을 주며, 다른 사람의 성장을 돕는 것을 좋아하는 성격입니다.",
            "ENTJ": "대담하고 상상력 풍부한 지도자로, 목표 달성을 위해 노력하는 성격입니다."
        };

        return {
            description: descriptions[mbtiType] || "독특하고 개성 있는 성격입니다.",
            firstChoice: mbtiToMajor[mbtiType] || ["전공 탐색을 권장합니다."],
            aiRecommendations: aiRecommendations
        };
    }

    cosineSimilarity(vec1, vec2) {
        const dotProduct = vec1.reduce((sum, a, i) => sum + a * vec2[i], 0);
        const magnitude1 = Math.sqrt(vec1.reduce((sum, a) => sum + a * a, 0));
        const magnitude2 = Math.sqrt(vec2.reduce((sum, a) => sum + a * a, 0));
        
        if (magnitude1 === 0 || magnitude2 === 0) return 0;
        return dotProduct / (magnitude1 * magnitude2);
    }
}

// 페이지 로드 시 테스트 초기화
document.addEventListener('DOMContentLoaded', () => {
    // no-js 클래스 제거 (JavaScript가 활성화됨을 표시)
    document.body.classList.remove('no-js');
    
    // MBTI 테스트 초기화
    try {
        new MBTITest();
    } catch (error) {
        console.error('MBTI 테스트 초기화 실패:', error);
        // 에러 발생 시 기본 메시지 표시
        const errorMsg = document.createElement('div');
        errorMsg.style.cssText = 'position: fixed; top: 20px; left: 20px; background: #ff4444; color: white; padding: 10px; border-radius: 5px; z-index: 9999;';
        errorMsg.textContent = '페이지 로딩 중 오류가 발생했습니다. 새로고침을 시도해주세요.';
        document.body.appendChild(errorMsg);
        setTimeout(() => errorMsg.remove(), 5000);
    }
});