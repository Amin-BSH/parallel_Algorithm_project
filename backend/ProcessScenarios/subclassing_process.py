import multiprocessing
import time

from backend.descriptions import SCENARIO_DESCRIPTIONS


class BasicWorker(multiprocessing.Process):
    """سناریو ۱: یک کلاس ساده که فرآیند را ارث‌بری می‌کند"""

    def __init__(self, worker_name, shared_logs):
        super().__init__()
        self.worker_name = worker_name
        self.shared_logs = shared_logs

    def run(self):
        self.shared_logs.append(
            f"👷 [کارگر پایه] فرآیند '{self.worker_name}' در حال اجراست. PID: {self.pid}"
        )
        time.sleep(0.5)
        self.shared_logs.append(
            f"✅ [کارگر پایه] کار '{self.worker_name}' به پایان رسید."
        )


class MathWorker(multiprocessing.Process):
    """سناریو ۲: کلاسی که علاوه بر اجرای فرآیند، محاسبات انجام داده و وضعیت را نگه می‌دارد"""

    def __init__(self, number, shared_logs):
        super().__init__()
        self.number = number
        self.shared_logs = shared_logs

    def run(self):
        self.shared_logs.append(
            f"🧮 [کارگر محاسباتی] دریافت عدد {self.number} برای محاسبه مربع آن..."
        )
        time.sleep(0.5)
        result = self.number**2
        self.shared_logs.append(
            f"📊 [کارگر محاسباتی] نتیجه: مربع عدد {self.number} برابر است با {result}"
        )


class ModularWorker(multiprocessing.Process):
    """سناریو ۳: کلاسی با ساختار ماژولار که متدهای داخلی مختلفی دارد"""

    def __init__(self, task_name, shared_logs):
        super().__init__(name=f"Modular-{task_name}")
        self.task_name = task_name
        self.shared_logs = shared_logs

    def _setup(self):
        self.shared_logs.append(
            f"⚙️ [کارگر ماژولار - {self.name}] در حال آماده‌سازی منابع..."
        )
        time.sleep(0.2)

    def _execute(self):
        self.shared_logs.append(
            f"🚀 [کارگر ماژولار - {self.name}] در حال اجرای منطق اصلی..."
        )
        time.sleep(0.3)

    def _cleanup(self):
        self.shared_logs.append(
            f"🧹 [کارگر ماژولار - {self.name}] در حال پاک‌سازی و خروج..."
        )

    def run(self):
        self._setup()
        self._execute()
        self._cleanup()


def run_subclassing_process(scenario_id):
    manager = multiprocessing.Manager()
    logs = manager.list()

    desc = (
        SCENARIO_DESCRIPTIONS.get("process", {})
        .get("subclassing_process", {})
        .get(scenario_id, "توضیحات یافت نشد.")
    )

    if scenario_id == 1:
        logs.append("▶️ ساخت شیء از کلاس BasicWorker...")
        worker = BasicWorker("آلفا", logs)

        worker.start()
        worker.join()
        logs.append("🏁 سناریوی ارث‌بری پایه تمام شد.")

    elif scenario_id == 2:
        logs.append("▶️ ایجاد دو فرآیند محاسباتی...")
        worker1 = MathWorker(5, logs)
        worker2 = MathWorker(8, logs)

        worker1.start()
        worker2.start()

        worker1.join()
        worker2.join()
        logs.append("🏁 محاسبات توسط کلاس‌های فرآیندی به اتمام رسید.")

    elif scenario_id == 3:
        logs.append("▶️ شروع فرآیند ماژولار...")
        worker = ModularWorker("پردازش_تصویر", logs)

        worker.start()
        worker.join()
        logs.append("🏁 فرآیند ماژولار با موفقیت تمام متدهای داخلی خود را اجرا کرد.")

    else:
        logs.append("شماره سناریو نامعتبر است.")

    return {"description": desc, "output": list(logs)}
