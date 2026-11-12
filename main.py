import streamlit as st
import pandas as pd
import time
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

st.set_page_config(
    page_title="학생 학습 관리",
    page_icon="📚",
    layout="centered",
)

# 세션 상태 초기화
defaults = {
    "running": False,
    "started_at": None,
    "elapsed_before_start": 0.0,
    "selected_subject": "수학",
    "records": [],
    "subject_input": "수학",
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# 사이드바 메뉴
st.sidebar.title("📚 학습 관리 메뉴")
page = st.sidebar.radio(
    "페이지 선택",
    ["공부 타이머", "오늘 할 일", "공부 회고"],
)

def format_time(seconds):
    hours, remainder = divmod(int(max(0, seconds)), 3600)
    minutes, secs = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"

def current_elapsed():
    elapsed = st.session_state.elapsed_before_start
    if st.session_state.running and st.session_state.started_at is not None:
        elapsed += time.monotonic() - st.session_state.started_at
    return max(0, int(elapsed))

if page == "공부 타이머":
    st.title("⏱️ 공부 타이머")
    st.caption("과목별 공부 시간을 측정하고 기록해 보세요.")

    if st.session_state.running:
        st_autorefresh(interval=1000, key="study_timer_refresh")

    subjects = ["수학", "영어", "국어", "과학", "사회", "기타"]
    subject_choice = st.selectbox(
        "과목 선택",
        subjects,
        index=subjects.index(st.session_state.selected_subject)
        if st.session_state.selected_subject in subjects else 0,
    )
    custom_subject = st.text_input(
        "직접 과목 입력 (선택 사항)",
        value=st.session_state.subject_input,
    )
    active_subject = custom_subject.strip() if custom_subject.strip() else subject_choice

    if st.session_state.running and active_subject != st.session_state.selected_subject:
        st.warning("타이머 실행 중에는 과목을 변경할 수 없습니다. 일시정지 후 변경해 주세요.")
        active_subject = st.session_state.selected_subject
    else:
        st.session_state.selected_subject = active_subject
        st.session_state.subject_input = custom_subject

    st.divider()
    st.subheader(f"현재 과목: {st.session_state.selected_subject}")
    st.markdown(
        f"<div style='text-align:center;font-size:56px;font-weight:700;"
        f"padding:18px 0'>{format_time(current_elapsed())}</div>",
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("▶ 시작", use_container_width=True, disabled=st.session_state.running):
            st.session_state.started_at = time.monotonic()
            st.session_state.running = True
            st.rerun()
    with col2:
        if st.button("⏸ 일시정지", use_container_width=True, disabled=not st.session_state.running):
            st.session_state.elapsed_before_start += time.monotonic() - st.session_state.started_at
            st.session_state.started_at = None
            st.session_state.running = False
            st.rerun()
    with col3:
        if st.button("↺ 초기화", use_container_width=True):
            st.session_state.running = False
            st.session_state.started_at = None
            st.session_state.elapsed_before_start = 0.0
            st.rerun()

    st.caption("초기화는 현재 타이머만 00:00:00으로 되돌립니다. 저장된 기록은 유지됩니다.")

    if st.button("현재 공부 시간 기록하기", type="primary", use_container_width=True):
        seconds = current_elapsed()
        if seconds > 0:
            now = datetime.now()
            st.session_state.records.append({
                "날짜": now.strftime("%Y-%m-%d"),
                "기록 시각": now.strftime("%H:%M:%S"),
                "과목": st.session_state.selected_subject,
                "공부 시간(초)": seconds,
                "공부 시간": format_time(seconds),
            })
            st.session_state.running = False
            st.session_state.started_at = None
            st.session_state.elapsed_before_start = 0.0
            st.success("공부 시간이 기록되었습니다.")
            st.rerun()
        else:
            st.info("기록할 공부 시간이 없습니다. 먼저 타이머를 시작해 주세요.")

    st.divider()
    st.subheader("📚 과목별 학습 기록")

    if st.session_state.records:
        df = pd.DataFrame(st.session_state.records)
        summary = df.groupby("과목", as_index=False)["공부 시간(초)"].sum()
        summary["총 공부 시간"] = summary["공부 시간(초)"].apply(format_time)

        st.markdown("**과목별 누적 시간**")
        st.dataframe(
            summary[["과목", "총 공부 시간"]],
            use_container_width=True,
            hide_index=True,
        )

        st.markdown("**기록 내역**")
        st.dataframe(
            df[["날짜", "기록 시각", "과목", "공부 시간"]],
            use_container_width=True,
            hide_index=True,
        )

        csv_data = df.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            "기록 CSV 다운로드",
            data=csv_data,
            file_name="study_records.csv",
            mime="text/csv",
            use_container_width=True,
        )

        if st.button("전체 기록 삭제", type="secondary"):
            st.session_state.records = []
            st.rerun()
    else:
        st.info("아직 저장된 기록이 없습니다. 공부 시간을 측정한 뒤 기록해 보세요.")

    st.caption(
        "※ 기록은 현재 브라우저 세션에 저장됩니다. "
        "앱을 새로 시작하거나 세션이 종료되면 사라질 수 있으니 CSV로 내려받아 보관하세요."
    )

elif page == "오늘 할 일":
    st.title("📝 오늘 할 일")

elif page == "공부 회고":
    st.title("✍️ 공부 회고")
