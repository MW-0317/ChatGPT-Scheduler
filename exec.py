import argparse
import os
import sys
from input import parse_scheduler_file
from output import SchedulerOutput
from rendering import print_scheduler_output
from lottery import lottery_scheduler
from roundrobin import round_robin_scheduler
from FCFS import fcfs_scheduler

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

def write_scheduler_output_to_file(scheduler_output: SchedulerOutput, file_path: str):
    """
    Write the SchedulerOutput details to a specified file by redirecting print_output method output to a file.

    :param scheduler_output: The SchedulerOutput object to be written to the file.
    :param file_path: The path to the file where the output should be written.
    """
    # Redirect standard output to a file
    with open(file_path, 'w') as file:
        # Save the original stdout
        original_stdout = sys.stdout
        sys.stdout = file
        
        # Call the print_output method to write to the file
        scheduler_output.print_output()
        
        # Restore the original stdout
        sys.stdout = original_stdout

def remove_file_extension(file_path: str) -> str:
    """
    Remove the file extension from a file path, if present.

    :param file_path: The path of the file from which the extension should be removed.
    :return: The file path without the extension.
    """
    # Split the file path into root and extension
    root, _ = os.path.splitext(file_path)
    return root
    
file = get_file_from_command_line()

scheduler = parse_scheduler_file(file)

match scheduler.use:
    case 'fcfs':
        output = fcfs_scheduler(scheduler)
    case 'rr':
        output = round_robin_scheduler(scheduler)
    case 'lottery':
        output = lottery_scheduler(scheduler)
    case _:
        print("Unknown algorithm!")
        exit(1)

destination = remove_file_extension(file) + ".out.test"
write_scheduler_output_to_file(output, destination)

print_scheduler_output(output)