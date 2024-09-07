from output import SchedulerOutput

def print_scheduler_output(output: SchedulerOutput):
    print("=" * 40)
    print(f"{'Scheduling Report':^40}")
    print("=" * 40)
    print(f"Processes: {output.process_count}")
    print(f"Scheduling Method: {output.algorithm}")
    
    if output.quantum:
        print(f"Quantum: {output.quantum}")
    
    print("\n" + "=" * 40)
    print(f"{'Event Log':^40}")
    print("=" * 40)
    
    # Printing events by time tick
    for time_tick in sorted(output.events.keys()):
        events = output.events[time_tick]
        for event in events:
            print(f"Time {time_tick:<2}: {event}")
    
    print("=" * 40)
    
    # Printing incomplete processes, if any
    if output.incomplete_processes:
        print(f"{'Incomplete Processes':^40}")
        print("=" * 40)
        for process in output.incomplete_processes:
            print(f"{process}")
        print("=" * 40)
    
    # Printing last time tick
    if output.last_time_tick is not None:
        print(f"Finished at time {output.last_time_tick}\n")
    
    print(f"{'Performance Metrics':^40}")
    print("=" * 40)
    
    # Printing process statistics
    for process, stats in output.process_stats.items():
        print(f"Process {process}:")
        print(f"  Wait: {stats['wait']}  Turnaround: {stats['turnaround']}  Response: {stats['response']}")
    
    print("=" * 40)