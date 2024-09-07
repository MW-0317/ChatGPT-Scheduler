def print_formatted_output(data):
    lines = data.strip().split('\n')
    
    # Extract basic information
    num_processes = lines[0].split()[0] + " processes"
    scheduling_method = lines[1]
    quantum_info = lines[2]
    
    # Print header information
    print(f"{'=' * 40}")
    print(f"{'Scheduling Report':^40}")
    print(f"{'=' * 40}\n")
    print(f"Processes: {num_processes}")
    print(f"Scheduling Method: {scheduling_method}")
    print(f"{quantum_info}\n")
    
    # Separate the process and time-related information
    print(f"{'Time Log':^40}")
    print(f"{'-' * 40}")
    
    time_logs = [line for line in lines[3:] if line.startswith("Time")]
    for log in time_logs:
        print(f"{log}")
    
    print(f"{'-' * 40}\n")
    
    # Separate finished information
    finished_line = next(line for line in lines if line.startswith("Finished"))
    print(f"{'Summary':^40}")
    print(f"{'-' * 40}")
    print(f"{finished_line}\n")
    
    # Separate waiting, turnaround, and response information
    print(f"{'Performance Metrics':^40}")
    print(f"{'-' * 40}")
    performance_lines = [line for line in lines if any(word in line for word in ["wait", "turnaround", "response"])]
    for metric in performance_lines:
        print(f"{metric}")

    print(f"{'=' * 40}")