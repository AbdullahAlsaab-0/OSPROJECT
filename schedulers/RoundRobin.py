import copy
import heapq

from schedulers.Scheduler import Scheduler


class RoundRobin(Scheduler):

    def __init__(self):
        super().__init__(interval=True)

    def run(self):
        processes_copy = copy.deepcopy(self.processes)
        ready = []
        requeue_priority = max([process["arrival"] for process in processes_copy]) + 1
        i = 0

        # Loop through all processes sorted by arrival time
        while i < self.num_processes or ready:
            # If there are processes that have arrived, add them to the ready queue
            while i < self.num_processes and processes_copy[i]["arrival"] <= self.current_time:
                heapq.heappush(ready, (processes_copy[i]["arrival"], i, processes_copy[i]))
                i += 1

            if ready:
                arrival, id, process = heapq.heappop(ready)
                process_idx = int(process["id"][1:]) - 1

                self.get_response_time(process_idx, arrival)

                # If the burst time of the current process is less than the quantum, finish the entire process
                execution_time = min(self.quantum, process["burst"])

                # Update scheduler state and store timeline information for visualization
                process["burst"] -= execution_time
                self.current_time += execution_time
                self.timeline.append({"id": process["id"],
                                      "finish": self.current_time,
                                      "start": self.current_time - execution_time})

                # If the current process has finished, update turnaround times and add it to the completed list
                if process["burst"] == 0:
                    self.turnaround_time[process_idx] = self.current_time - process["arrival"]
                    self.processes[process_idx]["finished"] = self.current_time
                    self.completed.append(self.processes[process_idx])
                else:
                    # If the current process hasn't finished, add it back to the end of the ready queue
                    heapq.heappush(ready, (requeue_priority, id, process))
                    requeue_priority += 1
            else:
                self.handle_idle_time(i)

        # Calculate waiting times for each process
        self.completed.sort(key=lambda x: x["id"])
        for idx, process in enumerate(self.processes):
            self.waiting_time[idx] = self.turnaround_time[idx] - self.completed[idx]["burst"]
        self.show_stats("Round-Robin")


