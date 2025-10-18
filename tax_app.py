import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import StringIO, BytesIO
import anthropic

# 페이지 설정
st.set_page_config(
    page_title="세금 데이터 분석 시스템",
    page_icon="💰",
    layout="wide"
)

# 제목
st.title("💰 세금 데이터 분석 시스템")
st.markdown("---")

# 세션 스테이트 초기화
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame({
        'name': ['Kim', 'Lee', 'Park', 'Choi', 'Jung', 'Song'],
        'income': [5000, 4000, 3000, 6000, 4500, 5200],
        'tax': [500, 400, 300, 600, 450, 520]
    })

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

df = st.session_state.df

# 사이드바
st.sidebar.title("📋 메뉴")
menu = st.sidebar.radio(
    "기능 선택:",
    ["1️⃣ 데이터 보기", "2️⃣ 세율 계산", "3️⃣ 조건부 서식", 
     "4️⃣ 통계 분석", "5️⃣ 새 데이터 추가", "6️⃣ 차트 생성",
     "7️⃣ 데이터 업로드/다운로드", "🤖 AI 챗봇"]
)

st.sidebar.markdown("---")
st.sidebar.info("💡 VBA 예제를 Streamlit + AI로 구현!")

# AI 챗봇 함수
def get_data_summary():
    summary = f"""
현재 데이터 요약:
- 총 인원: {len(df)}명
- 총 소득: {df['income'].sum():,}원
- 총 세금: {df['tax'].sum():,}원
- 평균 소득: {df['income'].mean():,.0f}원
- 평균 세금: {df['tax'].mean():,.0f}원
- 최고 소득: {df['income'].max():,}원 ({df.loc[df['income'].idxmax(), 'name']})
- 최저 소득: {df['income'].min():,}원 ({df.loc[df['income'].idxmin(), 'name']})
- 평균 세율: {(df['tax'].sum() / df['income'].sum() * 100):.2f}%

상세 데이터:
{df.to_string()}
"""
    return summary

def chat_with_ai(user_message, api_key):
    try:
        client = anthropic.Anthropic(api_key=api_key)
        data_context = get_data_summary()
        
        system_prompt = f"""당신은 세금 데이터 분석 전문가입니다. 
사용자의 질문에 대해 아래 데이터를 기반으로 정확하고 친절하게 답변해주세요.

{data_context}

답변 시 주의사항:
1. 데이터에 기반한 정확한 정보만 제공하세요
2. 필요시 구체적인 숫자와 함께 설명하세요
3. 한국어로 친절하게 답변하세요
4. 데이터 분석 인사이트를 제공하세요"""

        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            messages=[{"role": "user", "content": user_message}],
            system=system_prompt
        )
        
        return message.content[0].text
    except Exception as e:
        return f"❌ 오류 발생: {str(e)}\n\nAPI 키를 확인해주세요."

