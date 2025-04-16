import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random
import heapq

import util
from schdulers.Scheduler import Scheduler


class SJFScheduler(Scheduler):

    def __init__(self):
        super().__init__()
        self.completed = []

    def run(self):
        ready = []
        i = 0

        while i < self.num_processes or ready:
            while i < self.num_processes and self.processes[i]["arrival"] <= self.current_time:
                heapq.heappush(ready, (self.processes[i]["burst"], self.processes[i]))
                i += 1

            if ready:
                burst, process = heapq.heappop(ready)
                process_idx = int(process["id"][1:]) - 1
                waiting_time = self.current_time - process["arrival"]
                turnaround = waiting_time + burst
                self.waiting_time[process_idx]= waiting_time
                self.turnaround_time[process_idx] = turnaround
                self.current_time += burst
                self.completed.append(process)
            else:
                self.current_time = self.processes[i]["arrival"]

        self.show_stats()



    def show_stats(self):
        print(f"\n{'Process':<10}{'Arrival':<10}{'Burst':<10}{'Waiting':<10}{'Turnaround':<10}")
        for process in self.completed:
            process_idx = int(process["id"][1:]) - 1
            print(
                f"{process["id"]:<10}{process["arrival"]:<10}{process["burst"]:<10}{self.waiting_time[process_idx]:<10}{self.turnaround_time[process_idx]:<10}")
        AWT = sum(self.waiting_time) / len(self.waiting_time)
        ATT = sum(self.turnaround_time) / len(self.turnaround_time)
        print(f"\nAverage Waiting Time: {AWT:.2f}")
        print(f"Average Turnaround Time: {ATT:.2f}\n")
        self.show_gantt_chart()

    def show_gantt_chart(self):
        fig, gnt = plt.subplots(figsize=(10, 2.5))

        gnt.set_title("SJF Gantt Chart", fontsize=14)
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
                # Idle block
                idle_time = arrival - current_time
                gnt.broken_barh([(current_time, idle_time)], (10, 10), facecolors='lightgrey')
                gnt.text(current_time + idle_time / 2, 15, "IDLE", ha='center', va='center', fontsize=8)

                current_time = arrival

            # Process block
            gnt.broken_barh([(current_time, burst)], (10, 10), facecolors=color, edgecolors='black')
            gnt.text(current_time + burst / 2, 15, pid, ha='center', va='center', color='white', fontsize=9)

            # Tick label
            gnt.text(current_time, 5, str(current_time), ha='center', fontsize=8)
            current_time += burst

            legend_patches.append(patches.Patch(color=color, label=pid))

        # Final tick
        gnt.text(current_time, 5, str(current_time), ha='center', fontsize=8)

        gnt.legend(handles=legend_patches, bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
        plt.tight_layout()
        plt.show()