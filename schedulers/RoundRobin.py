import copy
import heapq

from schedulers.Scheduler import Scheduler


class RoundRobin(Scheduler):

    def __init__(self):
        super().__init__(interval=True)

    def run(self):
        processes_copy = copy.deepcopy(self.processes)
        ready = []
        process_sorter = max([process["arrival"] for process in processes_copy]) + 1
        i = 0

        while i < self.num_processes or ready:
            while i < self.num_processes and processes_copy[i]["arrival"] <= self.current_time:
                heapq.heappush(ready, (processes_copy[i]["arrival"], i, processes_copy[i]))
                i += 1

            if ready:
                arrival, id, process = heapq.heappop(ready)
                process_idx = int(process["id"][1:]) - 1

                if not self.responded[process_idx]:
                    self.response_time[process_idx] = self.current_time - process["arrival"]
                    self.responded[process_idx] = True

                execution_time = min(self.interval, process["burst"])

                process["burst"] -= execution_time
                self.current_time += execution_time

                self.timeline.append({"id": process["id"],
                                      "finish": self.current_time,
                                      "start": self.current_time - execution_time})


                if process["burst"] == 0:
                    self.turnaround_time[process_idx] = self.current_time - process["arrival"]
                    self.processes[process_idx]["finished"] = self.current_time
                    self.completed.append(self.processes[process_idx])
                else:
                    heapq.heappush(ready, (process_sorter, id, process))
                    process_sorter += 1
            else:
                self.timeline.append({"id": "idle",
                                      "finish": processes_copy[i]["arrival"],
                                      "start": self.current_time})
                self.current_time = processes_copy[i]["arrival"]


        for idx, process in enumerate(self.processes):
            self.waiting_time[idx] = self.turnaround_time[idx] - self.processes[idx]["burst"]
        self.show_stats("Round-Robin")


