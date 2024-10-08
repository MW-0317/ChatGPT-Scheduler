from typing import List, Optional, Dict

class SchedulerOutput:
    def __init__(self, process_count: int, algorithm: str, quantum: Optional[int] = None):
        self.process_count = process_count
        self.algorithm = algorithm
        self.quantum = quantum if algorithm == 'rr' else None
        self.events: Dict[int, List[str]] = {}  # Events by time tick
        self.last_time_tick: Optional[int] = None
        self.incomplete_processes: List[str] = []
        self.process_stats: Dict[str, Dict[str, int]] = {}  # Store stats for each process

    def add_event(self, time_tick: int, event: str):
        if time_tick not in self.events:
            self.events[time_tick] = []
        self.events[time_tick].append(event)

    def set_last_time_tick(self, time_tick: int):
        self.last_time_tick = time_tick

    def add_incomplete_process(self, process_name: str):
        self.incomplete_processes.append(process_name)

    def add_process_stats(self, process_name: str, wait: int, turnaround: int, response: int):
        """Add statistics for a process."""
        self.process_stats[process_name] = {
            'wait': wait,
            'turnaround': turnaround,
            'response': response
        }

    def print_output(self):
        """Print the scheduler output in the required format."""
        # Print the number of processes and algorithm used
        print(f"{self.process_count} processes")
        match self.algorithm:
            case 'rr':
              algo_description = "round-robin" 
            case 'sjf':
                algo_description = 'shortest job first'
            case 'fcfs':
                algo_description = 'first-come first-served'
            case 'lottery':
                algo_description = 'lottery'
            case 'ljf':
                algo_description = 'longest job first'
            case _:
                print(f"Unknown algorithm {self.algorithm}!")
                exit(1)

        match self.algorithm:
            case 'sjf':
                is_preemptive = "preemptive "
            case _:
                is_preemptive = ""

        print(f"Using {is_preemptive}{algo_description.title()}")

        # Print quantum if the algorithm is round robin
        if self.algorithm == 'rr':
            print(f"Quantum {self.quantum}")

        # Print events in order
        for time_tick in sorted(self.events.keys()):
            for event in sorted(self.events[time_tick], key = lambda event: 'arrived' in event, reverse = True):
                print(f"Time {time_tick:3} : {event}")

        # Print idle times if any
        if self.last_time_tick is not None:
            for time_tick in range(max(self.events.keys()) + 1, self.last_time_tick):
                print(f"Time {time_tick:3} : Idle")

        # Print the final time
        if self.last_time_tick is not None:
            print(f"Finished at time {self.last_time_tick:3}\n")

        # Print process statistics, now sorted
        for process_name, stats in sorted(self.process_stats.items(), key=lambda a: a[0]):
            print(f"{process_name} wait {stats['wait']:3} turnaround {stats['turnaround']:3} response {stats['response']}")

    def __repr__(self):
        return (f"SchedulerOutput(process_count={self.process_count}, algorithm='{self.algorithm}', "
                f"quantum={self.quantum}, events={self.events}, "
                f"last_time_tick={self.last_time_tick}, incomplete_processes={self.incomplete_processes})")
