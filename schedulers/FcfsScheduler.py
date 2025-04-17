from schedulers.Scheduler import Scheduler


class FcfsScheduler(Scheduler):

    def run(self):

        for process in self.processes:
            arrival = process["arrival"]
            burst = process["burst"]

            if arrival > self.current_time:
                self.timeline.append({"id": "idle",
                                      "finish": process["arrival"],
                                      "start": self.current_time})
                self.current_time = process["arrival"]

            waiting = self.current_time - arrival
            turnaround = waiting + burst

            process_idx = int(process["id"][1:]) - 1

            if not self.responded[process_idx]:
                self.response_time[process_idx] = self.current_time - arrival
                self.responded[process_idx] = True

            self.turnaround_time[process_idx] = turnaround
            self.waiting_time[process_idx] = waiting
            self.current_time += burst
            self.timeline.append({"id": process["id"],
                                  "finish": self.current_time,
                                  "start": self.current_time - burst})
            self.completed.append(process)

        self.show_stats("FCFS")