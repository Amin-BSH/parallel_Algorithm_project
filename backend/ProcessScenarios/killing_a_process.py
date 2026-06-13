import multiprocessing
import time

from backend.descriptions import SCENARIO_DESCRIPTIONS


def long_running_task():
    """یک پردازش طولانی‌مدت شبیه‌سازی‌شده که هرگز به طور طبیعی در زمان کوتاه تمام نمی‌شود"""
    time.sleep(10)


def run_killing_process(scenario_id):
    manager = multiprocessing.Manager()
    logs = manager.list()

    desc = (
        SCENARIO_DESCRIPTIONS.get("process", {})
        .get("killing_process", {})
        .get(scenario_id, "توضیحات یافت نشد.")
    )

    if scenario_id == 1:
        p = multiprocessing.Process(target=long_running_task)
        p.start()

        logs.append(f"▶️ فرآیند با PID: {p.pid} شروع شد.")
        logs.append(f"آیا فرآیند زنده است؟ {p.is_alive()}")

        time.sleep(0.5)

        logs.append("🛑 ارسال دستور terminate()...")
        p.terminate()
        p.join()

        logs.append(f"آیا فرآیند زنده است؟ {p.is_alive()}")
        logs.append(f"کد خروج (Exit Code): {p.exitcode}")

    elif scenario_id == 2:
        p = multiprocessing.Process(target=long_running_task)
        p.start()

        logs.append(f"▶️ فرآیند با PID: {p.pid} شروع شد.")

        time.sleep(0.5)

        logs.append("☠️ ارسال دستور kill() (توقف اجباری)...")
        p.kill()
        p.join()

        logs.append(f"آیا فرآیند زنده است؟ {p.is_alive()}")
        logs.append(f"کد خروج (Exit Code): {p.exitcode}")

    elif scenario_id == 3:
        p = multiprocessing.Process(target=long_running_task)
        p.start()

        logs.append("▶️ فرآیند شروع شد.")
        p.terminate()
        p.join()

        logs.append(
            "🧹 فرآیند متوقف شد. فراخوانی دستور close() برای آزادسازی منابع سیستم..."
        )
        p.close()

        try:
            logs.append(f"وضعیت حیات پس از کلوز: {p.is_alive()}")
        except ValueError as e:
            logs.append(f"✅ خطای مورد انتظار پس از close رخ داد: {e}")

    else:
        logs.append("شماره سناریو نامعتبر است.")

    logs_output = list(logs)
    return {"description": desc, "output": logs_output}
