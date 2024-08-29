import argparse
import os
import sys
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

output = SchedulerOutput(len(scheduler.processes), scheduler.use, scheduler.quantum)
output.add_event(0, "A arrived")
output.add_event(2, "B arrived")
output.add_event(3, "A finished")
output.add_process_stats("A", 1, 13, 1)
output.set_last_time_tick(20)

write_scheduler_output_to_file(output, remove_file_extension(file) + ".out")