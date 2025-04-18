from schedulers.FcfsScheduler import FcfsScheduler
from schedulers.PriorityScheduler import PriorityScheduler
from schedulers.RoundRobin import RoundRobin
from schedulers.SjfPreScheduler import SjfPreScheduler
from schedulers.SjfScheduler import SjfScheduler
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.text import Text

console = Console()

def run_scheduler(scheduler_class):
    try:
        scheduler = scheduler_class()
        scheduler.run()
    except Exception as e:
        print(e)
        return False
    return True


def run_app():
    scheduler_map = {
        "1": FcfsScheduler,
        "2": SjfScheduler,
        "3": SjfPreScheduler,
        "4": PriorityScheduler,
        "5": RoundRobin
    }

    while True:
        console.clear()
        console.rule("[bold blue]⚙️ CPU SCHEDULER")

        menu_text = """
[cyan]1.[/] FCFS Scheduler
[cyan]2.[/] Non-Preemptive SJF Scheduler
[cyan]3.[/] Preemptive SJF Scheduler
[cyan]4.[/] Priority Scheduler
[cyan]5.[/] Round-Robin Scheduler
[cyan]6.[/] Exit
"""
        console.print(Panel(menu_text, title="Main Menu", border_style="green"))

        try:
            choice = Prompt.ask("[green]🔎 Your choice[/]")
        except KeyboardInterrupt:
            console.print("\n[bold red]🚪 Exiting... Goodbye![/]")
            break

        console.print()

        if choice in scheduler_map:
            run_scheduler(scheduler_map[choice])
        elif choice == "6":
            console.print("[bold red]👋 Exiting...[/]\n")
            break
        else:
            console.print("[bold red]❌ Invalid choice. Please try again.[/]\n")


if __name__ == "__main__":
    try:
        run_app()
    except KeyboardInterrupt:
        print("Failed to run app")