# 기능 1: 데이터 보기
if menu == "1️⃣ 데이터 보기":
    st.header("📊 현재 데이터")
    st.dataframe(df, use_container_width=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("총 인원", f"{len(df)}명")
    with col2:
        st.metric("총 소득", f"{df['income'].sum():,}원")
    with col3:
        st.metric("총 세금", f"{df['tax'].sum():,}원")

# 기능 2: 세율 계산
elif menu == "2️⃣ 세율 계산":
    st.header("📈 세율 계산")
    df_with_rate = df.copy()
    df_with_rate['tax_rate'] = (df_with_rate['tax'] / df_with_rate['income'] * 100).round(2)
    st.dataframe(df_with_rate, use_container_width=True)
    
    if st.button("💾 세율을 데이터에 추가"):
        st.session_state.df = df_with_rate
        st.success("✅ 세율이 추가되었습니다!")
        st.rerun()

# 기능 3: 조건부 서식
elif menu == "3️⃣ 조건부 서식":
    st.header("🎨 조건부 서식")
    st.write("**소득 구간별 색상:**")
    st.write("🔴 고소득자 (≥5000): 빨강")
    st.write("🟡 중소득자 (4000~4999): 노랑")
    st.write("🟢 저소득자 (<4000): 초록")
    
    def highlight_income(row):
        if row['income'] >= 5000:
            return ['background-color: #ffcccc'] * len(row)
        elif row['income'] >= 4000:
            return ['background-color: #ffffcc'] * len(row)
        else:
            return ['background-color: #ccffcc'] * len(row)
    
    styled_df = df.style.apply(highlight_income, axis=1)
    st.dataframe(styled_df, use_container_width=True)

# 기능 4: 통계 분석
elif menu == "4️⃣ 통계 분석":
    st.header("📊 통계 요약")
    
    total_income = df['income'].sum()
    total_tax = df['tax'].sum()
    avg_income = df['income'].mean()
    avg_tax = df['tax'].mean()
    max_income = df['income'].max()
    min_income = df['income'].min()
    avg_tax_rate = (total_tax / total_income * 100)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 기본 통계")
        stats_df = pd.DataFrame({
            '항목': ['총 인원', '총 소득', '총 세금', '평균 소득', 
                    '평균 세금', '최고 소득', '최저 소득', '평균 세율'],
            '값': [
                f"{len(df)}명",
                f"{total_income:,.0f}원",
                f"{total_tax:,.0f}원",
                f"{avg_income:,.0f}원",
                f"{avg_tax:,.0f}원",
                f"{max_income:,.0f}원",
                f"{min_income:,.0f}원",
                f"{avg_tax_rate:.2f}%"
            ]
        })
        st.dataframe(stats_df, use_container_width=True, hide_index=True)
    
    with col2:
        st.subheader("📊 소득 분포")
        fig = px.histogram(df, x='income', nbins=10, 
                          title='소득 분포',
                          labels={'income': '소득', 'count': '인원'})
        st.plotly_chart(fig, use_container_width=True)

# 기능 5: 새 데이터 추가
elif menu == "5️⃣ 새 데이터 추가":
    st.header("➕ 새 데이터 추가")
    
    with st.form("add_data_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            new_name = st.text_input("이름", placeholder="홍길동")
        with col2:
            new_income = st.number_input("소득", min_value=0, value=5000, step=100)
        with col3:
            new_tax = st.number_input("세금", min_value=0, value=500, step=10)
        
        submitted = st.form_submit_button("추가하기", type="primary")
        
        if submitted:
            if new_name:
                new_row = pd.DataFrame({
                    'name': [new_name],
                    'income': [new_income],
                    'tax': [new_tax]
                })
                st.session_state.df = pd.concat([st.session_state.df, new_row], 
                                                ignore_index=True)
                st.success(f"✅ {new_name}님의 데이터가 추가되었습니다!")
                st.rerun()
            else:
                st.error("❌ 이름을 입력해주세요!")
    
    st.subheader("현재 데이터")
    st.dataframe(df, use_container_width=True)

# 기능 6: 차트 생성
elif menu == "6️⃣ 차트 생성":
    st.header("📊 데이터 시각화")
    
    chart_type = st.selectbox(
        "차트 유형 선택:",
        ["막대 차트", "라인 차트", "파이 차트", "산점도"]
    )
    
    if chart_type == "막대 차트":
        fig = go.Figure()
        fig.add_trace(go.Bar(x=df['name'], y=df['income'], 
                            name='소득', marker_color='lightblue'))
        fig.add_trace(go.Bar(x=df['name'], y=df['tax'], 
                            name='세금', marker_color='lightcoral'))
        fig.update_layout(title='소득 및 세금 비교', 
                         xaxis_title='이름', yaxis_title='금액 (원)',
                         barmode='group')
        st.plotly_chart(fig, use_container_width=True)
    
    elif chart_type == "라인 차트":
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['name'], y=df['income'], 
                                mode='lines+markers', name='소득'))
        fig.add_trace(go.Scatter(x=df['name'], y=df['tax'], 
                                mode='lines+markers', name='세금'))
        fig.update_layout(title='소득 및 세금 추이',
                         xaxis_title='이름', yaxis_title='금액 (원)')
        st.plotly_chart(fig, use_container_width=True)
    
    elif chart_type == "파이 차트":
        fig = px.pie(df, values='income', names='name', 
                    title='소득 비율')
        st.plotly_chart(fig, use_container_width=True)
    
    elif chart_type == "산점도":
        fig = px.scatter(df, x='income', y='tax', text='name',
                        title='소득-세금 상관관계',
                        labels={'income': '소득', 'tax': '세금'})
        fig.update_traces(textposition='top center')
        st.plotly_chart(fig, use_container_width=True)

