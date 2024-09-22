from input import Scheduler
from output import SchedulerOutput

def ljf_scheduler(scheduler: Scheduler) -> SchedulerOutput:
    # Initialize SchedulerOutput to track events
    output = SchedulerOutput(process_count=scheduler.processcount, algorithm="ljf")
    
    current_time = 0  # Track the current time
    ready_queue = []  # Queue for processes ready to run
    index = 0  # Index to track arriving processes
    last_event_time = -1  # Track the last event time
    
    # Sort processes by arrival time initially
    processes = sorted(scheduler.processes, key=lambda p: p.arrival)

    # Run until the scheduler run time or all processes have completed
    while current_time < scheduler.runfor or ready_queue:
        # Add processes to the ready queue if they have arrived
        while index < len(processes) and processes[index].arrival <= current_time:
            process = processes[index]
            ready_queue.append(process)
            output.add_event(process.arrival, f"{process.name} arrived")
            index += 1

        if ready_queue:
            # Select the process with the longest burst time (LJF)
            process = max(ready_queue, key=lambda p: p.burst)
            ready_queue.remove(process)

            # Track the start time and response time
            start_time = current_time
            response_time = start_time - process.arrival
            output.add_event(current_time, f"{process.name} selected (burst {process.burst})")
            
            # Run the process for its burst time
            current_time += process.burst
            turnaround_time = current_time - process.arrival
            waiting_time = start_time - process.arrival

            # Record process statistics: wait, turnaround, response
            output.add_process_stats(process.name, wait=waiting_time, turnaround=turnaround_time, response=response_time)
            output.add_event(current_time, f"{process.name} finished")

            # Update the last event time
            last_event_time = current_time
        else:
            # If no process is ready, system is idle
            output.add_event(current_time, "Idle")
            last_event_time = current_time
            current_time += 1

    # Once finished, record the final time
    output.set_last_time_tick(current_time)

    return output