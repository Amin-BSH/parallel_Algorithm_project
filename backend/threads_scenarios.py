import os
import random
import threading
import time
from random import randint
from threading import Thread

from backend.descriptions import SCENARIO_DESCRIPTIONS


def run_basic_thread(scenario_id: int):
    output_log = []
    description = ""

    if scenario_id == 1:
        description = SCENARIO_DESCRIPTIONS["thread"]["defining_thread"].get(
            scenario_id, "سناریو یافت نشد"
        )

        def send_email(user):
            output_log.append(f"شروع ارسال ایمیل به {user}...")
            time.sleep(random.uniform(0.5, 2.5))
            output_log.append(f"ایمیل با موفقیت به {user} ارسال شد.")

        users = ["Ali", "Sara", "Reza"]
        threads = [threading.Thread(target=send_email, args=(u,)) for u in users]

        for t in threads:
            t.start()
        for t in threads:
            t.join()

    elif scenario_id == 2:
        description = SCENARIO_DESCRIPTIONS["thread"]["defining_thread"][2]

        def download_chunk(chunk_id):
            output_log.append(f"در حال دانلود قطعه {chunk_id}...")
            time.sleep(random.uniform(0.5, 2.5))
            output_log.append(f"دانلود قطعه {chunk_id} تکمیل شد.")

        threads = [
            threading.Thread(target=download_chunk, args=(i,)) for i in range(1, 4)
        ]

        for t in threads:
            t.start()
        for t in threads:
            t.join()

    elif scenario_id == 3:
        description = SCENARIO_DESCRIPTIONS["thread"]["defining_thread"][3]

        def read_sensor(sensor_name):
            output_log.append(f"اتصال به سنسور {sensor_name}...")
            time.sleep(random.uniform(0.5, 2.5))
            output_log.append(f"داده از سنسور {sensor_name} دریافت شد.")

        sensors = ["دما", "رطوبت", "فشار"]
        threads = [threading.Thread(target=read_sensor, args=(s,)) for s in sensors]

        for t in threads:
            t.start()
        for t in threads:
            t.join()
    else:
        description = "شماره سناریو نامعتبر است."

    return {"output": output_log, "description": description}


def run_determining_current_thread(scenario_id: int):
    description = SCENARIO_DESCRIPTIONS["thread"]["determining_the_current_thread"][
        scenario_id
    ]
    logs = []

    if scenario_id == 1:
        logs.append("شروع سناریو ۱: سرویس‌های پس‌زمینه سیستم...\n")

        def service_task():
            thread_name = threading.current_thread().name
            logs.append(f"[{thread_name}] --> شروع به کار کرد.\n")
            time.sleep(random.uniform(1.0, 2.0))
            logs.append(f"[{thread_name}] --> عملیاتش تمام شد و خارج شد.\n")

        t1 = threading.Thread(name="LoggerService", target=service_task)
        t2 = threading.Thread(name="MonitorService", target=service_task)
        t3 = threading.Thread(name="BackupService", target=service_task)

        threads = [t1, t2, t3]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        logs.append("\n✅ تمامی سرویس‌ها با موفقیت کار خود را به پایان رساندند.")

        return {"description": description, "output": logs}

    elif scenario_id == 2:
        logs.append("شروع سناریو ۲: کارگران خط تولید دیتا...\n")

        def worker_pipeline():
            current_name = threading.current_thread().name
            logs.append(f"کارگر [{current_name}] وارد خط تولید شد.\n")

            if current_name == "DataFetcher":
                logs.append(f"[{current_name}]: در حال استخراج داده‌ها از API...\n")
                time.sleep(1)
            elif current_name == "DataProcessor":
                logs.append(f"[{current_name}]: در حال پردازش و پاکسازی داده‌ها...\n")
                time.sleep(1.5)
            elif current_name == "DataSaver":
                logs.append(f"[{current_name}]: در حال ذخیره داده‌ها در دیتابیس...\n")
                time.sleep(0.5)

            logs.append(f"کارگر [{current_name}] کارش را تمام کرد.\n")

        t1 = threading.Thread(name="DataFetcher", target=worker_pipeline)
        t2 = threading.Thread(name="DataProcessor", target=worker_pipeline)
        t3 = threading.Thread(name="DataSaver", target=worker_pipeline)

        threads = [t1, t2, t3]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        return {"description": description, "output": logs}

    elif scenario_id == 3:
        logs.append("شروع سناریو ۳: تفکیک نخ اصلی از فرعی...\n")

        current_thread_name = threading.current_thread().name
        logs.append(f"👑 نام نخ اجرا کننده این خط: {current_thread_name}\n")

        def background_task():
            current = threading.current_thread()
            logs.append(f"👻 نام نخ پس‌زمینه: {current.name}\n")
            logs.append(
                f"آیا این نخ همان نخ اصلی است؟ {'بله' if current.name == 'MainThread' else 'خیر'}\n"
            )
            time.sleep(1.5)
            logs.append(f"👻 کار نخ پس‌زمینه ({current.name}) تمام شد.\n")

        bg_thread = threading.Thread(name="BackgroundWorker-1", target=background_task)
        bg_thread.start()

        active_threads = threading.enumerate()
        logs.append(
            f"\n📊 لیست تمام نخ‌های فعال در این لحظه ({len(active_threads)} مورد):\n"
        )
        for th in active_threads:
            logs.append(f" - {th.name}\n")

        bg_thread.join()

        return {"description": description, "output": logs}


