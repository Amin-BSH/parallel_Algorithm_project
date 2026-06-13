import multiprocessing
import time

from backend.descriptions import SCENARIO_DESCRIPTIONS


def task_with_lock(lock, process_num, shared_logs):
    with lock:
        shared_logs.append(f"🔒 [Lock] my_func called by process N°{process_num}")
        time.sleep(0.1)
        shared_logs.append(f"🔓 [Lock] process N°{process_num} finished its task.")


def task_with_semaphore(sema, process_num, shared_logs):
    with sema:
        shared_logs.append(
            f"🚦 [Semaphore] Process N°{process_num} acquired the resource."
        )
        time.sleep(0.1)
        shared_logs.append(
            f"🟢 [Semaphore] Process N°{process_num} released the resource."
        )


def task_with_barrier(barrier, process_num, shared_logs):
    shared_logs.append(
        f"⏳ [Barrier] Process N°{process_num} is waiting at the barrier..."
    )
    try:
        barrier.wait()
        shared_logs.append(f"🚀 [Barrier] Process N°{process_num} passed the barrier!")
    except multiprocessing.BrokenBarrierError:
        shared_logs.append(
            f"❌ [Barrier] Process N°{process_num} failed due to broken barrier."
        )


def run_synchronizing_processes(scenario_id):
    manager = multiprocessing.Manager()
    logs = manager.list()

    desc = (
        SCENARIO_DESCRIPTIONS.get("process", {})
        .get("synchronizing_processes", {})
        .get(scenario_id, "توضیحات یافت نشد.")
    )

    if scenario_id == 1:
        logs.append("▶️ شروع سناریو ۱: همگام‌سازی با Lock...")
        lock = multiprocessing.Lock()
        processes = []

        for i in range(3):
            p = multiprocessing.Process(target=task_with_lock, args=(lock, i, logs))
            processes.append(p)
            p.start()

        for p in processes:
            p.join()

        logs.append("🏁 سناریو ۱ با موفقیت به پایان رسید.")

    elif scenario_id == 2:
        logs.append("▶️ شروع سناریو ۲: همگام‌سازی با Semaphore...")
        sema = multiprocessing.Semaphore(2)
        processes = []

        for i in range(4):
            p = multiprocessing.Process(
                target=task_with_semaphore, args=(sema, i, logs)
            )
            processes.append(p)
            p.start()

        for p in processes:
            p.join()

        logs.append("🏁 سناریو ۲ با موفقیت به پایان رسید.")

    elif scenario_id == 3:
        logs.append("▶️ شروع سناریو ۳: همگام‌سازی با Barrier...")
        barrier = multiprocessing.Barrier(3)
        processes = []

        for i in range(3):
            p = multiprocessing.Process(
                target=task_with_barrier, args=(barrier, i, logs)
            )
            processes.append(p)
            p.start()

        for p in processes:
            p.join()

        logs.append("🏁 سناریو ۳ با موفقیت به پایان رسید.")

    else:
        logs.append("شماره سناریو نامعتبر است.")

    return {"description": desc, "output": list(logs)}
