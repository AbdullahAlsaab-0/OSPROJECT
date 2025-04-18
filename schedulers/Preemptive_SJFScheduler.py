import heapq
import copy
from schedulers.Scheduler import Scheduler

class Preemptive_SJFScheduler(Scheduler):

    def run(self):
        processes = copy.deepcopy(self.processes)  # deep copy to avoid breaking existing data
        ready = []  # Min-heap to store available processes by (burst, index, process) located at util.py
        i = 0  # Index for tracking arrivals
        current_process = None  # Currently running process (can be 0)
        start_time = 0  # Start time of the current portion
        current_process_id = None  # ID of the process currently executing

        # Main loop runs until all processes are complete
        while i < self.num_processes or ready:
            # Add all new processes to the ready heap
            while i < self.num_processes and processes[i]["arrival"] <= self.current_time:
                heapq.heappush(ready, (processes[i]["burst"], i, processes[i]))
                i += 1

            if ready:
                # Pick the process with the shortest burst remaining
                burst, idx, process = heapq.heappop(ready)
                process_idx = int(process["id"][1:]) - 1   # Convert 'P1' → 0, 'P2' → 1

                #  update timeline for previous one
                if current_process_id != process["id"]:
                    if current_process_id:
                        self.timeline.append({
                            "id": current_process_id,
                            "start": start_time,
                            "finish": self.current_time
                        })
                    current_process_id = process["id"]
                    start_time = self.current_time
                    self.get_response_time(process_idx, process["arrival"])

                # + one unit of CPU time
                process["burst"] -= 1
                self.current_time += 1 # this one is preemptive
                # Non-preemptive: process runs to completion without interruption (unlike preemptive SJF, which runs 1 unit at a time and allows context switching)

                if process["burst"] == 0:
                    # If process finished, compute stats
                    self.timeline.append({
                        "id": process["id"],
                        "start": start_time,
                        "finish": self.current_time
                    })
                    self.turnaround_time[process_idx] = self.current_time - process["arrival"]
                    self.completed.append(self.processes[process_idx])
                    current_process_id = None  # CPU free
                else:
                    # If not done, put it back in the heap with updated burst
                    heapq.heappush(ready, (process["burst"], idx, process))
            else:
                # If no process is ready, jump to next arrival
                self.handle_idle_time(i)

        # Calculate waiting time after it ends
        for idx, process in enumerate(self.processes):
            self.waiting_time[idx] = self.turnaround_time[idx] - self.processes[idx]["burst"]

        # Display it to user
        self.show_stats("Preemptive-SJF")
