import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

# 1. 페이지 기본 설정
st.set_page_config(page_title="Ham's app", layout="wide")

# 2. 왼쪽 사이드바 메뉴 만들기
st.sidebar.title("🧮 메뉴")
menu = st.sidebar.radio("원하는 기능을 선택하세요:", 
                        ["선형 보간법 (Linear Interpolation)", 
                         "상대습도 계산기 (Relative Humidity)",
                         "소성 승온 스케줄러 (Calcination)",
                         "📅 샘플 분석 "])

# ---------------------------------------------------------
# [기능 1] 선형 보간법 계산기
# ---------------------------------------------------------
if menu == "선형 보간법 (Linear Interpolation)":
    st.title("📈 선형 보간법 계산기")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("첫 번째 점 (Point 1)")
        x1 = st.number_input("x1 값을 입력하세요", value=0.0)
        y1 = st.number_input("y1 값을 입력하세요", value=0.0)
    with col2:
        st.subheader("두 번째 점 (Point 2)")
        x2 = st.number_input("x2 값을 입력하세요", value=10.0)
        y2 = st.number_input("y2 값을 입력하세요", value=100.0)
    
    st.divider()
    target_x = st.number_input("💡 구하고 싶은 y값의 x 좌표를 입력하세요", value=5.0)
    
    if st.button("계산하기", key="btn_linear"):
        if x1 == x2:
            st.error("x1과 x2의 값이 같으면 계산할 수 없습니다.")
        else:
            target_y = y1 + ((target_x - x1) * (y2 - y1) / (x2 - x1))
            st.success(f"결과: x가 {target_x}일 때, y값은 **{target_y:.4f}** 입니다!")

# ---------------------------------------------------------
# [기능 2] 상대습도 & 수증기압 계산기
# ---------------------------------------------------------
elif menu == "상대습도 계산기 (Relative Humidity)":
    st.title("💧 상대습도 & 수증기압 계산기")
    col1, col2 = st.columns(2)
    with col1:
        T = st.number_input("온도 (℃)", value=25.0, step=0.1)
    with col2:
        RH = st.number_input("목표 상대습도 (RH %)", value=80.0, min_value=0.0, max_value=100.0, step=1.0)
    
    if st.button("습도 계산하기", key="btn_rh"):
        A, B, C = 8.07131, 1730.63, 233.426
        P_sat_mmHg = 10 ** (A - (B / (T + C)))
        P_sat_kPa = P_sat_mmHg * 0.133322
        P_act_mmHg = P_sat_mmHg * (RH / 100)
        P_act_kPa = P_sat_kPa * (RH / 100)
        T_kelvin = T + 273.15
        AH = (2.16679 * P_act_kPa * 1000) / T_kelvin
        st.success("계산 완료!")
        st.info(f"""
        🌡️ **입력 조건:** {T} ℃ / {RH}% RH
        - **포화 수증기압 (100% RH):** {P_sat_mmHg:.2f} mmHg (`{P_sat_kPa:.2f} kPa`)
        - **현재 조건의 실제 수증기압:** {P_act_mmHg:.2f} mmHg (`{P_act_kPa:.2f} kPa`)
        - **현재 조건의 절대습도:** {AH:.2f} g/m³
        """)

