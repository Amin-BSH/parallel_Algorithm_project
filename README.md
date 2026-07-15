# Parallel Processing Project

A Python-based learning project demonstrating parallelism with threads and processes.

The project includes:

- A FastAPI backend (`backend/main.py`) exposing a `/run-scenario` endpoint.
- A Streamlit frontend (`frontend/app.py`) for selecting and running thread/process scenarios.
- Example thread scenarios in `backend/threads_scenarios.py`.
- Example process scenarios in `backend/ProcessScenarios/`.
- Scenario descriptions in `backend/descriptions.py`.

## What it does

This project is a university homework assignment for learning Python parallelism. It includes two layers:

- A FastAPI backend that executes concurrency scenarios.
- A Streamlit frontend that lets the student choose a concurrency tool and a scenario.

### Threading tools

- `basic_thread`: demonstrates basic thread creation and execution with examples such as parallel email sending, chunked downloads, and sensor reading.
- `determining_current_thread`: shows how to inspect the current thread identity, assign meaningful thread names, and branch behavior based on thread name.
- `subclass`: uses custom `Thread` subclasses to encapsulate thread behavior, store results on the thread object, and share data between threads.
- `lock`: shows how `threading.Lock` prevents race conditions when multiple threads update shared state like ticket reservations, bank balances, or request counters.
- `rlock`: demonstrates `threading.RLock` for reentrant locking, allowing the same thread to acquire the lock multiple times safely in nested or recursive code.
- `semaphore`: simulates limited resources using `threading.Semaphore`, such as parking slot management, database connection pools, or limited parallel downloads.
- `condition`: implements coordinated workflows using `threading.Condition` and `wait/notify`, including producer-consumer, multi-waiter notifications, and turn-based execution.
- `event`: uses `threading.Event` to signal one or more threads, including start signals, synchronized release of workers, and polling for completion.
- `barrier`: coordinates groups of threads with `threading.Barrier`, demonstrating simultaneous start points and multi-phase synchronization.
- `queue`: uses `queue.Queue` for safe thread communication in producer-consumer patterns and shared task processing.

### Process tools

- `spawning_a_process`: creates separate OS processes with `multiprocessing.Process`, demonstrating simple spawn, concurrent workers, and a custom process subclass.
- `naming_a_process`: shows how to assign readable process names, rename an existing process object, and use subclassing to keep named process definitions.
- `running_a_process_in_background`: explains daemon processes, how they differ from foreground processes, and why daemon processes cannot create child processes.
- `killing_a_process`: demonstrates process termination methods such as `terminate()`, `kill()`, and `close()` to manage long-running or unwanted processes.
- `subclassing_process`: uses `multiprocessing.Process` subclasses to encapsulate process logic, state, and behavior in object-oriented form.
- `queue`: shows safe process communication with `multiprocessing.Queue`, including producer-consumer patterns, task/result queues, and multi-process coordination.
- `synchronizing_processes`: illustrates process synchronization with `multiprocessing.Lock`, `multiprocessing.Semaphore`, and `multiprocessing.Barrier` for safe shared-resource access.
- `using_a_process_pool`: uses a process pool to distribute work across a fixed number of worker processes, making CPU-bound parallelism easier to manage.

The frontend sends JSON requests to the backend, which executes the selected scenario and returns descriptive output.

## Requirements

The project currently depends on:

- `fastapi==0.124.0`
- `uvicorn==0.38.0`
- `streamlit==1.52.2`
- `requests==2.31.0`

Install them with:

```bash
pip install -r requirements.txt
```

## Running locally

### Start the backend

From the project root:

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### Start the frontend

In a new terminal:

```bash
streamlit run frontend/app.py --server.port 8501 --server.address 0.0.0.0
```

Then open `http://localhost:8501` in your browser.

## API endpoint

The backend provides a single endpoint:

- `POST /run-scenario`

Example request payload:

```json
{
  "method": "thread",
  "tool": "basic_thread",
  "scenario_id": 1
}
```

Example `curl` command:

```bash
curl -X POST http://localhost:8000/run-scenario \
  -H "Content-Type: application/json" \
  -d '{"method":"thread","tool":"basic_thread","scenario_id":1}'
```

## Environment variables

The project supports configuring a few runtime values via environment variables. Create a `.env` file in the project root or export variables in your environment. A sample file is provided at [.env.example](.env.example).

- **BACKEND_URL**: URL the frontend should use to contact the backend (default: `http://localhost:8000`).

To use the example file, copy it to `.env` and edit values as needed:

```bash
cp .env.example .env
```

## Docker support

A `Dockerfile` is included to run both the backend and frontend together in one container.

Build the image:

```bash
docker build -t parallel-algo-project .
```

Run the container:

```bash
docker run --rm -p 8000:8000 -p 8501:8501 parallel-algo-project
```

Then open `http://localhost:8501`.

## Project structure

```
backend/
  main.py
  descriptions.py
  threads_scenarios.py
  ProcessScenarios/
    spawning_a_process.py
    naming_a_process.py
    background_process.py
    killing_a_process.py
    subclassing_process.py
    queue.py
    synchronizing_processes.py
    process_pool.py
frontend/
  app.py
  fonts/
    Vazir-Thin.ttf
requirements.txt
Dockerfile
```

## Notes

- The Streamlit UI is Persian-language oriented and interacts with the FastAPI server at `http://localhost:8000`.
- If you use Docker, both the backend and frontend ports are exposed by default: `8000` and `8501`.
