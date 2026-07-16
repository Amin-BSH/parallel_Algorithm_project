import base64
import os
from pathlib import Path

import requests
import streamlit as st


def load_font():
    font_path = Path(__file__).parent / "fonts" / "Vazir-Thin.ttf"

    with open(font_path, "rb") as f:
        font_data = f.read()

    font_base64 = base64.b64encode(font_data).decode()

    st.markdown(
        f"""
        <style>
        @font-face {{
            font-family: 'Vazir';
            src: url(data:font/ttf;base64,{font_base64}) format('truetype');
            font-weight: 500;
            font-style: normal;
        }}

        html, body, * {{
            font-family: 'Vazir', sans-serif !important;
            direction: rtl;
            text-align: right;
        }}

        /* keep code blocks LTR */
        pre, code {{
            direction: ltr;
            text-align: left;
        }}

        /* fix inputs & labels */
        label {{
            direction: rtl;
            text-align: right;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


load_font()

st.set_page_config(
    page_title="Parallel Processing Project", page_icon="🚀", layout="centered"
)

st.title("🚀 پروژه نهایی: پردازش موازی در پایتون")
st.markdown("---")

col1, col2, col3 = st.columns(3)
with col1:
    method_display = st.selectbox(
        "⚙️ روش همزمانی:", ["نخ (Thread)", "فرآیند (Process)"])
    method_map = {"نخ (Thread)": "thread", "فرآیند (Process)": "process"}

with col2:
    tool_display = (
        st.selectbox(
            "🛠️ ابزار همزمانی:",
            [
                "Basic Thread",
                "Determining Current Thread",
                "Subclass",
                "Lock",
                "RLock",
                "Semaphore",
                "Condition",
                "Event",
                "Barrier",
                "Queue",
            ],
        )
        if method_display == "نخ (Thread)"
        else st.selectbox(
            "🛠️ ابزار همزمانی:",
            [
                "Spawning a Process",
                "Naming a Process",
                "Running a Process in Background",
                "Killing a Process",
                "Subclassing a Process",
                "Queue",
                "Synchronizing Processes",
                "Using a Process Pool",
            ],
        )
    )
    tool_map = {
        "Basic Thread": "basic_thread",
        "Determining Current Thread": "determining_current_thread",
        "Subclass": "subclass",
        "Lock": "lock",
        "RLock": "rlock",
        "Semaphore": "semaphore",
        "Condition": "condition",
        "Event": "event",
        "Barrier": "barrier",
        "Queue": "queue",
        "Spawning a Process": "spawning_a_process",
        "Naming a Process": "naming_a_process",
        "Running a Process in Background": "running_a_process_in_background",
        "Killing a Process": "killing_a_process",
        "Subclassing a Process": "subclassing_process",
        "Queue": "queue",  # noqa: F601
        "Synchronizing Processes": "synchronizing_processes",
        "Using a Process Pool": "using_a_process_pool",
    }

with col3:
    scenario_id = st.selectbox("📝 شماره سناریو:", [1, 2, 3])

if st.button("▶️ اجرای سناریو", type="primary"):
    with st.spinner("⏳ در حال پردازش و ارتباط با سرور..."):
        payload = {
            "method": method_map[method_display],
            "tool": tool_map[tool_display],
            "scenario_id": scenario_id,
        }
        BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

        try:
            response = requests.post(
                f"{BACKEND_URL}/run-scenario", json=payload)

            if response.status_code == 200:
                data = response.json()

                st.info(data.get("description", "توضیحاتی یافت نشد."))
                st.subheader("🖥️ خروجی اجرا:")
                with st.container():
                    for log in data.get("output", []):
                        st.code(log, language="text")
            else:
                st.error(f"❌ خطایی در سرور رخ داد: {response.text}")

        except requests.exceptions.ConnectionError:
            st.error(
                "🔌 خطا: ارتباط با سرور بک‌اند (FastAPI) برقرار نشد. مطمئن شوید که سرور روشن است."
            )
