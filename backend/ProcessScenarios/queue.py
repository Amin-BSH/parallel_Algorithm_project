import multiprocessing
import random
import time

from backend.descriptions import SCENARIO_DESCRIPTIONS


class Producer(multiprocessing.Process):
    def __init__(self, queue, shared_logs):
        multiprocessing.Process.__init__(self)
        self.queue = queue
        self.shared_logs = shared_logs

    def run(self):
        for i in range(5):
            item = random.randint(0, 256)
            self.queue.put(item)
            self.shared_logs.append(
                f"📦 [Producer] item {item} appended to queue by {self.name}"
            )
            time.sleep(0.1)

        try:
            self.shared_logs.append(f"📊 The size of queue is {self.queue.qsize()}")
        except NotImplementedError:
            self.shared_logs.append("📊 [qsize() is not supported on this OS]")


class Consumer(multiprocessing.Process):
    def __init__(self, queue, shared_logs):
        multiprocessing.Process.__init__(self)
        self.queue = queue
        self.shared_logs = shared_logs

    def run(self):
        time.sleep(0.2)
        while True:
            if self.queue.empty():
                self.shared_logs.append("🛑 the queue is empty. Consumer stopping.")
                break
            else:
                time.sleep(0.1)
                item = self.queue.get()
                self.shared_logs.append(
                    f"🛒 [Consumer] item {item} popped by {self.name}"
                )


def worker_task(task_queue, result_queue, worker_name, shared_logs):
    while True:
        task = task_queue.get()
        if task is None:
            break
        shared_logs.append(f"⚙️ [کارگر {worker_name}] پردازش عدد {task}...")
        result_queue.put((task, task**2))
        time.sleep(0.1)


def run_using_a_queue(scenario_id):
    manager = multiprocessing.Manager()
    logs = manager.list()

    desc = (
        SCENARIO_DESCRIPTIONS.get("process", {})
        .get("using_a_queue", {})
        .get(scenario_id, "توضیحات یافت نشد.")
    )

    if scenario_id == 1:
        logs.append("▶️ شروع سناریو ۱: تبادل داده شی‌گرا با Queue...")
        q = multiprocessing.Queue()

        process_producer = Producer(q, logs)
        process_consumer = Consumer(q, logs)

        process_producer.start()
        process_consumer.start()

        process_producer.join()
        process_consumer.join()
        logs.append("🏁 تبادل داده بین Producer و Consumer به پایان رسید.")

    elif scenario_id == 2:
        logs.append("▶️ شروع سناریو ۲: توزیع وظایف بین دو کارگر...")
        task_queue = multiprocessing.Queue()
        result_queue = multiprocessing.Queue()

        w1 = multiprocessing.Process(
            target=worker_task, args=(task_queue, result_queue, "A", logs)
        )
        w2 = multiprocessing.Process(
            target=worker_task, args=(task_queue, result_queue, "B", logs)
        )

        for i in range(1, 4):
            task_queue.put(i)

        w1.start()
        w2.start()

        task_queue.put(None)
        task_queue.put(None)

        w1.join()
        w2.join()
        logs.append("🏁 تمام وظایف از صف برداشته شدند.")

    elif scenario_id == 3:
        logs.append("▶️ شروع سناریو ۳: ارتباط دوطرفه با دو Queue...")
        q_tasks = multiprocessing.Queue()
        q_results = multiprocessing.Queue()

        worker = multiprocessing.Process(
            target=worker_task, args=(q_tasks, q_results, "محاسب", logs)
        )

        numbers = [10, 20]
        for num in numbers:
            q_tasks.put(num)

        worker.start()

        q_tasks.put(None)

        for _ in range(len(numbers)):
            orig, squared = q_results.get()
            logs.append(f"✅ [فرآیند اصلی] نتیجه دریافت شد: {orig}^2 = {squared}")

        worker.join()
        logs.append("🏁 ارتباط دوطرفه با موفقیت انجام شد.")

    else:
        logs.append("شماره سناریو نامعتبر است.")

    return {"description": desc, "output": list(logs)}
