from input import Scheduler
from output import SchedulerOutput
from collections import deque

def round_robin_scheduler(scheduler: Scheduler) -> SchedulerOutput:
    # Initialize SchedulerOutput
    output = SchedulerOutput(process_count=scheduler.processcount, algorithm='rr', quantum=scheduler.quantum)
    
    # Sort processes by arrival time
    processes = sorted(scheduler.processes, key=lambda p: p.arrival)
    
    # Use a queue to manage the ready processes
    ready_queue = deque()
    time = 0  # Global time tracker
    process_dict = {p.name: {'remaining_time': p.burst, 'start_time': None, 'response_recorded': False} for p in processes}
    completed_processes = set()
    
    # Function to check if all processes are completed
    def all_processes_completed():
        return all(process_dict[p.name]['remaining_time'] == 0 for p in processes)
    
    # Add processes that have arrived to the ready queue
    def add_arrived_processes(exclude_process=None):
        for p in processes:
            if p.arrival <= time and p.name not in completed_processes and p not in ready_queue:
                if exclude_process is None or p.name != exclude_process.name:
                    output.add_event(time, f"{p.name} arrived")
                    ready_queue.append(p)

    # Keep running until all processes are completed or time exceeds runfor
    while time < scheduler.runfor:
        add_arrived_processes()

        if ready_queue:
            # Get the next process in the queue
            current_process = ready_queue.popleft()
            output.add_event(time, f"{current_process.name} selected (burst {process_dict[current_process.name]['remaining_time']})")
            

            # Record response time if it's the first time the process is running
            if not process_dict[current_process.name]['response_recorded']:
                process_dict[current_process.name]['response_recorded'] = True
                process_dict[current_process.name]['start_time'] = time

            # Run the process for the quantum or until completion
            execution_time = min(scheduler.quantum, process_dict[current_process.name]['remaining_time'])
            process_dict[current_process.name]['remaining_time'] -= execution_time
            # for t in range(time, time + execution_time):
            #     output.add_event(t, f"{current_process.name} running")

            time += execution_time

            # After the process runs, check for new arrivals
            add_arrived_processes(exclude_process=current_process)

            # Check if the process is completed
            if process_dict[current_process.name]['remaining_time'] == 0:
                completed_processes.add(current_process.name)
                turnaround_time = time - current_process.arrival
                wait_time = turnaround_time - current_process.burst
                response_time = process_dict[current_process.name]['start_time'] - current_process.arrival  # Correct response time
                output.add_process_stats(current_process.name, wait=wait_time, turnaround=turnaround_time, response=response_time)
                output.add_event(time, f"{current_process.name} finished")
            else:
                # Re-add the process to the queue if it's not finished
                ready_queue.append(current_process)
        else:
            # If no process is ready, the CPU is idle
            output.add_event(time, "Idle")
            time += 1

        add_arrived_processes()

    output.set_last_time_tick(time)
    
    return output
