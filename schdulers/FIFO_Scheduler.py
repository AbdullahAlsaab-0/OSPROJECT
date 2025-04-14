import time

class FIFO_Scheduler():
    def __init__(self):
        self.num_processes = 0
        self.processes = []
        self.waiting_time = []
        self.turnaround_time = []

    def __str__(self):
        return f"Number of processes = {self.num_processes}, processes = {self.processes}"

    def read_processes(self):
        try:
            self.num_processes = int(input("How many processes are there? "))
        except ValueError:
            raise ValueError("Please enter a number.")

        arrival_time = input("Enter the arrival time of each process separated by a space.\n").split()
        burst_time = input("Enter the burst time of each process separated by a space.\n").split()

        if (len(arrival_time) != self.num_processes or len(burst_time) != self.num_processes):
            print(arrival_time, burst_time)
            raise ValueError("Number of arrival times and burst times does not match number of processes")
        try:
            self.processes = sorted(([[int(x[0]), int(x[1])] for x in zip(arrival_time, burst_time)]), key=lambda x: x[0])
        except ValueError:
            raise ValueError("non integer arrival time or burst time")

    def start(self, process):
        print("Starting process {}".format(process))
        time.sleep(process[1])
        print("Process completed")
        return process[1]

    def run(self):
        turnaround = 0
        for i in range(len(self.processes)):
            self.waiting_time.append(turnaround)
            turnaround = self.start(self.processes[i]) + turnaround
            self.turnaround_time.append(turnaround)

    def show_stats(self):
        for idx, process in enumerate(self.processes):
            print(f"Process {idx + 1}, turnaround: {self.turnaround_time[idx]}, waiting time: {self.waiting_time[idx]}")
        AWT = sum(self.waiting_time) / len(self.waiting_time)
        ATT = sum(self.turnaround_time) / len(self.turnaround_time)
        print(f"AWT: {AWT}, ATT: {ATT}")
