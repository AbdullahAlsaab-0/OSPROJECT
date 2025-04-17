from typing import Any


def read_input_processes(priority:bool=False, interval:bool=False) -> tuple[list[dict], int]:

    try:
        num_processes = int(input("How many processes are there? "))
        if num_processes <= 0:
            raise ValueError()
    except ValueError:
        raise ValueError("Please enter a positive integer.\n")

    arrival_time = input("Enter the arrival time of each process separated by spaces.\n").split()
    burst_time = input("Enter the burst time of each process separated by spaces.\n").split()


    if len(arrival_time) != num_processes or len(burst_time) != num_processes:
        raise ValueError(f"Expected {num_processes} values for each attribute, but got {len(arrival_time)} arrival times and {len(burst_time)} burst times\n")

    try:
        processes = [{"id": f"P{idx + 1}", "arrival": int(x[0]), "burst": int(x[1])}
                                 for idx, x in enumerate(zip(arrival_time, burst_time))]
    except ValueError:
        raise ValueError("non integer arrival time or burst time\n")

    validate_times(processes)

    if priority:
        priorities = read_int_list("priority", num_processes)
        for idx, process in enumerate(processes):
            process["priority"] = priorities[idx]

    if interval:
        intervals = read_int_list("interval", num_processes)
        for idx, process in enumerate(processes):
            process["interval"] = intervals[idx]

    processes = sorted(processes, key=lambda x: x["arrival"])

    return processes, num_processes

def validate_times(processes: list[dict]):
    for process in processes:
        if process["arrival"] < 0 or process["burst"] <= 0:
            raise ValueError("Arrival times must be non-negative and burst times must be positive\n")

def read_int_list(name: str, count: int) -> list[int]:
    values = input(f"Enter the {name} of each process separated by spaces.\n").split()
    if len(values) != count:
        raise ValueError(f"Number of {name} values does not match number of processes\n")
    try:
        return [int(x) for x in values]
    except ValueError:
        raise ValueError(f"All {name} values must be integers\n")
