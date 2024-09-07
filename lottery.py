import random
from typing import List, Dict, Optional
from input import Scheduler
from output import SchedulerOutput

def lottery_scheduler(scheduler: Scheduler) -> SchedulerOutput:
    # Initialize SchedulerOutput with the given algorithm as 'lottery'
    output = SchedulerOutput(
        process_count=scheduler.processcount,
        algorithm='lottery'
    )
    
    # Initialize a list of processes and their states
    processes = scheduler.processes
    current_time = 0
    process_queue = [process for process in processes if process.arrival <= current_time]
    remaining_burst = {process.name: process.burst for process in processes}
    process_tickets = {process.name: 1 for process in processes}  # Initial tickets count (1 per process)
    completed_processes = set()
    first_run_time = {process.name: None for process in processes}  # Track first run time
    
    while current_time < scheduler.runfor and len(completed_processes) < scheduler.processcount:
        # Update the queue with newly arrived processes
        for process in processes:
            if process.arrival <= current_time and process.name not in process_queue:
                process_queue.append(process)
        
        # Filter out completed processes from the queue
        process_queue = [process for process in process_queue if process.name not in completed_processes]
        
        # If no process is in the queue, time passes until the next arrival
        if not process_queue:
            current_time += 1
            continue
        
        # Allocate lottery tickets and select a winner
        total_tickets = sum(process_tickets[process.name] for process in process_queue)
        winning_ticket = random.randint(1, total_tickets)
        
        # Determine which process won the lottery
        ticket_sum = 0
        selected_process = None
        for process in process_queue:
            ticket_sum += process_tickets[process.name]
            if ticket_sum >= winning_ticket:
                selected_process = process
                break
        
        # Track the first run time for response time calculation
        if first_run_time[selected_process.name] is None:
            first_run_time[selected_process.name] = current_time
        
        # Simulate the execution of the selected process for one time tick
        output.add_event(current_time, f"Process {selected_process.name} selected (Lottery)")
        remaining_burst[selected_process.name] -= 1
        
        # If the process completes its execution
        if remaining_burst[selected_process.name] == 0:
            completed_processes.add(selected_process.name)
            process_queue.remove(selected_process)
            finish_time = current_time + 1
            turnaround_time = finish_time - selected_process.arrival
            wait_time = turnaround_time - selected_process.burst  # Recalculate wait time
            response_time = first_run_time[selected_process.name] - selected_process.arrival
            output.add_process_stats(selected_process.name, wait_time, turnaround_time, response_time)
            output.add_event(current_time + 1, f"Process {selected_process.name} completes")
        
        # Update the process list and time
        current_time += 1

    # Set the last time tick to the current time after all processes are scheduled
    output.set_last_time_tick(current_time)
    
    # Check for incomplete processes and log them
    for process in processes:
        if process.name not in completed_processes:
            output.add_incomplete_process(process.name)
    
    return output