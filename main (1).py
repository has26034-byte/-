import streamlit as st
import pandas as pd
import time
from datetime import datetime, date
from streamlit_autorefresh import st_autorefresh

st.set_page_config(
    page_title="학생 학습 관리",
    page_icon="📚",
    layout="centered",
)

# --------------------------------
# 세션 상태 초기화
# --------------------------------
defaults = {
    "running": False,
    "started_at": None,
    "elapsed_before_start": 0.0,
    "selected_subject": "수학",
    "records": [],
    "subject_input": "수학",
    "todo_items": [],
    "study_reviews": [],
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


def format_time(seconds):
    hours, remainder = divmod(int(max(0, seconds)), 3600)
    minutes, secs = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def current_elapsed():
    elapsed = st.session_state.elapsed_before_start
    if st.session_state.running and st.session_state.started_at is not None:
        elapsed += time.monotonic() - st.session_state.started_at
    return max(0, int(elapsed))


# --------------------------------
# 사이드바 메뉴
# --------------------------------
st.sidebar.title("📚 학습 관리 메뉴")

page = st.sidebar.radio(
    "페이지 선택",
    ["공부 타이머", "오늘 할 일", "공부 회고"],
)


# ================================================
# 1. 공부 타이머
# ================================================
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

    active_subject = (
        custom_subject.strip()
        if custom_subject.strip()
        else subject_choice
    )

    if (
        st.session_state.running
        and active_subject != st.session_state.selected_subject
    ):
        st.warning("타이머 실행 중에는 과목을 변경할 수 없습니다. 일시정지 후 변경해 주세요.")
        active_subject = st.session_state.selected_subject
    else:
        st.session_state.selected_subject = active_subject
        st.session_state.subject_input = custom_subject

    st.divider()
    st.subheader(f"현재 과목: {st.session_state.selected_subject}")

    st.markdown(
        f"<div style='text-align:center;font-size:56px;"
        f"font-weight:700;padding:18px 0'>"
        f"{format_time(current_elapsed())}</div>",
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button(
            "▶ 시작",
            use_container_width=True,
            disabled=st.session_state.running,
        ):
            st.session_state.started_at = time.monotonic()
            st.session_state.running = True
            st.rerun()

    with col2:
        if st.button(
            "⏸ 일시정지",
            use_container_width=True,
            disabled=not st.session_state.running,
        ):
            st.session_state.elapsed_before_start += (
                time.monotonic() - st.session_state.started_at
            )
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

    if st.button(
        "현재 공부 시간 기록하기",
        type="primary",
        use_container_width=True,
    ):
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

        summary = df.groupby(
            "과목", as_index=False
        )["공부 시간(초)"].sum()

        summary["총 공부 시간"] = (
            summary["공부 시간(초)"].apply(format_time)
        )

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


# ================================================
# 2. 오늘 할 일
# ================================================
elif page == "오늘 할 일":

    st.title("📝 오늘 할 일")
    st.write("과목과 할 일을 입력한 뒤 추가 버튼을 눌러 주세요.")

    with st.form("todo_add_form", clear_on_submit=True):

        todo_subject = st.selectbox(
            "과목",
            ["수학", "영어", "국어", "과학", "사회", "기타"],
        )

        todo_subject_custom = st.text_input(
            "직접 과목 입력 (선택 사항)",
            placeholder="예: 정보",
        )

        todo_text = st.text_input(
            "할 일",
            placeholder="예: 교과서 20~25쪽 풀기",
        )

        submitted = st.form_submit_button(
            "➕ 추가",
            use_container_width=True,
        )

        if submitted:
            subject = todo_subject_custom.strip() or todo_subject
            task = todo_text.strip()

            if not task:
                st.warning("할 일을 입력해 주세요.")
            else:
                st.session_state.todo_items.append({
                    "과목": subject,
                    "할 일": task,
                    "완료": False,
                })
                st.rerun()

    st.divider()
    st.subheader("📋 할 일 목록")

    if st.session_state.todo_items:

        for index, item in enumerate(st.session_state.todo_items):
            col1, col2 = st.columns([5, 1])

            with col1:
                completed = st.checkbox(
                    f"**[{item['과목']}]** {item['할 일']}",
                    value=item["완료"],
                    key=f"todo_done_{index}",
                )
                st.session_state.todo_items[index]["완료"] = completed

            with col2:
                if st.button("삭제", key=f"todo_delete_{index}"):
                    st.session_state.todo_items.pop(index)
                    st.rerun()

        total = len(st.session_state.todo_items)
        done = sum(
            1 for item in st.session_state.todo_items
            if item["완료"]
        )

        st.progress(done / total)
        st.caption(f"완료 {done}개 / 전체 {total}개")

        if st.button("할 일 전체 삭제"):
            st.session_state.todo_items = []
            st.rerun()

    else:
        st.info("아직 등록된 할 일이 없습니다. 위에서 과목과 할 일을 추가해 보세요.")


# ================================================
# 3. 공부 회고
# ================================================
elif page == "공부 회고":

    st.title("✍️ 공부 회고")
    st.write("오늘의 공부를 돌아보고 내일의 목표를 세워 보세요.")

    st.divider()
    st.subheader("📝 오늘의 공부 회고")

    with st.form("study_review_form", clear_on_submit=True):

        review_date = st.date_input(
            "날짜",
            value=date.today(),
        )

        review_subject = st.selectbox(
            "오늘 공부한 과목",
            ["수학", "영어", "국어", "과학", "사회", "기타"],
        )

        review_study = st.text_area(
            "오늘 공부한 내용",
            placeholder="오늘 무엇을 공부했나요?",
        )

        review_good = st.text_area(
            "오늘 잘한 점",
            placeholder="오늘 스스로 칭찬하고 싶은 점은?",
        )

        review_bad = st.text_area(
            "아쉬웠던 점",
            placeholder="오늘 부족했던 점이나 개선할 점은?",
        )

        review_tomorrow = st.text_area(
            "내일의 공부 목표",
            placeholder="내일은 무엇을 공부할까요?",
        )

        submitted = st.form_submit_button(
            "💾 회고 저장하기",
            use_container_width=True,
        )

        if submitted:
            if not review_study.strip():
                st.warning("오늘 공부한 내용을 입력해 주세요.")
            else:
                st.session_state.study_reviews.append({
                    "날짜": str(review_date),
                    "과목": review_subject,
                    "공부 내용": review_study.strip(),
                    "잘한 점": review_good.strip(),
                    "아쉬운 점": review_bad.strip(),
                    "내일 목표": review_tomorrow.strip(),
                })

                st.success("공부 회고가 저장되었습니다.")
                st.rerun()

    st.divider()
    st.subheader("📚 나의 공부 회고 기록")

    if st.session_state.study_reviews:

        for index, review in enumerate(
            reversed(st.session_state.study_reviews)
        ):
            original_index = len(st.session_state.study_reviews) - 1 - index

            with st.expander(
                f"📅 {review['날짜']} | {review['과목']}"
            ):
                st.markdown("**📖 오늘 공부한 내용**")
                st.write(review["공부 내용"])

                st.markdown("**👍 오늘 잘한 점**")
                st.write(review["잘한 점"] or "작성하지 않았습니다.")

                st.markdown("**💡 아쉬웠던 점**")
                st.write(review["아쉬운 점"] or "작성하지 않았습니다.")

                st.markdown("**🎯 내일의 공부 목표**")
                st.write(review["내일 목표"] or "작성하지 않았습니다.")

                if st.button(
                    "회고 삭제",
                    key=f"delete_review_{original_index}",
                ):
                    st.session_state.study_reviews.pop(original_index)
                    st.rerun()

        review_df = pd.DataFrame(st.session_state.study_reviews)
        review_csv = review_df.to_csv(index=False).encode("utf-8-sig")

        st.download_button(
            "회고 기록 CSV 다운로드",
            data=review_csv,
            file_name="study_reviews.csv",
            mime="text/csv",
            use_container_width=True,
        )

    else:
        st.info("아직 작성한 공부 회고가 없습니다.")
