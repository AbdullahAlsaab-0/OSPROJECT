from schdulers.Scheduler import Scheduler


class FcfsScheduler(Scheduler):

    def __init__(self):
        super().__init__()
        self.response_time = self.waiting_time


    def run(self):

        for process in self.processes:
            arrival = process["arrival"]
            burst = process["burst"]

            if arrival > self.current_time:
                self.current_time = arrival

            waiting_time = self.current_time - arrival
            turnaround = waiting_time + burst

            process_idx = int(process["id"][1:]) - 1

            self.turnaround_time[process_idx] = turnaround
            self.waiting_time[process_idx] = waiting_time
            self.current_time += burst
            self.completed.append(process)

        self.show_stats("FCFS")