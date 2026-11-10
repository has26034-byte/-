import streamlit as st
import time

# --- [페이지 기본 설정] ---
st.set_page_config(
    page_title="학생용 학습 타이머",
    page_icon="⏱️",
    layout="centered"
)

# --- [세션 상태(Session State) 초기화] ---
# 애플리케이션의 상태를 저장하는 변수들입니다.
if "running" not in st.session_state:
    st.session_state.running = False
if "elapsed_time" not in st.session_state:
    st.session_state.elapsed_time = 0
if "last_start_time" not in st.session_state:
    st.session_state.last_start_time = None
if "subject_records" not in st.session_state:
    st.session_state.subject_records = {"국어": 0, "수학": 0, "영어": 0}

# --- [유틸리티 함수: 초 단위 시간을 HH:MM:SS 형식으로 변환] ---
def format_time(seconds):
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hrs:02d}:{mins:02d}:{secs:02d}"

# --- [UI 레이아웃] ---
st.title("⏱️ 과목별 학습 타이머")
st.caption("오늘의 목표를 향해 달려보세요!")

st.divider()

# 1. 과목 선택 섹션
st.subheader("1. 과목 선택")
col_sub1, col_sub2 = st.columns([2, 1])

with col_sub1:
    selected_subject = st.selectbox(
        "공부할 과목을 선택하세요:",
        options=list(st.session_state.subject_records.keys())
    )

with col_sub2:
    new_subject = st.text_input("새 과목 추가:", placeholder="예: 과학")
    if st.button("과목 추가", use_container_width=True):
        if new_subject and new_subject not in st.session_state.subject_records:
            st.session_state.subject_records[new_subject] = 0
            st.success(f"'{new_subject}' 과목이 추가되었습니다.")
            st.rerun()

st.divider()

# 2. 타이머 디스플레이 및 제어 버튼
st.subheader(f"2. [{selected_subject}] 학습 측정")

# 경과 시간 계산
current_elapsed = st.session_state.elapsed_time
if st.session_state.running:
    current_elapsed += time.time() - st.session_state.last_start_time

# 타이머 시계 표시 (큰 글씨)
st.markdown(
    f"<h1 style='text-align: center; color: #4CAF50; font-size: 60px;'>{format_time(current_elapsed)}</h1>",
    unsafe_allow_html=True
)

st.write("") # 여백

# 버튼 컨트롤 레이아웃 (시작, 일시정지, 초기화, 기록 저장)
btn_col1, btn_col2, btn_col3, btn_col4 = st.columns(4)

with btn_col1:
    if st.button("▶️ 시작", disabled=st.session_state.running, use_container_width=True):
        st.session_state.running = True
        st.session_state.last_start_time = time.time()
        st.rerun()

with btn_col2:
    if st.button("⏸️ 일시정지", disabled=not st.session_state.running, use_container_width=True):
        st.session_state.elapsed_time += time.time() - st.session_state.last_start_time
        st.session_state.running = False
        st.rerun()

with btn_col3:
    if st.button("🔄 초기화", use_container_width=True):
        st.session_state.running = False
        st.session_state.elapsed_time = 0
        st.session_state.last_start_time = None
        st.rerun()

with btn_col4:
    if st.button("💾 기록 저장", use_container_width=True):
        if st.session_state.running:
            st.session_state.elapsed_time += time.time() - st.session_state.last_start_time
            st.session_state.last_start_time = time.time()

        # 선택된 과목에 누적 시간 저장 후 타이머 리셋
        st.session_state.subject_records[selected_subject] += int(st.session_state.elapsed_time)
        st.session_state.elapsed_time = 0
        st.session_state.running = False
        st.success(f"'{selected_subject}'에 시간이 성공적으로 저장되었습니다!")
        st.rerun()

st.divider()

# 3. 과목별 공부 시간 누적 기록표
st.subheader("📊 과목별 누적 학습 시간")

for subject, total_sec in st.session_state.subject_records.items():
    c1, c2 = st.columns([1, 2])
    with c1:
        st.write(f"**{subject}**")
    with c2:
        st.write(format_time(total_sec))

# 타이머가 작동 중일 때 1초마다 화면을 새로고침합니다.
if st.session_state.running:
    time.sleep(1)
    st.rerun()