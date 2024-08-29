import argparse
from typing import List, Optional

class Process:
    def __init__(self, name: str, arrival: int, burst: int):
        """
        Initialize a Process with a name, arrival time, and burst time.
        
        :param name: The name of the process.
        :param arrival: The arrival time of the process.
        :param burst: The total burst time of the process.
        """
        self.name = name
        self.arrival = arrival
        self.burst = burst

    def __repr__(self):
        """
        Provide a string representation of the Process for easy debugging and display.
        
        :return: A string representing the Process.
        """
        return f"Process(name='{self.name}', arrival={self.arrival}, burst={self.burst})"

class Scheduler:
    def __init__(self, processcount: int, runfor: int, use: str, quantum: Optional[int] = None, end: str = "EOF"):
        """
        Initialize the Scheduler with given parameters.

        :param processcount: Number of processes in the list.
        :param runfor: Total number of time ticks to run.
        :param use: Scheduling algorithm to use ('fcfs', 'sjf', 'rr').
        :param quantum: Time quantum for round-robin scheduling (required if 'use' is 'rr').
        :param end: End-of-file marker.
        """
        self.processcount = processcount
        self.runfor = runfor
        self.use = use
        self.quantum = quantum
        self.processes: List[Process] = []
        self.end = end

        # Validation for the algorithm type and quantum requirement
        if self.use not in ['fcfs', 'sjf', 'rr']:
            raise ValueError("Invalid algorithm specified. Valid values: 'fcfs', 'sjf', 'rr'")

        if self.use == 'rr' and self.quantum is None:
            raise ValueError("Quantum must be specified for round-robin (rr) scheduling.")

    def add_process(self, process: Process):
        """
        Add a process to the list of processes.
        
        :param process: The Process object to be added.
        """
        self.processes.append(process)

    def __repr__(self):
        """
        Provide a string representation of the Scheduler for easy debugging and display.
        
        :return: A string representing the Scheduler.
        """
        return (f"Scheduler(processcount={self.processcount}, runfor={self.runfor}, "
                f"use='{self.use}', quantum={self.quantum}, processes={self.processes}, end='{self.end}')")

def parse_scheduler_file(file_path: str) -> Scheduler:
    """
    Parses a file to create a Scheduler object with its processes.

    :param file_path: Path to the input file.
    :return: A Scheduler object populated with data from the file.
    """
    scheduler = None
    processes = []
    quantum = None

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('processcount'):
                processcount = int(line.split()[1])
            elif line.startswith('runfor'):
                runfor = int(line.split()[1])
            elif line.startswith('use'):
                use = line.split()[1]
            elif line.startswith('quantum'):
                quantum = int(line.split()[1])
            elif line.startswith('process name'):
                # Extract process details
                parts = line.split()
                name = parts[2]
                arrival = int(parts[4])
                burst = int(parts[6])
                # Create and store the process
                processes.append(Process(name=name, arrival=arrival, burst=burst))
            elif line.startswith('end'):
                end = 'EOF'
                # Create the Scheduler object when "end" is encountered
                scheduler = Scheduler(processcount=processcount, runfor=runfor, use=use, quantum=quantum)
                # Add all the processes to the Scheduler
                for process in processes:
                    scheduler.add_process(process)
                scheduler.end = end
                break

    return scheduler

def get_file_from_command_line() -> str:
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description="Process a file path from the command line.")

    # Add an argument for the file path
    parser.add_argument('file', type=str, help="Path to the file")

    # Parse the arguments from the command line
    args = parser.parse_args()

    # Get the file path from the parsed arguments
    file_path = args.file
    return file_path
    
file = get_file_from_command_line()

scheduler = parse_scheduler_file(file)

print(scheduler)