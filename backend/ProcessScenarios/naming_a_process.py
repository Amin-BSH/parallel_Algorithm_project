import multiprocessing
import os
import time

from backend.descriptions import SCENARIO_DESCRIPTIONS


def named_worker_task(logs: list):
    current_process = multiprocessing.current_process()
    logs.append(
        f"[PID: {os.getpid()}] 🟢 فرآیند '{current_process.name}' شروع به کار کرد."
    )
    time.sleep(1)
    logs.append(
        f"[PID: {os.getpid()}] 🔴 فرآیند '{current_process.name}' به پایان رسید."
    )


class NamedCustomProcess(multiprocessing.Process):
    def __init__(self, name, logs):

        super().__init__(name=name)
        self.logs = logs

    def run(self):
        current_name = multiprocessing.current_process().name
        self.logs.append(
            f"[PID: {os.getpid()}] 🚀 فرآیند سفارشی '{current_name}' در حال اجراست."
        )
        time.sleep(1)
        self.logs.append(
            f"[PID: {os.getpid()}] 🏁 فرآیند سفارشی '{current_name}' خاتمه یافت."
        )


def run_naming_process(scenario_id):
    manager = multiprocessing.Manager()
    logs = manager.list()

    main_process_name = multiprocessing.current_process().name
    logs.append(f"[Main PID: {os.getpid()}] فرآیند اصلی برنامه: {main_process_name}")

    desc = (
        SCENARIO_DESCRIPTIONS.get("process", {})
        .get("naming_a_process", {})
        .get(scenario_id, "توضیحات یافت نشد.")
    )

    if scenario_id == 1:
        p = multiprocessing.Process(
            target=named_worker_task, name="Worker-Process-1", args=(logs,)
        )
        p.start()
        p.join()

    elif scenario_id == 2:
        p = multiprocessing.Process(target=named_worker_task, args=(logs,))
        p.name = "Renamed-Process-2"
        p.start()
        p.join()

    elif scenario_id == 3:
        p = NamedCustomProcess("Custom-Named-Process-3", logs)
        p.start()
        p.join()

    else:
        logs.append("شماره سناریو نامعتبر است.")

    logs_output = list(logs)
    return {"description": desc, "output": logs_output}
