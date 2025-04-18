import heapq
from schedulers.Scheduler import Scheduler

class Non_Preemptive_SJFScheduler(Scheduler):

    def run(self):
        i = 0  # Index to track  arrivals
        ready = []  # Min-heap to store processes sorted by burst time

        # Continue until all processes have been handled
        while i < self.num_processes or ready:
            # Add all processes that have arrived by current time to the heap
            while i < self.num_processes and self.processes[i]["arrival"] <= self.current_time:
                heapq.heappush(ready, (self.processes[i]["burst"], i, self.processes[i]))
                i += 1

            if ready:
                # Pick the process with the shortest burst time
                burst, idx, process = heapq.heappop(ready)
                process_idx = int(process["id"][1:]) - 1  # Convert 'P1' → 0, 'P2' → 1

                # Record response time if this is the first time it's being picked
                self.get_response_time(process_idx, process["arrival"])

                start = self.current_time  # Mark process start time
                self.current_time += burst  # Non-preemptive: process runs to completion without interruption (unlike preemptive SJF, which runs 1 unit at a time and allows context switching)

                # If process finished, compute stats
                self.timeline.append({
                    "id": process["id"],
                    "start": start,
                    "finish": self.current_time
                })

                # Calculate and store turnaround and waiting time
                self.turnaround_time[process_idx] = self.current_time - process["arrival"]
                self.waiting_time[process_idx] = self.turnaround_time[process_idx] - burst

                # Mark process as completed
                self.completed.append(process)
            else:
                # If no process is ready, move time forward to the next arrival
                self.handle_idle_time(i)

        # Display it to the user
        self.show_stats("Non-Preemptive-SJF")
