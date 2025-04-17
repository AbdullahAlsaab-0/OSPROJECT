import random

from matplotlib import pyplot as plt, patches

import util


class Scheduler():
    def __init__(self, priority=False, interval=False):
        self.processes, self.num_processes = util.read_input_processes(priority, interval)
        self.waiting_time = [0] * self.num_processes
        self.turnaround_time = [0] * self.num_processes
        self.response_time = [0] * self.num_processes
        self.response_time = [0] * self.num_processes
        self.responded = [False] * self.num_processes
        self.current_time = 0
        self.completed = []
        self.timeline = []

    def __str__(self):
        return f"Number of processes = {self.num_processes}, processes = {self.processes}"

    def show_stats(self, name: str):
        print(f"\n{name} Scheduling\n")
        print(f"{'Process':<10}{'Arrival':<10}{'Burst':<10}"
              f"{'Waiting':<10}{'Turnaround':<15}"
              f"{'Response':<10}")

        for idx, process in enumerate(self.completed):
            process_idx = int(process["id"][1:]) - 1
            print(f"{process['id']:<10}{process['arrival']:<10}{process['burst']:<10}"
                  f"{self.waiting_time[process_idx]:<10}{self.turnaround_time[process_idx]:<15}"
                  f"{self.response_time[process_idx]:<10}")

        avg_waiting = sum(self.waiting_time) / self.num_processes
        avg_turnaround = sum(self.turnaround_time) / self.num_processes
        avg_response = (
            sum(self.response_time) / self.num_processes
            if hasattr(self, 'response_time') else None
        )

        print(f"\nAverage Waiting Time: {avg_waiting:.2f}")
        print(f"Average Turnaround Time: {avg_turnaround:.2f}")
        if avg_response is not None:
            print(f"Average Response Time: {avg_response:.2f}\n")
        self.show_gantt_chart(name)

    def show_gantt_chart(self, algo):
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

            # Handle idle time
            if start > current_time:
                idle_time = start - current_time
                gnt.broken_barh([(current_time, idle_time)], (10, 10), facecolors='lightgrey')
                gnt.text(current_time + idle_time / 2, 15, "IDLE", ha='center', va='center', fontsize=8)
                gnt.text(current_time, 5, str(current_time), ha='center', fontsize=8)
                current_time = start

            # Assign a color if it's a new PID
            if id not in colors:
                colors[id] = available_colors[len(colors) % len(available_colors)]

            color = colors[id]
            duration = end - start

            gnt.broken_barh([(start, duration)], (10, 10), facecolors=color, edgecolors='black')
            gnt.text(start + duration / 2, 15, id, ha='center', va='center', color='white', fontsize=9)
            gnt.text(start, 5, str(start), ha='center', fontsize=8)

            current_time = end

            if id not in used_pids:
                legend_patches.append(patches.Patch(color=color, label=id))
                used_pids.add(id)

        # Final time marker
        gnt.text(current_time, 5, str(current_time), ha='center', fontsize=8)

        gnt.legend(handles=legend_patches, bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
        plt.tight_layout()
        plt.show()