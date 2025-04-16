import random

from matplotlib import pyplot as plt, patches

import util


class Scheduler():
    def __init__(self, priority=False, interval=False):
        self.processes, self.num_processes = util.read_input_processes(priority, interval)
        self.waiting_time = [0] * self.num_processes
        self.turnaround_time = [0] * self.num_processes
        self.current_time = 0
        self.completed = []

    def __str__(self):
        return f"Number of processes = {self.num_processes}, processes = {self.processes}"

    # def read_processes(self, sort:str, priority:bool=False, interval:bool=False):
    #     self.processes, self.num_processes = util.read_input_processes(sort, priority, interval)

    def show_stats(self, algo):
        print(f"\n{'Process':<10}{'Arrival':<10}{'Burst':<10}{'Waiting':<10}{'Turnaround':<10}")
        for process in self.completed:
            process_idx = int(process["id"][1:]) - 1
            print(
                f"{process["id"]:<10}{process["arrival"]:<10}{process["burst"]:<10}{self.waiting_time[process_idx]:<10}{self.turnaround_time[process_idx]:<10}")
        AWT = sum(self.waiting_time) / len(self.waiting_time)
        ATT = sum(self.turnaround_time) / len(self.turnaround_time)
        print(f"\nAverage Waiting Time: {AWT:.2f}")
        print(f"Average Turnaround Time: {ATT:.2f}\n")
        self.show_gantt_chart(algo)

    def show_gantt_chart(self, algo):
        fig, gnt = plt.subplots(figsize=(10, 2.5))

        gnt.set_title(f"{algo} Gantt Chart", fontsize=14)
        gnt.set_xlabel("Time")
        gnt.set_yticks([])  # Hide y-axis
        gnt.set_ylim(0, 30)
        gnt.set_xlim(0, self.current_time + 2)

        colors = [
            "#4e79a7", "#f28e2b", "#e15759", "#76b7b2", "#59a14f",
            "#edc949", "#af7aa1", "#ff9da7", "#9c755f", "#bab0ab"
        ]
        random.shuffle(colors)

        current_time = 0
        legend_patches = []

        for i, process in enumerate(self.completed):
            arrival = process["arrival"]
            burst = process["burst"]
            pid = process["id"]
            color = colors[i % len(colors)]

            if arrival > current_time:
                idle_time = arrival - current_time
                gnt.broken_barh([(current_time, idle_time)], (10, 10), facecolors='lightgrey')
                gnt.text(current_time + idle_time / 2, 15, "IDLE", ha='center', va='center', fontsize=8)

                current_time = arrival

            gnt.broken_barh([(current_time, burst)], (10, 10), facecolors=color, edgecolors='black')
            gnt.text(current_time + burst / 2, 15, pid, ha='center', va='center', color='white', fontsize=9)

            gnt.text(current_time, 5, str(current_time), ha='center', fontsize=8)
            current_time += burst

            legend_patches.append(patches.Patch(color=color, label=pid))

        gnt.text(current_time, 5, str(current_time), ha='center', fontsize=8)

        gnt.legend(handles=legend_patches, bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
        plt.tight_layout()
        plt.show()