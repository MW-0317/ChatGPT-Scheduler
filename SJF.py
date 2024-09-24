from input import Scheduler
from output import SchedulerOutput

def sjf_scheduler(scheduler: Scheduler) -> SchedulerOutput:
    output = SchedulerOutput(process_count=scheduler.processcount, algorithm=scheduler.use)
    current_time = 0
    ready_queue = []
    index = 0
    processes = sorted(scheduler.processes, key=lambda p: p.arrival)

    finished = False
    while current_time < scheduler.runfor:
        while index < len(processes) and processes[index].arrival <= current_time:
            process = processes[index]
            ready_queue.append(process)
            output.add_event(process.arrival, f"{process.name} arrived")
            index += 1

        ready_queue = sorted(ready_queue, key=lambda p: p.remaining_time)

        if ready_queue:
            process = ready_queue[0]
            if (process.start_time is None) or finished:
                if process.start_time is None:
                    process.start_time = current_time
                    process.response_time = current_time - process.arrival
                output.add_event(current_time, f"{process.name} selected (burst {process.remaining_time})")
            
            if finished:
                finished = False

            process.remaining_time -= 1
            current_time += 1

            if process.remaining_time == 0:
                turnaround_time = current_time - process.arrival
                waiting_time = turnaround_time - process.burst
                output.add_process_stats(process.name, wait=waiting_time, turnaround=turnaround_time, response=process.response_time)
                output.add_event(current_time, f"{process.name} finished")
                ready_queue.pop(0)
                finished = True
        else:
            output.add_event(current_time, "Idle")
            current_time += 1

    output.set_last_time_tick(current_time)
    return output