def run_thread_subclass(scenario_id: int):
    logs = []
    description = SCENARIO_DESCRIPTIONS["thread"]["thread_subclass"].get(
        scenario_id, "سناریوی نامعتبر یافت نشد."
    )

    if scenario_id == 1:

        class MyThreadClass(Thread):
            def __init__(self, name, duration):
                Thread.__init__(self)
                self.name = name
                self.duration = duration

            def run(self):
                logs.append(
                    f"---> {self.name} در حال اجرا متعلق به واحد اجرایی با شناسه {os.getpid()}\n"
                )
                time.sleep(self.duration)
                logs.append(f"---> {self.name} (خوابیده {self.duration}s)\n")

        start_time = time.time()
        threads = []

        for i in range(1, 10):
            t = MyThreadClass(f"نخ#{i}", randint(1, 3))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        logs.append("پایان")
        logs.append("--- %.4f ثانیه ---\n" % (time.time() - start_time))

    elif scenario_id == 2:

        class CalculatorThread(Thread):
            def __init__(self, number):
                super().__init__()
                self.number = number
                self.result = None

            def run(self):
                logs.append(
                    f"[محاسبات] نخ داره محاسبه میکنه توان دوم {self.number}...\n"
                )
                time.sleep(0.5)
                self.result = self.number**2

        threads = []
        numbers_to_calc = [4, 7, 12]

        for num in numbers_to_calc:
            t = CalculatorThread(num)
            threads.append(t)
            t.start()

        for t in threads:
            t.join()
            logs.append(f"[نتیجه] توان دوم {t.number} هست {t.result}\n")

    elif scenario_id == 3:

        class WorkerThread(Thread):
            def __init__(self, name, shared_list):
                super().__init__()
                self.name = name
                self.shared_list = shared_list

            def run(self):
                logs.append(f"[{self.name}] اضافه کردن داده ها به لیست اشتراکی.\n")
                time.sleep(0.2)
                self.shared_list.append(f"داده از {self.name}")

        shared_results = []
        threads = []

        for i in range(1, 4):
            t = WorkerThread(f"کارگر-{i}", shared_results)
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        logs.append("\کار کارگر ها تمام شد. محتویات لیست اشتراکی نهایی:\n")
        for item in shared_results:
            logs.append(f" - {item}\n")

    return {"description": description, "output": logs}


