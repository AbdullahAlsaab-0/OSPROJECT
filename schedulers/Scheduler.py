import random
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from matplotlib import pyplot as plt, patches
from rich.align import Align
import util

console = Console()

class Scheduler:

    def __init__(self, priority:bool=False, interval:bool=False):
        self.processes, self.num_processes, self.quantum = util.read_input_processes(priority, interval)
        self.waiting_time = [0] * self.num_processes
        self.turnaround_time = [0] * self.num_processes
        self.response_time = [0] * self.num_processes
        self.responded = [False] * self.num_processes
        self.current_time = 0
        self.completed = []
        self.timeline = []

    def __str__(self) -> str:
        return f"Number of processes = {self.num_processes}, processes = {self.processes}"

    def get_response_time(self, process_idx:int, arrival:int):
        if not self.responded[process_idx]:
            self.response_time[process_idx] = self.current_time - arrival
            self.responded[process_idx] = True

    def handle_idle_time(self, i:int):
        self.timeline.append({"id": "idle",
                              "finish": self.processes[i]["arrival"],
                              "start": self.current_time})
        self.current_time = self.processes[i]["arrival"]

    def show_stats(self, name: str):
        console.rule(f"[bold blue]📈 {name} Scheduling Stats")

        table = Table(show_header=True, header_style="bold magenta", border_style="dim")
        table.add_column("📛 Process", style="cyan", justify="center")
        table.add_column("🕓 Arrival", justify="right")
        table.add_column("⚙️ Burst", justify="right")
        table.add_column("⌛ Waiting", justify="right")
        table.add_column("🔁 Turnaround", justify="right")
        table.add_column("📥 Response", justify="right")

        for idx, process in enumerate(self.completed):
            i = int(process["id"][1:]) - 1
            table.add_row(
                process["id"],
                str(process["arrival"]),
                str(process["burst"]),
                str(self.waiting_time[i]),
                str(self.turnaround_time[i]),
                str(self.response_time[i]),
            )

        # Center the table
        console.print(Align.center(table))

        avg_waiting = sum(self.waiting_time) / self.num_processes
        avg_turnaround = sum(self.turnaround_time) / self.num_processes
        avg_response = sum(self.response_time) / self.num_processes

        summary_text = (
            f"📊 [bold]Averages[/bold]\n\n"
            f"⏳ [cyan]Waiting Time:[/] [green]{avg_waiting:.2f}[/]\n"
            f"🔁 [cyan]Turnaround Time:[/] [green]{avg_turnaround:.2f}[/]\n"
            f"📥 [cyan]Response Time:[/] [green]{avg_response:.2f}[/]"
        )

        panel = Panel.fit(
            summary_text,
            title="📌 Summary",
            title_align="left",
            border_style="bright_blue",
            padding=(1, 4)
        )

        # Center the panel
        console.print(Align.center(panel))

        if self.quantum:
            context_msg = f"\n[bold yellow]🔄 Context Switches:[/] [bright_white]{len(self.timeline) - 1}[/]"
            console.print(Align.center(context_msg))

        self.show_gantt_chart(name)

    def show_gantt_chart(self, algo:str):
        fig, gnt = plt.subplots(figsize=(10, 2.5))

        gnt.set_title(f"{algo} Gantt Chart", fontsize=14)
        gnt.set_xlabel("Time")
        gnt.set_yticks([])
        gnt.set_ylim(0, 30)
        gnt.set_xlim(0, self.current_time + 2)

        colors = {}
        available_colors = [
            "#4e79a7", "#f28e2b", "#e15759", "#76b7b2", "#59a14f",
            "#edc949", "#af7aa1", "#ff9da7", "#9c755f", "#bab0ab"
        ]
        random.shuffle(available_colors)

        legend_patches = []
        used_pids = set()

        current_time = 0

        for segment in self.timeline:
            id = segment["id"]
            start = segment["start"]
            end = segment["finish"]

            if id not in colors:
                colors[id] = available_colors[len(colors) % len(available_colors)]

            color = colors[id]
            duration = end - start

            gnt.broken_barh([(start, duration)], (10, 10), facecolors=color, edgecolors='black')
            gnt.text(start + duration / 2, 15, id, ha='center', va='center', color='white', fontsize=9, weight='bold')
            gnt.text(start, 5, str(start), ha='center', fontsize=8)

            current_time = end

            if id not in used_pids:
                legend_patches.append(patches.Patch(color=color, label=id))
                used_pids.add(id)

        gnt.text(current_time, 5, str(current_time), ha='center', fontsize=8)

        gnt.legend(handles=legend_patches, bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
        plt.tight_layout()
        plt.show()