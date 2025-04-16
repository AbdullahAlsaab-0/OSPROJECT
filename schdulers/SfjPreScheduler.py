import copy
import heapq

from schdulers.Scheduler import Scheduler


class SfjPreScheduler(Scheduler):

    def __init__(self):
        super().__init__()
        self.response_time = [0] * self.num_processes
        self.responded = [False] * self.num_processes

    def run(self):
        processes_copy = copy.deepcopy(self.processes)
        ready = []
        i = 0
        while i < self.num_processes or ready:
            while i < self.num_processes and processes_copy[i]["arrival"] <= self.current_time:
                heapq.heappush(ready, (processes_copy[i]["burst"], i, processes_copy[i]))
                i += 1

            if ready:
                burst, id, process = heapq.heappop(ready)
                process_idx = int(process["id"][1:]) - 1

                if not self.responded[process_idx]:
                    self.response_time[process_idx] = self.current_time - process["arrival"]
                    self.responded[process_idx] = True

                process["burst"] -= 1
                self.current_time += 1

                if burst == 0:
                    self.turnaround_time[process_idx] = self.current_time - process["arrival"]
                    self.processes[process_idx]["finished"] = self.current_time
                    self.completed.append(self.processes[process_idx])
                else:
                    heapq.heappush(ready, (process["burst"], id, processes_copy[process_idx]))

            else:
                self.current_time = processes_copy[i]["arrival"]

        for idx, process in enumerate(self.processes):
            self.waiting_time[idx] = self.turnaround_time[idx] - self.processes[idx]["burst"]

        self.show_stats("Preemptive-SJF")