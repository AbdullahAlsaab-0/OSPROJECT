from rich.console import Console
from rich.prompt import Prompt, IntPrompt
from typing import List, Dict, Tuple

console = Console()


def read_input_processes(priority: bool = False, interval: bool = False) -> Tuple[List[Dict], int, int]:
    console.rule("[bold blue]CPU Scheduler Input")

    while True:
        try:
            num_processes = IntPrompt.ask("[bold]How many processes are there?[/]")
            if num_processes <= 0:
                raise ValueError()
            break
        except ValueError:
            console.print("[red]Please enter a positive integer.[/]\n")

    arrival_time = Prompt.ask(f"Enter [green]arrival times[/] separated by spaces").split()
    burst_time = Prompt.ask(f"Enter [green]burst times[/] separated by spaces").split()

    if len(arrival_time) != num_processes or len(burst_time) != num_processes:
        console.print(
            f"[red]❌ Expected {num_processes} values for each attribute, but got {len(arrival_time)} arrival times and {len(burst_time)} burst times.[/]")
        raise ValueError("Mismatched input lengths.\n")

    try:
        processes = [
            {"id": f"P{idx + 1}", "arrival": int(x[0]), "burst": int(x[1])}
            for idx, x in enumerate(zip(arrival_time, burst_time))
        ]
    except ValueError:
        console.print("[red]❌ Arrival time or burst time contains non-integer values.[/]")
        raise

    validate_times(processes)

    if priority:
        priorities = read_int_list("priority", num_processes)
        for idx, process in enumerate(processes):
            process["priority"] = priorities[idx]

    quantum = None
    if interval:
        while True:
            try:
                quantum = IntPrompt.ask("Enter the [bold]interval (quantum)[/] for the processes")
                if quantum <= 0:
                    raise ValueError()
                break
            except ValueError:
                console.print("[red]❌ Interval can't be zero or negative.[/]")

    processes = sorted(processes, key=lambda x: x["arrival"])
    console.rule("[green]Input Received Successfully")

    return processes, num_processes, quantum

def validate_times(processes: list[dict]):
    for process in processes:
        if process["arrival"] < 0 or process["burst"] <= 0:
            console.print(f"[red]❌ Invalid input for {process['id']} — arrival must be ≥ 0 and burst must be > 0[/]")
            raise ValueError("Arrival times must be non-negative and burst times must be positive\n")


def read_int_list(name: str, count: int) -> list[int] | None:
    while True:
        raw_input = Prompt.ask(f"Enter the [bold]{name}[/] values separated by spaces").split()
        if len(raw_input) != count:
            console.print(f"[red]❌ Expected {count} values, but got {len(raw_input)}.[/]")
            continue
        try:
            return [int(x) for x in raw_input]
        except ValueError:
            console.print(f"[red]❌ All {name} values must be integers.[/]")
