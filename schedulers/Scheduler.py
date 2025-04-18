import random

from matplotlib import pyplot as plt, patches

import util


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
        print(f"\n{name} Scheduling\n")
        print(f"{'Process':<10}{'Arrival':<10}{'Burst':<10}"
              f"{'Waiting':<10}{'Turnaround':<15}"
              f"{'Response':<10}")

        # Print waiting, turnaround, and response times for completed processes
        for idx, process in enumerate(self.completed):
            process_idx = int(process["id"][1:]) - 1
            print(f"{process['id']:<10}{process['arrival']:<10}{process['burst']:<10}"
                  f"{self.waiting_time[process_idx]:<10}{self.turnaround_time[process_idx]:<15}"
                  f"{self.response_time[process_idx]:<10}")

        # Calculate average waiting, turnaround, and response times for all processes
        avg_waiting = sum(self.waiting_time) / self.num_processes
        avg_turnaround = sum(self.turnaround_time) / self.num_processes
        avg_response = sum(self.response_time) / self.num_processes



        print(f"\nAverage Waiting Time: {avg_waiting:.2f}")
        print(f"Average Turnaround Time: {avg_turnaround:.2f}")
        print(f"Average Response Time: {avg_response:.2f}\n")
        # If Round-Robin is chosen, calculate and print the number of context switches
        if self.quantum:
            print(f"Number of context switches: {len(self.timeline) - 1}\n")

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
            gnt.text(start + duration / 2, 15, id, ha='center', va='center', color='white', fontsize=9)
            gnt.text(start, 5, str(start), ha='center', fontsize=8)

            current_time = end

            if id not in used_pids:
                legend_patches.append(patches.Patch(color=color, label=id))
                used_pids.add(id)

        gnt.text(current_time, 5, str(current_time), ha='center', fontsize=8)

        gnt.legend(handles=legend_patches, bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
        plt.tight_layout()
        plt.show()