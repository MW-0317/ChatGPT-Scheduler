from input import Scheduler
from output import SchedulerOutput

# Longest Job First Algorithm
# ljf_scheduler.py

class Process:
    def __init__(self, name, arrival, burst):
        self.name = name
        self.arrival = arrival
        self.burst = burst
        self.waiting_time = 0
        self.turnaround_time = 0
        self.response_time = -1  # To indicate it hasn't started yet
        self.start_time = None

def ljf_scheduler(processes, run_for):
    # Sort processes by their arrival time
    processes.sort(key=lambda p: p.arrival)
    
    current_time = 0
    output_log = []
    ready_queue = []
    index = 0
    last_event_time = -1  # Keep track of the time when the last event occurred

    while current_time < run_for:
        # Add processes to the ready queue if they have arrived
        while index < len(processes) and processes[index].arrival <= current_time:
            process = processes[index]
            ready_queue.append(process)
            output_log.append(f"Time {process.arrival:3} : {process.name} arrived")
            index += 1

        if ready_queue:
            # Select the process with the longest burst time
            process = max(ready_queue, key=lambda p: p.burst)
            ready_queue.remove(process)
            
            # If the CPU was idle, log the idle time
            if last_event_time != current_time:
                output_log.append(f"Time {current_time:3} : {process.name} selected (burst {process.burst:3})")
            else:
                output_log.append(f"Time {current_time:3} : {process.name} selected (burst {process.burst:3})")
            
            process.start_time = current_time
            if process.response_time == -1:
                process.response_time = current_time - process.arrival
            
            # Run the process
            current_time += process.burst
            process.turnaround_time = current_time - process.arrival
            process.waiting_time = process.start_time - process.arrival

            output_log.append(f"Time {current_time:3} : {process.name} finished")
            last_event_time = current_time  # Update the time of the last event
        else:
            if last_event_time != current_time:
                output_log.append(f"Time {current_time:3} : Idle")
                last_event_time = current_time
            current_time += 1

    output_log.append(f"Finished at time {run_for}")
    return output_log

def calculate_metrics(processes):
    # Generate metrics log based on the alphabetical order of process names
    metrics_log = []
    for process in sorted(processes, key=lambda p: p.name):
        metrics_log.append(f"{process.name} wait {process.waiting_time:3} "
                           f"turnaround {process.turnaround_time:3} "
                           f"response {process.response_time:3}")
    return metrics_log

def read_input_file(file_path):
    processes = []
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            process_count = int(lines[0].split()[1])
            run_for = int(lines[1].split()[1])
            algorithm = lines[2].split()[1].lower()

            for line in lines[3:]:
                if line.startswith("process name"):
                    parts = line.split()
                    name = parts[2]
                    arrival = int(parts[4])
                    burst = int(parts[6])
                    processes.append(Process(name, arrival, burst))
                elif line.strip() == "end":
                    break
    except Exception as e:
        print(f"Error: {e}")

    return processes, run_for, algorithm, process_count

def print_output(output_log, metrics_log, process_count, algorithm):
    # Print number of processes and algorithm used
    print(f"{process_count} processes")
    if algorithm == 'ljf':
        print(f"Using Longest Job First\n")
    else:
        print(f"Using First-Come First-Served\n")

    # Print the scheduling logs
    for line in output_log:
        print(line)
    print()

    # Print the metrics logs in the correct order
    for line in metrics_log:
        print(line)

# Specify the input file path
input_file_path = 'ljf_input.txt'

# Read data from input file
processes, run_for, algorithm, process_count = read_input_file(input_file_path)

# Run LJF scheduler and generate output logs
if processes and algorithm == 'ljf':
    output_log = ljf_scheduler(processes, run_for)
    metrics_log = calculate_metrics(processes)
    print_output(output_log, metrics_log, process_count, algorithm)
else:
    print("Unsupported scheduling algorithm or no processes to schedule.")
