import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import random

class FCFS_Scheduler():
    def __init__(self):
        self.num_processes = 0
        self.processes = []
        self.waiting_time = []
        self.turnaround_time = []
        self.current_time = 0

    def __str__(self):
        return f"Number of processes = {self.num_processes}, processes = {self.processes}"

    def read_processes(self):

        try:
            self.num_processes = int(input("How many processes are there? "))
        except ValueError:
            raise ValueError("Please enter a number.")

        arrival_time = input("Enter the arrival time of each process separated by spaces.\n").split()
        burst_time = input("Enter the burst time of each process separated by spaces.\n").split()

        if (len(arrival_time) != self.num_processes or len(burst_time) != self.num_processes):
            raise ValueError("Number of arrival times and burst times does not match number of processes")

        try:
            self.processes = sorted([ {"id":f"P{idx+1}", "arrival":int(x[0]), "burst":int(x[1])}
                                      for idx, x in enumerate(zip(arrival_time, burst_time)) ],
                                    key=lambda x: x["arrival"])
        except ValueError:
            raise ValueError("non integer arrival time or burst time")

    def run(self):
        self.current_time = 0
        for process in self.processes:
            arrival = process["arrival"]
            burst = process["burst"]

            if arrival > self.current_time:
                print(f"CPU idle from {self.current_time} to {arrival}")
                self.current_time = arrival

            waiting_time = self.current_time - arrival
            turnaround = waiting_time + burst

            self.turnaround_time.append(turnaround)
            self.waiting_time.append(waiting_time)
            self.current_time += burst


        self.show_stats()

    def show_stats(self):
        print(f"\n{'Process':<10}{'Arrival':<10}{'Burst':<10}{'Waiting':<10}{'Turnaround':<10}")
        for idx, process in enumerate(self.processes):
            print(
                f"{process["id"]:<10}{process["arrival"]:<10}{process["burst"]:<10}{self.waiting_time[idx]:<10}{self.turnaround_time[idx]:<10}")
        AWT = sum(self.waiting_time) / len(self.waiting_time)
        ATT = sum(self.turnaround_time) / len(self.turnaround_time)
        print(f"\nAverage Waiting Time: {AWT:.2f}")
        print(f"Average Turnaround Time: {ATT:.2f}")
        self.show_gantt_chart()

    def show_gantt_chart(self):
        fig, gnt = plt.subplots(figsize=(10, 2.5))

        gnt.set_title("FCFS Gantt Chart", fontsize=14)
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

        for i, process in enumerate(self.processes):
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

            legend_patches.append(mpatches.Patch(color=color, label=pid))

        # Final tick
        gnt.text(current_time, 5, str(current_time), ha='center', fontsize=8)

        gnt.legend(handles=legend_patches, bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
        plt.tight_layout()
        plt.show()