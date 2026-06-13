import multiprocessing
import time

from backend.descriptions import SCENARIO_DESCRIPTIONS


def worker_map(x):
    time.sleep(0.1)
    return f"✅ پردازش مقدار {x}: مربع آن برابر است با {x * x}"


def worker_async(name):
    time.sleep(0.2)
    return f"👋 سلام {name}! این پیام از یک فرآیند ناهمگام آمده است."


def worker_imap(task_id):
    sleep_time = 0.3 if task_id % 2 == 0 else 0.1
    time.sleep(sleep_time)
    return f"⚙️ وظیفه {task_id} تکمیل شد (زمان اجرا: {sleep_time}s)"


def run_using_a_process_pool(scenario_id):
    manager = multiprocessing.Manager()
    logs = manager.list()

    desc = (
        SCENARIO_DESCRIPTIONS.get("process", {})
        .get("using_a_process_pool", {})
        .get(scenario_id, "توضیحات یافت نشد.")
    )

    if scenario_id == 1:
        logs.append("▶️ شروع سناریو ۱: توزیع وظایف با Pool.map...")
        data = [1, 2, 3, 4, 5]

        with multiprocessing.Pool(processes=3) as pool:
            results = pool.map(worker_map, data)

        for res in results:
            logs.append(res)

        logs.append("🏁 سناریو ۱ با موفقیت به پایان رسید.")

    elif scenario_id == 2:
        logs.append("▶️ شروع سناریو ۲: اجرای ناهمگام با Pool.apply_async...")
        names = ["علی", "مریم", "سارا"]

        def log_result(result):
            logs.append(f"📥 دریافت نتیجه در Callback: {result}")

        with multiprocessing.Pool(processes=2) as pool:
            for name in names:
                pool.apply_async(worker_async, args=(name,), callback=log_result)

            pool.close()
            pool.join()

        logs.append("🏁 سناریو ۲ با موفقیت به پایان رسید.")

    elif scenario_id == 3:
        logs.append("▶️ شروع سناریو ۳: پردازش نامنظم با Pool.imap_unordered...")
        tasks = [1, 2, 3, 4, 5]

        with multiprocessing.Pool(processes=3) as pool:
            for result in pool.imap_unordered(worker_imap, tasks):
                logs.append(result)

        logs.append("🏁 سناریو ۳ با موفقیت به پایان رسید.")

    else:
        logs.append("شماره سناریو نامعتبر است.")

    return {"description": desc, "output": list(logs)}
