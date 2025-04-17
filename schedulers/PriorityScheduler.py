import heapq

from schedulers.Scheduler import Scheduler


class PriorityScheduler(Scheduler):

    def __init__(self):
        super().__init__(priority=True)

    def run(self):
        ready = []
        i = 0

        # Loop through all processes sorted by arrival time
        while i < self.num_processes or ready:
            # If there are processes that have arrived, add them to the ready queue
            while i < self.num_processes and self.processes[i]["arrival"] <= self.current_time:
                heapq.heappush(ready, (self.processes[i]["priority"], i, self.processes[i]))
                i += 1

            if ready:
                priority, _, process = heapq.heappop(ready)
                process_idx = int(process["id"][1:]) - 1 # Extract process index from ID (e.g. P1 -> 0)

                # Calculate waiting and turnaround times for the current process
                waiting = self.current_time - process["arrival"]
                turnaround = waiting + process["burst"]

                self.get_response_time(process_idx, process["arrival"])

                # Update scheduler state and store timeline information for visualization
                self.waiting_time[process_idx] = waiting
                self.turnaround_time[process_idx] = turnaround
                self.current_time += process["burst"]
                self.timeline.append({"id": process["id"],
                                      "finish": self.current_time,
                                      "start": self.current_time - process["burst"]})
                self.completed.append(process)
            else:
                self.handle_idle_time(i)


        self.show_stats("Priority")
