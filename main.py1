        unsafe_allow_html=True
    )

    if len(picked) < 4:
        step = len(picked)
        st.info(
            f"현재 선택: {step + 1}/4  ·  "
            f"{POSITIONS[step][0]} — {POSITIONS[step][1]}"
        )
    else:
        st.success("네 장의 카드가 모두 선택되었어요. 이제 두 사람의 이야기를 확인해 보세요.")

    # 실제 라이더-웨이트 계열 카드 그림을 보여주는 7열 갤러리
    for start in range(0, len(st.session_state.tarot_order), 7):
        row_indices = st.session_state.tarot_order[start:start + 7]
        cols = st.columns(7)
        for col, card_index in zip(cols, row_indices):
            card = CARDS[card_index]
            with col:
                if card["name"] in picked:
                    if card["name"] in CARD_ART:
                        st.markdown('<div class="tarot-card-frame">', unsafe_allow_html=True)
                        st.image(base64.b64decode(CARD_ART[card["name"]]), use_container_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="tarot-card-placeholder">☼<small>THE WORLD</small></div>', unsafe_allow_html=True)
                else:
                    st.markdown(
                        '<div class="tarot-card-back"><span class="tarot-card-back-mark top">THE TAROT</span>'
                        '<span class="tarot-card-back-mark bottom">✧  ✧  ✧</span></div>',
                        unsafe_allow_html=True
                    )
                if card["name"] in picked:
                    st.button(
                        "선택 완료",
                        key=f"tarot_done_{card_index}",
                        disabled=True,
                        use_container_width=True
                    )
                elif len(picked) >= 4:
                    st.button(
                        "선택 마감",
                        key=f"tarot_closed_{card_index}",
                        disabled=True,
                        use_container_width=True
                    )
                else:
                    if st.button(
                        "선택",
                        key=f"tarot_pick_{card_index}",
                        use_container_width=True
                    ):
                        st.session_state.tarot_picked.append(card["name"])
                        st.session_state.pop("tarot_show_result", None)
                        st.rerun()

    if picked:
        st.markdown("---")
        st.markdown("### 🌟 선택한 카드")
        chosen_cols = st.columns(4)
        for i, card_name in enumerate(picked):
            card = get_card(card_name)
            with chosen_cols[i]:
                if card_name in CARD_ART:
                    st.markdown('<div class="tarot-card-frame">', unsafe_allow_html=True)
                    st.image(base64.b64decode(CARD_ART[card_name]), use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="tarot-card-placeholder">☼<small>THE WORLD</small></div>', unsafe_allow_html=True)
                st.markdown(f"<div class='tarot-position'><b>{card['name']}</b><br>{card['keyword']}</div>", unsafe_allow_html=True)
                st.caption(POSITIONS[i][0])

    if len(picked) == 4:
        st.markdown("---")
        if st.button(
            "🌙 내 타로 리딩 확인하기",
            type="primary",
            use_container_width=True,
            key="tarot_read_button"
        ):
            if not question.strip():
                st.warning("먼저 궁금한 질문을 적어주세요.")
                st.session_state.tarot_show_result = False
            else:
                st.session_state.tarot_show_result = True

        if st.session_state.get("tarot_show_result", False) and question.strip():
            with st.spinner("네 장의 카드에 담긴 상징을 해석하고 있어요..."):
                reading = ai_reading(question.strip(), picked)

            st.markdown("---")
            st.markdown("## 🔮 두 사람의 타로 리딩")
            if reading:
                st.markdown(reading)
                st.caption(
                    "선택한 카드에 미리 준비된 해석을 조합한 오락·자기성찰용 리딩입니다. "
                    "외부 API 연결이나 비용이 발생하지 않습니다."
                )
            else:
                st.markdown(
                    build_reading(question.strip(), picked),
                    unsafe_allow_html=True
                )
                st.caption(
                    "앱에 포함된 카드 해석 데이터만 사용합니다. 외부 API 연결이나 비용이 발생하지 않습니다."
                )

    st.markdown("---")
    st.markdown(
        '<p class="tarot-note">✦ 타로는 미래나 상대방의 실제 마음을 '
        '확정하는 도구가 아니라, 관계를 다른 시각으로 생각해 보는 '
        '오락·자기성찰 콘텐츠입니다. 실제 관계에서는 서로의 말과 행동, '
        '존중과 대화가 가장 중요해요.</p>',
        unsafe_allow_html=True
    )

    if st.button("↻ 타로 카드 다시 뽑기", use_container_width=True, key="tarot_reset"):
        st.session_state.tarot_picked = []
        new_order = list(range(len(CARDS)))
        random.shuffle(new_order)
        st.session_state.tarot_order = new_order
        st.session_state.pop("tarot_show_result", None)
        st.rerun()