def run_lock_thread(scenario_id: int):
    output_log = []
    description = ""
    lock = threading.Lock()

    if scenario_id == 1:
        description = SCENARIO_DESCRIPTIONS["thread"]["lock"][1]
        tickets = 1

        def book_ticket(user_id):
            nonlocal tickets
            output_log.append(f"کاربر {user_id} در حال بررسی ظرفیت بلیت...")
            with lock:
                if tickets > 0:
                    time.sleep(0.1)
                    tickets -= 1
                    output_log.append(
                        f"✅ بلیت با موفقیت برای کاربر {user_id} رزرو شد."
                    )
                else:
                    output_log.append(f"❌ کاربر {user_id} موفق نشد. ظرفیت تکمیل است.")

        threads = [threading.Thread(target=book_ticket, args=(i,)) for i in range(1, 4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

    elif scenario_id == 2:
        description = SCENARIO_DESCRIPTIONS["thread"]["lock"][2]
        balance = 1000
        output_log.append(f"موجودی اولیه: {balance} تومان")

        def transaction(amount, t_type):
            nonlocal balance
            with lock:
                temp = balance
                time.sleep(0.05)
                if t_type == "deposit":
                    balance = temp + amount
                    output_log.append(
                        f"💰 واریز {amount} تومان. موجودی جدید: {balance}"
                    )
                elif t_type == "withdraw":
                    if temp >= amount:
                        balance = temp - amount
                        output_log.append(
                            f"💸 برداشت {amount} تومان. موجودی جدید: {balance}"
                        )
                    else:
                        output_log.append(
                            f"❌ موجودی کافی نیست برای برداشت {amount} تومان."
                        )

        threads = [
            threading.Thread(target=transaction, args=(500, "deposit")),
            threading.Thread(target=transaction, args=(200, "withdraw")),
            threading.Thread(target=transaction, args=(800, "withdraw")),
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

    elif scenario_id == 3:
        description = SCENARIO_DESCRIPTIONS["thread"]["lock"][3]
        views = 0

        def add_view():
            nonlocal views
            with lock:
                temp = views
                time.sleep(0.01)
                views = temp + 1

        threads = [threading.Thread(target=add_view) for _ in range(50)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        output_log.append(
            f"تعداد بازدید ثبت شده با موفقیت: {views} (از 50 درخواست همزمان)"
        )

    else:
        description = "شماره سناریو نامعتبر است."

    return {"output": output_log, "description": description}


def run_rlock_thread(scenario_id: int):
    logs = []
    desc = (
        SCENARIO_DESCRIPTIONS.get("thread", {})
        .get("rlock", {})
        .get(scenario_id, "Description not found.")
    )
    if scenario_id == 1:
        rlock = threading.RLock()
        shared_inventory = {"items": 0}

        class InventoryManager:
            def log_addition(self, thread_name, count):
                with rlock:
                    logs.append(
                        f"[{thread_name}] قفل RLock در log_addition() دریافت شد."
                    )
                    time.sleep(random.uniform(0.1, 0.3))
                    logs.append(f"[{thread_name}] ثبت شد: {count} آیتم اضافه گردید.")

            def add_items(self, thread_name, count):
                with rlock:
                    logs.append(
                        f"[{thread_name}] قفل RLock در add_items() دریافت شد. در حال شروع افزودن..."
                    )
                    shared_inventory["items"] += count
                    self.log_addition(thread_name, count)
                    logs.append(
                        f"[{thread_name}] افزودن آیتم‌ها پایان یافت. مجموع اکنون {shared_inventory['items']} است."
                    )

        manager = InventoryManager()

        def worker(name, items_to_add):
            logs.append(f"[{name}] در حال تلاش برای افزودن {items_to_add} آیتم...")
            manager.add_items(name, items_to_add)

        threads = [
            threading.Thread(target=worker, args=(f"Thread-{i}", random.randint(1, 5)))
            for i in range(3)
        ]

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        logs.append(f"[نخ اصلی] موجودی نهایی انبار: {shared_inventory['items']} آیتم.")

    elif scenario_id == 2:
        rlock = threading.RLock()

        def recursive_factorial(n, thread_name):
            with rlock:
                logs.append(f"[{thread_name}] قفل برای n={n} دریافت شد.")
                time.sleep(0.1)
                if n == 0 or n == 1:
                    logs.append(
                        f"[{thread_name}] رسیدن به شرط پایه (n={n}). در حال آزادسازی قفل..."
                    )
                    return 1
                else:
                    result = n * recursive_factorial(n - 1, thread_name)
                    logs.append(
                        f"[{thread_name}] محاسبه فاکتوریل برای n={n} انجام شد. در حال آزادسازی..."
                    )
                    return result

        def worker(num):
            thread_name = threading.current_thread().name
            logs.append(f"[{thread_name}] شروع محاسبه بازگشتی فاکتوریل برای {num}")
            res = recursive_factorial(num, thread_name)
            logs.append(f"[{thread_name}] نتیجه نهایی برای {num}! = {res}")

        threads = [
            threading.Thread(target=worker, args=(3,), name="FactThread-1"),
            threading.Thread(target=worker, args=(4,), name="FactThread-2"),
        ]

        for t in threads:
            t.start()
        for t in threads:
            t.join()

    elif scenario_id == 3:
        rlock = threading.RLock()

        def backup_db(thread_name):
            with rlock:
                logs.append(f"[{thread_name}] قفل RLock برای بک‌آپ دیتابیس دریافت شد.")
                time.sleep(0.2)
                logs.append(f"[{thread_name}] بک‌آپ دیتابیس تکمیل شد.")

        def backup_files(thread_name):
            with rlock:
                logs.append(f"[{thread_name}] قفل RLock برای بک‌آپ فایل‌ها دریافت شد.")
                time.sleep(0.2)
                logs.append(f"[{thread_name}] بک‌آپ فایل‌ها تکمیل شد.")

        def full_system_backup(thread_name):
            with rlock:
                logs.append(
                    f"[{thread_name}] --- شروع بک‌آپ کامل سیستم (دریافت قفل اصلی) ---"
                )
                backup_db(thread_name)
                backup_files(thread_name)
                logs.append(f"[{thread_name}] --- بک‌آپ کامل سیستم به پایان رسید ---")

        threads = [
            threading.Thread(target=full_system_backup, args=("BackupAgent-1",)),
            threading.Thread(target=backup_db, args=("IndependentDB-Backup",)),
        ]

        for t in threads:
            t.start()
        for t in threads:
            t.join()

    else:
        logs.append("شناسه سناریو نامعتبر است.")

    return {"description": desc, "output": logs}


def run_semaphore_thread(scenario_id: int):
    output_log = []
    description = ""

    if scenario_id == 1:
        description = SCENARIO_DESCRIPTIONS["thread"]["semaphore"][1]
        spots = 3
        semaphore = threading.Semaphore(spots)

        def car_enter_parking(car_id):
            output_log.append(f"🚗 ماشین {car_id} منتظر ورود به پارکینگ است...")
            semaphore.acquire()
            output_log.append(f"✅ ماشین {car_id} وارد پارکینگ شد.")
            time.sleep(0.2)  # The waiting time in parking
            output_log.append(f"⬅️ ماشین {car_id} از پارکینگ خارج شد.")
            semaphore.release()

        threads = [
            threading.Thread(target=car_enter_parking, args=(i,)) for i in range(1, 6)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

    elif scenario_id == 2:
        description = SCENARIO_DESCRIPTIONS["thread"]["semaphore"][2]
        max_connections = 2
        semaphore = threading.Semaphore(max_connections)

        def run_db_query(query_id):
            output_log.append(f"درخواست {query_id} منتظر اتصال به دیتابیس است...")
            with semaphore:
                output_log.append(
                    f"🔗 اتصال برقرار شد. در حال اجرای کوئری {query_id}..."
                )
                time.sleep(0.3)
                output_log.append(
                    f"✅ کوئری {query_id} با موفقیت اجرا شد و اتصال آزاد شد."
                )

        threads = [
            threading.Thread(target=run_db_query, args=(i,)) for i in range(1, 5)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

    elif scenario_id == 3:
        description = SCENARIO_DESCRIPTIONS["thread"]["semaphore"][3]
        max_downloads = 2
        semaphore = threading.Semaphore(max_downloads)

        def download_file(file_name):
            output_log.append(f"فایل '{file_name}' در صف دانلود قرار گرفت.")
            with semaphore:
                output_log.append(f"📥 شروع دانلود '{file_name}'...")
                time.sleep(0.2)
                output_log.append(f"✅ دانلود '{file_name}' تمام شد.")

        files = ["ویدیو.mp4", "عکس.jpg", "موزیک.mp3", "سند.pdf", "آرشیو.zip"]
        threads = [threading.Thread(target=download_file, args=(f,)) for f in files]

        for t in threads:
            t.start()
        for t in threads:
            t.join()

    else:
        description = "شماره سناریو نامعتبر است."

    return {"output": output_log, "description": description}


def run_condition_thread(scenario_id: int):
    logs = []
    desc = (
        SCENARIO_DESCRIPTIONS.get("thread", {})
        .get("condition", {})
        .get(scenario_id, "توضیحات یافت نشد.")
    )

    if scenario_id == 1:
        condition = threading.Condition()
        buffer = []

        def producer():
            with condition:
                logs.append("[تولیدکننده] در حال تولید داده...")
                time.sleep(0.2)
                buffer.append("بسته داده ۱")
                logs.append(f"[تولیدکننده] داده به بافر اضافه شد. وضعیت بافر: {buffer}")
                condition.notify()
                logs.append("[تولیدکننده] سیگنال بیدارباش (notify) ارسال شد.")

        def consumer():
            with condition:
                logs.append("[مصرف‌کننده] در حال بررسی بافر...")
                while not buffer:
                    logs.append("[مصرف‌کننده] بافر خالی است. در حال انتظار (wait)...")
                    condition.wait()
                item = buffer.pop(0)
                logs.append(f"[مصرف‌کننده] داده '{item}' مصرف شد. وضعیت بافر: {buffer}")

        t1 = threading.Thread(target=consumer)
        t2 = threading.Thread(target=producer)

        t1.start()
        time.sleep(0.1)
        t2.start()

        t1.join()
        t2.join()

    elif scenario_id == 2:
        condition = threading.Condition()
        shared_state = {"temperature": 0}

        def sensor_reader():
            for _ in range(3):
                time.sleep(0.2)
                with condition:
                    shared_state["temperature"] += 40
                    logs.append(
                        f"[سنسور] دما به {shared_state['temperature']} درجه رسید."
                    )
                    if shared_state["temperature"] >= 100:
                        logs.append(
                            "[سنسور] دما به حد بحرانی رسید! ارسال سیگنال به همه (notify_all)..."
                        )
                        condition.notify_all()
                        break

        def cooler_system(cooler_id):
            with condition:
                logs.append(
                    f"[خنک‌کننده {cooler_id}] آماده به کار. در انتظار رسیدن دما به بالای ۱۰۰..."
                )
                while shared_state["temperature"] < 100:
                    condition.wait()
                logs.append(
                    f"[خنک‌کننده {cooler_id}] سیگنال دریافت شد! شروع فرآیند خنک‌سازی..."
                )

        threads = [
            threading.Thread(target=cooler_system, args=(1,)),
            threading.Thread(target=cooler_system, args=(2,)),
            threading.Thread(target=sensor_reader),
        ]

        for t in threads:
            t.start()
        for t in threads:
            t.join()

    elif scenario_id == 3:
        condition = threading.Condition()
        turn = {"current": "A"}

        def worker_A():
            for i in range(2):
                with condition:
                    while turn["current"] != "A":
                        condition.wait()
                    logs.append(f"[نخ A] مرحله {i + 1} را انجام داد.")
                    time.sleep(0.1)
                    turn["current"] = "B"
                    logs.append("[نخ A] نوبت را به B داد و سیگنال فرستاد.")
                    condition.notify()

        def worker_B():
            for i in range(2):
                with condition:
                    while turn["current"] != "B":
                        condition.wait()
                    logs.append(f"[نخ B] مرحله {i + 1} را انجام داد.")
                    time.sleep(0.1)
                    turn["current"] = "A"
                    logs.append("[نخ B] نوبت را به A داد و سیگنال فرستاد.")
                    condition.notify()

        ta = threading.Thread(target=worker_A)
        tb = threading.Thread(target=worker_B)

        ta.start()
        tb.start()
        ta.join()
        tb.join()
        logs.append("[نخ اصلی] کار نوبتی هر دو نخ به پایان رسید.")

    else:
        logs.append("شناسه سناریو نامعتبر است.")

    return {"description": desc, "output": logs}
