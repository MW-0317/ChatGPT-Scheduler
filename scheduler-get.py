import argparse
from input import parse_scheduler_file
from output import SchedulerOutput

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

output = SchedulerOutput(len(scheduler.processes), scheduler.use, scheduler.quantum)
output.add_event(0, "A arrived")
output.add_event(2, "B arrived")
output.add_event(3, "A finished")
output.add_process_stats("A", 1, 13, 1)
output.set_last_time_tick(20)
output.print_output()