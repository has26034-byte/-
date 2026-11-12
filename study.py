
# --------------------------------
# 3. 공부 회고
# --------------------------------

elif page == "공부 회고":

    st.title("✍️ 공부 회고")
    st.write("오늘의 공부를 돌아보고 내일의 목표를 세워 보세요.")

    from datetime import date

    # 회고 데이터 초기화
    if "study_reviews" not in st.session_state:
        st.session_state.study_reviews = []

    st.divider()

    st.subheader("📝 오늘의 공부 회고")

    with st.form("study_review_form", clear_on_submit=True):

        review_date = st.date_input(
            "날짜",
            value=date.today()
        )

        review_subject = st.selectbox(
            "오늘 공부한 과목",
            ["수학", "영어", "국어", "과학", "사회", "기타"]
        )

        review_study = st.text_area(
            "오늘 공부한 내용",
            placeholder="오늘 무엇을 공부했나요?"
        )

        review_good = st.text_area(
            "오늘 잘한 점",
            placeholder="오늘 스스로 칭찬하고 싶은 점은?"
        )

        review_bad = st.text_area(
            "아쉬웠던 점",
            placeholder="오늘 부족했던 점이나 개선할 점은?"
        )

        review_tomorrow = st.text_area(
            "내일의 공부 목표",
            placeholder="내일은 무엇을 공부할까요?"
        )

        submitted = st.form_submit_button(
            "💾 회고 저장하기",
            use_container_width=True
        )

        if submitted:

            if not review_study.strip():
                st.warning("오늘 공부한 내용을 입력해 주세요.")

            else:

                st.session_state.study_reviews.append({
                    "날짜": str(review_date),
                    "과목": review_subject,
                    "공부 내용": review_study,
                    "잘한 점": review_good,
                    "아쉬운 점": review_bad,
                    "내일 목표": review_tomorrow
                })

                st.success("공부 회고가 저장되었습니다.")
                st.rerun()

    st.divider()

    st.subheader("📚 나의 공부 회고 기록")

    if st.session_state.study_reviews:

        for index, review in enumerate(
            reversed(st.session_state.study_reviews)
        ):

            original_index = len(
                st.session_state.study_reviews
            ) - 1 - index

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
                    key=f"delete_review_{original_index}"
                ):

                    st.session_state.study_reviews.pop(
                        original_index
                    )

                    st.rerun()

    else:

        st.info("아직 작성한 공부 회고가 없습니다.")