# ---------------------------------------------------------
# [기능 3] 소성 승온 스케줄러 (Calcination)
# ---------------------------------------------------------
elif menu == "소성 승온 스케줄러 (Calcination)":
    st.title("🔥 소성(Calcination) 승온 스케줄러")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("온도 설정 (℃)")
        start_temp = st.number_input("시작 온도", value=25.0, step=1.0)
        target_temp = st.number_input("목표 온도", value=500.0, step=10.0)
        ramp_rate = st.number_input("승온 속도 (℃/min)", value=5.0, step=0.1)

    with col2:
        st.subheader("시간 설정")
        hold_hours = st.number_input("목표 온도 유지 시간 (시간)", value=4, min_value=0)
        hold_mins = st.number_input("목표 온도 유지 시간 (분)", value=0, min_value=0, max_value=59)
        
        st.divider()
        start_time = st.time_input("실험 시작(예정) 시각", value="now") 

    if st.button("스케줄 계산하기", key="btn_calcination"):
        if target_temp <= start_temp:
            st.error("목표 온도는 시작 온도보다 높아야 합니다.")
        elif ramp_rate <= 0:
            st.error("승온 속도는 0보다 커야 합니다.")
        else:
            ramp_time_min = (target_temp - start_temp) / ramp_rate
            total_min = ramp_time_min + (hold_hours * 60) + hold_mins
            total_hours_display = int(total_min // 60)
            total_mins_display = int(total_min % 60)

            today = datetime.today()
            start_datetime = datetime.combine(today, start_time)
            end_datetime = start_datetime + timedelta(minutes=total_min)

            st.success("계산 완료!")
            st.info(f"""
            ⏱️ **총 소요 시간:** {total_hours_display}시간 {total_mins_display}분
            (승온 소요: {int(ramp_time_min//60)}시간 {int(ramp_time_min%60)}분 / 유지: {hold_hours}시간 {hold_mins}분)
            🕒 **작동 종료 예정 시각:** {end_datetime.strftime('%Y년 %m월 %d일 %p %I시 %M분').replace('AM', '오전').replace('PM', '오후')}
            """)

# ---------------------------------------------------------
# [기능 4] 내 일정 스케줄러 (달력 & 자동 정렬 & 다중 체크 완벽 호환)
# ---------------------------------------------------------
elif menu == "📅 샘플 분석 ":
    st.title("📅 분석 맡김")


    FILE_NAME = "my_schedule.csv"

    if os.path.exists(FILE_NAME):
        df = pd.read_csv(FILE_NAME)
        if "완료여부" not in df.columns:
            df["완료여부"] = False
        df["날짜"] = pd.to_datetime(df["날짜"]).dt.date
    else:
        df = pd.DataFrame(columns=["날짜", "일정 내용", "완료여부"])

    # 1. 일정 추가 폼
    with st.form("schedule_form", clear_on_submit=True):
        col1, col2 = st.columns([1, 3])
        with col1:
            date_input = st.date_input("🗓️ 날짜 선택")
        with col2:
            task_input = st.text_input("📝 샘플", placeholder="예: 샘플이름/분석 기기")
        
        submitted = st.form_submit_button("일정 추가하기")

        if submitted:
            if task_input.strip() == "":
                st.warning("일정 내용을 입력해 주세요!")
            else:
                new_data = pd.DataFrame([{"날짜": date_input, "일정 내용": task_input, "완료여부": False}])
                df = pd.concat([df, new_data], ignore_index=True)
                df.to_csv(FILE_NAME, index=False)
                st.success("일정이 성공적으로 추가되었습니다!")
                st.rerun()

    st.divider()

    # 💡 2. 화면을 두 개의 '탭(Tab)'으로 나누기
    tab1, tab2 = st.tabs(["📌 해야 할 일 (To-Do)", "분석 완료"])

    # --- 탭 1: 해야 할 일 ---
    with tab1:
        todo_df = df[df["완료여부"] == False].sort_values(by="날짜")

        if todo_df.empty:
            st.info("현재 남은 샘플이 없습니다. 👏")
        else:
            edited_todo = st.data_editor(
                todo_df,
                column_config={
                    "완료여부": st.column_config.CheckboxColumn(
                        "끝냈나요?",
                        help="분석을 끝냈다면 체크하세요!",
                        default=False,
                    ),
                    "날짜": st.column_config.DateColumn("날짜", disabled=True),
                    "일정 내용": st.column_config.TextColumn("일정 내용", disabled=True)
                },
                hide_index=True,
                use_container_width=True
            )

            if st.button("✅ 체크한 일정 완료 처리하기 (보관함으로 이동)"):
                df.update(edited_todo)
                df.to_csv(FILE_NAME, index=False)
                st.rerun() 

    # --- 탭 2: 완료된 일정 보관함 ---
    with tab2:
        # 완료된 항목만 가져와서, 최근에 완료한 날짜가 맨 위로 오도록 정렬 (내림차순)
        done_df = df[df["완료여부"] == True].sort_values(by="날짜", ascending=False)
        
        if done_df.empty:
            st.info("아직 완료된 일정이 없습니다. 첫 번째 목표를 달성해 보세요!")
        else:
            st.success(f"🎉 지금까지 총 {len(done_df)}개의 일정을 완료하셨습니다!")
            # 완료된 일정은 수정할 필요가 없으므로 깔끔하게 표로만 출력
            st.dataframe(
                done_df[["날짜", "일정 내용"]], 
                hide_index=True, 
                use_container_width=True
            )
            
            # 혹시나 보관함 기록마저 아예 지워버리고 싶을 때를 대비한 버튼
            st.divider()
            if st.button("🗑️ 보관함 기록 모두 영구 삭제하기"):
                df = df[df["완료여부"] == False] # 안 끝난 일만 남기고 덮어쓰기
                df.to_csv(FILE_NAME, index=False)
                st.rerun()