# 기능 7: 데이터 업로드/다운로드
elif menu == "7️⃣ 데이터 업로드/다운로드":
    st.header("📁 데이터 가져오기/내보내기")
    
    st.subheader("📤 CSV 파일 업로드")
    uploaded_file = st.file_uploader("CSV 파일을 선택하세요", type=['csv'])
    
    if uploaded_file is not None:
        try:
            new_df = pd.read_csv(uploaded_file)
            st.success("✅ 파일이 업로드되었습니다!")
            st.dataframe(new_df, use_container_width=True)
            
            if st.button("이 데이터로 교체하기"):
                st.session_state.df = new_df
                st.success("✅ 데이터가 교체되었습니다!")
                st.rerun()
        except Exception as e:
            st.error(f"❌ 파일 읽기 오류: {e}")
    
    st.markdown("---")
    
    st.subheader("📥 현재 데이터 다운로드")
    
    col1, col2 = st.columns(2)
    
    with col1:
        csv = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📄 CSV 다운로드",
            data=csv,
            file_name='tax_data.csv',
            mime='text/csv',
        )
    
    with col2:
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='데이터', index=False)
        excel_data = output.getvalue()
        
        st.download_button(
            label="📊 Excel 다운로드",
            data=excel_data,
            file_name='tax_data.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )
    
    st.dataframe(df, use_container_width=True)

# 기능 8: AI 챗봇
elif menu == "🤖 AI 챗봇":
    st.header("🤖 AI 데이터 분석 챗봇")
    
    st.info("💡 데이터에 대해 자유롭게 질문하세요! AI가 분석해서 답변해드립니다.")
    
    api_key = st.text_input(
        "Claude API 키를 입력하세요:",
        type="password",
        help="https://console.anthropic.com에서 발급받을 수 있습니다."
    )
    
    if not api_key:
        st.warning("⚠️ API 키를 입력해야 챗봇을 사용할 수 있습니다.")
        st.markdown("""
        ### 📌 API 키 발급 방법:
        1. [Anthropic Console](https://console.anthropic.com) 접속
        2. 로그인 또는 회원가입
        3. API Keys 메뉴에서 새 키 생성
        4. 생성된 키를 복사하여 위 입력창에 붙여넣기
        
        ### 💰 요금:
        - Claude Sonnet: $3 / 1M 토큰 (매우 저렴!)
        - 일반적인 질문 1개 = 약 0.001~0.01원
        """)
    else:
        # 채팅 히스토리 표시
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
        
        # 사용자 입력
        user_input = st.chat_input("데이터에 대해 질문해보세요...")
        
        if user_input:
            st.session_state.chat_history.append({
                "role": "user",
                "content": user_input
            })
            
            with st.spinner("🤔 AI가 생각 중..."):
                ai_response = chat_with_ai(user_input, api_key)
            
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": ai_response
            })
            
            st.rerun()
        
        # 채팅 초기화 버튼
        if st.button("🗑️ 대화 기록 삭제"):
            st.session_state.chat_history = []
            st.rerun()
        
        # 예제 질문
        st.markdown("---")
        st.subheader("💬 예제 질문:")
        example_questions = [
            "평균 세율이 얼마인가요?",
            "가장 높은 소득자는 누구인가요?",
            "5000원 이상 소득자는 몇 명인가요?",
            "데이터의 전반적인 인사이트를 알려주세요",
            "세금 절감 방안을 추천해주세요"
        ]
        
        cols = st.columns(2)
        for idx, question in enumerate(example_questions):
            with cols[idx % 2]:
                if st.button(question, key=f"example_{idx}"):
                    st.session_state.chat_history.append({
                        "role": "user",
                        "content": question
                    })
                    with st.spinner("🤔 AI가 생각 중..."):
                        ai_response = chat_with_ai(question, api_key)
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": ai_response
                    })
                    st.rerun()

# 푸터
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    💡 VBA 예제를 Streamlit + AI로 구현한 웹 서비스입니다<br>
    데이터는 세션에만 저장되며, 새로고침 시 초기화됩니다
</div>
""", unsafe_allow_html=True)
