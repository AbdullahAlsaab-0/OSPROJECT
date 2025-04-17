import heapq

from schedulers.Scheduler import Scheduler


class SjfScheduler(Scheduler):

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

                if not self.responded[process_idx]:
                    self.response_time[process_idx] = self.current_time - process["arrival"]
                    self.responded[process_idx] = True

                self.waiting_time[process_idx]= waiting_time
                self.turnaround_time[process_idx] = turnaround
                self.current_time += burst
                self.timeline.append({"id": process["id"],
                                      "finish": self.current_time,
                                      "start": self.current_time - burst})
                self.completed.append(process)
            else:
                self.current_time = self.processes[i]["arrival"]

        self.show_stats("Non-Preemptive-SJF")