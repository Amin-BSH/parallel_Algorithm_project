import multiprocessing
import os
import time

from backend.descriptions import SCENARIO_DESCRIPTIONS


def simple_task(logs: list):
    logs.append(f"PPID(Parent Process ID): {os.getppid()} 🟡")
    logs.append(f"[PID: {os.getpid()}] 🟢 فرآیند ساده شروع به کار کرد.")
    time.sleep(1)
    logs.append(f"[PID: {os.getpid()}] 🔴 فرآیند ساده به پایان رسید.")


def worker_task(worker_id, data, logs):
    logs.append(f"PPID(Parent Process ID): {os.getppid()} 🟡")
    logs.append(
        f"[PID: {os.getpid()}] 👷‍♂️ کارگر {worker_id} در حال پردازش داده: {data}"
    )
    time.sleep(1.5)
    logs.append(f"[PID: {os.getpid()}] ✅ کارگر {worker_id} کار خود را تمام کرد.")


class CustomProcess(multiprocessing.Process):
    def __init__(self, name, logs):
        super().__init__()
        self.custom_name = name
        self.logs = logs

    def run(self):
        self.logs.append(
            f"[PID: {os.getpid()}] 🚀 فرآیند سفارشی '{self.custom_name}' در حال اجراست."
        )
        time.sleep(1)
        self.logs.append(
            f"[PID: {os.getpid()}] 🏁 فرآیند سفارشی '{self.custom_name}' خاتمه یافت."
        )


def run_spawning_process(scenario_id):
    manager = multiprocessing.Manager()
    logs = manager.list()

    logs.append(f"[Main PID: {os.getpid()}] فرآیند اصلی برنامه")

    desc = (
        SCENARIO_DESCRIPTIONS.get("process", {})
        .get("spawning_a_thread", {})
        .get(scenario_id, "توضیحات یافت نشد.")
    )

    if scenario_id == 1:
        p = multiprocessing.Process(target=simple_task, args=(logs,))
        p.start()
        p.join()

    elif scenario_id == 2:
        processes = []
        datasets = ["تصاویر", "متون", "ویدیوها"]

        for i, data in enumerate(datasets):
            p = multiprocessing.Process(target=worker_task, args=(i + 1, data, logs))
            processes.append(p)
            p.start()

        for p in processes:
            p.join()

    elif scenario_id == 3:
        p1 = CustomProcess("Alpha", logs)
        p2 = CustomProcess("Beta", logs)

        p1.start()
        p2.start()

        p1.join()
        p2.join()

    else:
        logs.append("شماره سناریو نامعتبر است.")

    logs_output = list(logs)
    return {"description": desc, "output": logs_output}
