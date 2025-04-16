import heapq

from schdulers.Scheduler import Scheduler


class PriorityScheduler(Scheduler):
    def __init__(self):
        super().__init__(priority=True)

    def run(self):
        ready = []
        i = 0

        while i < self.num_processes or ready:
            while i < self.num_processes and self.processes[i]["arrival"] <= self.current_time:
                heapq.heappush(ready, (self.processes[i]["priority"], self.processes[i]))
                i += 1

            if ready:
                _, process = heapq.heappop(ready)
                process_idx = int(process["id"][1:]) - 1

                waiting_time = self.current_time - process["arrival"]
                turnaround_time = waiting_time + process["burst"]

                self.waiting_time[process_idx] = waiting_time
                self.turnaround_time[process_idx] = turnaround_time
                self.current_time += process["burst"]
                self.completed.append(process)
            else:
                self.current_time = self.processes[i]["arrival"]

        self.show_stats("Priority")
