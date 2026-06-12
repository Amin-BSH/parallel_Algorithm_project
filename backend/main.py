from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from backend.threads_scenarios import (
    run_basic_thread,
    run_determining_current_thread,
    run_thread_subclass,
    run_lock_thread,
    run_rlock_thread,
    run_semaphore_thread,
    run_condition_thread,
    run_event_thread,
    run_barrier_thread,
    run_queue_thread,
)

from backend.ProcessScenarios.spawning_a_process import run_spawning_process
from backend.ProcessScenarios.naming_a_process import run_naming_process

app = FastAPI(title="Parallel Processing Project API")


class ScenarioRequest(BaseModel):
    method: str  # 'thread' or 'process'
    tool: str  # e.g., 'basic_thread'
    scenario_id: int  # 1, 2, or 3


@app.post("/run-scenario")
def execute_scenario(request: ScenarioRequest):
    if request.method == "thread":
        if request.tool == "basic_thread":
            result = run_basic_thread(request.scenario_id)
            return result
        elif request.tool == "determining_current_thread":
            result = run_determining_current_thread(request.scenario_id)
            return result
        elif request.tool == "subclass":
            result = run_thread_subclass(request.scenario_id)
            return result
        elif request.tool == "lock":
            result = run_lock_thread(request.scenario_id)
            return result
        elif request.tool == "rlock":
            result = run_rlock_thread(request.scenario_id)
            return result
        elif request.tool == "semaphore":
            result = run_semaphore_thread(request.scenario_id)
            return result
        elif request.tool == "condition":
            result = run_condition_thread(request.scenario_id)
            return result
        elif request.tool == "event":
            result = run_event_thread(request.scenario_id)
            return result
        elif request.tool == "barrier":
            result = run_barrier_thread(request.scenario_id)
            return result
        elif request.tool == "queue":
            result = run_queue_thread(request.scenario_id)
            return result
        else:
            raise HTTPException(status_code=404, detail="ابزار Thread یافت نشد.")

    elif request.method == "process":
        if request.tool == "spawning_a_process":
            result = run_spawning_process(request.scenario_id)
            return result
        elif request.tool == "naming_a_process":
            result = run_naming_process(request.scenario_id)
            return result
        else:
            raise HTTPException(status_code=404, detail="ابزار Process یافت نشد.")

    raise HTTPException(status_code=400, detail="متد انتخابی نامعتبر است.")
