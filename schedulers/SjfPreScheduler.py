import copy
import heapq

from schedulers.Scheduler import Scheduler


class SjfPreScheduler(Scheduler):

    def run(self):
        processes_copy = copy.deepcopy(self.processes)
        ready = []
        i = 0
        start_time = 0
        current_process_id = None

        # Loop through all processes sorted by arrival time
        while i < self.num_processes or ready:
            # If there are processes that have arrived, add them to the ready queue
            while i < self.num_processes and processes_copy[i]["arrival"] <= self.current_time:
                heapq.heappush(ready, (processes_copy[i]["burst"], i, processes_copy[i]))
                i += 1

            if ready:
                burst, id, process = heapq.heappop(ready)
                process_idx = int(process["id"][1:]) - 1

                # if context switch happened update timeline of the previous process and update current_process_id
                if current_process_id != process["id"]:
                    if current_process_id:
                        self.timeline.append({"id": current_process_id,
                                              "finish": self.current_time,
                                              "start": start_time})
                    current_process_id = process["id"]
                    start_time = self.current_time

                self.get_response_time(process_idx, process["arrival"])

                process["burst"] -= 1
                self.current_time += 1


                # If the current process has finished, update turnaround times and timeline and add it to the completed list
                if process["burst"] == 0:
                    self.turnaround_time[process_idx] = self.current_time - process["arrival"]
                    self.processes[process_idx]["finished"] = self.current_time
                    self.completed.append(self.processes[process_idx])

                    self.timeline.append({"id": process["id"],
                                          "finish": self.current_time,
                                          "start": start_time})

                    current_process_id = None
                else:
                    # If the current process hasn't finished, add it back to the ready queue'
                    heapq.heappush(ready, (process["burst"], id, processes_copy[process_idx]))
            else:
                self.handle_idle_time(i)

        # Calculate waiting times for each process
        for idx, process in enumerate(self.processes):
            self.waiting_time[idx] = self.turnaround_time[idx] - self.processes[idx]["burst"]

        self.show_stats("Preemptive-SJF")