from input import Scheduler
from output import SchedulerOutput

def fcfs_scheduler(scheduler: Scheduler) -> SchedulerOutput:
    # Initialize SchedulerOutput to keep track of events
    output = SchedulerOutput(process_count=scheduler.processcount, algorithm=scheduler.use)

    current_time = 0  # Track the current time in the system
    ready_queue = []  # Queue for ready processes
    last_event_time = 0  # Track the last event time
    index = 0  # Track process arrival

    processes = sorted(scheduler.processes, key=lambda p: p.arrival)  # Sort by arrival time for FCFS

    while current_time < scheduler.runfor or ready_queue:
        # Add processes to the ready queue if they have arrived
        while index < len(processes) and processes[index].arrival <= current_time:
            process = processes[index]
            ready_queue.append(process)
            output.add_event(process.arrival, f"{process.name} arrived")
            index += 1

        if ready_queue:
            process = ready_queue.pop(0)  # Select the first process in the queue (FCFS)

            # If current time is before process arrival, move time forward
            if current_time < process.arrival:
                current_time = process.arrival

            # Track the start time and response time for the process
            start_time = current_time
            response_time = start_time - process.arrival
            output.add_event(current_time, f"{process.name} selected (burst {process.burst})")

            # Simulate the process running
            current_time += process.burst
            turnaround_time = current_time - process.arrival
            waiting_time = start_time - process.arrival

            # Record process statistics: wait, turnaround, response
            output.add_process_stats(process.name, wait=waiting_time, turnaround=turnaround_time, response=response_time)
            output.add_event(current_time, f"{process.name} finished")

            last_event_time = current_time  # Update last event time
        else:
            # If no process is ready, the system is idle
            output.add_event(current_time, "Idle")
            current_time += 1

    # Once finished, record the last time tick and the end event
    output.set_last_time_tick(current_time)
    
    return output