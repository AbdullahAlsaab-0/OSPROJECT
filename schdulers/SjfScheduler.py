import heapq

from schdulers.Scheduler import Scheduler


class SjfScheduler(Scheduler):

    def __init__(self):
        super().__init__()
        self.response_time = self.waiting_time

    def run(self):
        ready = []
        i = 0

        while i < self.num_processes or ready:
            while i < self.num_processes and self.processes[i]["arrival"] <= self.current_time:
                heapq.heappush(ready, (self.processes[i]["burst"],i , self.processes[i]))
                i += 1

            if ready:
                burst, _, process = heapq.heappop(ready)
                process_idx = int(process["id"][1:]) - 1

                waiting_time = self.current_time - process["arrival"]
                turnaround = waiting_time + burst

                self.waiting_time[process_idx]= waiting_time
                self.turnaround_time[process_idx] = turnaround
                self.current_time += burst
                self.completed.append(process)
            else:
                self.current_time = self.processes[i]["arrival"]

        self.show_stats("Non-Preemptive-SJF")