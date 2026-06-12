import multiprocessing
import time
import os
from backend.descriptions import SCENARIO_DESCRIPTIONS


def background_task(name, logs):
    logs.append(f"[PID: {os.getpid()}] ⚙️ پردازش '{name}' شروع به کار کرد...")
    time.sleep(0.5)
    logs.append(f"[PID: {os.getpid()}] ✅ پردازش '{name}' با موفقیت پایان یافت.")


def daemon_with_child_task(logs):
    logs.append(f"[PID: {os.getpid()}] 😈 پردازش پس‌زمینه (Daemon) شروع شد.")
    try:
        child = multiprocessing.Process(
            target=background_task, args=("Child-Process", logs)
        )
        child.start()
        child.join()
    except Exception as e:
        logs.append(f"❌ خطای مورد انتظار رخ داد: {type(e).__name__} - {str(e)}")


def run_background_process(scenario_id):
    manager = multiprocessing.Manager()
    logs = manager.list()

    desc = (
        SCENARIO_DESCRIPTIONS.get("process", {})
        .get("running_in_background", {})
        .get(scenario_id, "توضیحات یافت نشد.")
    )

    if scenario_id == 1:
        p_normal = multiprocessing.Process(
            target=background_task, args=("Foreground-Worker", logs)
        )
        p_daemon = multiprocessing.Process(
            target=background_task, args=("Background-Worker", logs)
        )

        p_daemon.daemon = True

        logs.append(f"وضعیت ویژگی daemon برای فرآیند عادی: {p_normal.daemon}")
        logs.append(f"وضعیت ویژگی daemon برای فرآیند پس‌زمینه: {p_daemon.daemon}")

        p_normal.start()
        p_daemon.start()

        p_normal.join()
        p_daemon.join()

    elif scenario_id == 2:
        p = multiprocessing.Process(target=background_task, args=("Daemon-Task", logs))
        p.daemon = True

        logs.append(f"پیش از start: آیا فرآیند در حال اجراست؟ {p.is_alive()}")
        p.start()
        logs.append(f"پس از start: آیا فرآیند در حال اجراست؟ {p.is_alive()}")

        p.join()
        logs.append(f"پس از join: آیا فرآیند در حال اجراست؟ {p.is_alive()}")

    elif scenario_id == 3:
        p = multiprocessing.Process(target=daemon_with_child_task, args=(logs,))
        p.daemon = True
        p.start()
        p.join()

    else:
        logs.append("شماره سناریو نامعتبر است.")

    logs_output = list(logs)
    return {"description": desc, "output": logs_output}
