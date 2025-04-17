from schedulers.Scheduler import Scheduler


class FcfsScheduler(Scheduler):

    def run(self):

        # Loop through all sorted processes
        for process in self.processes:
            arrival = process["arrival"]
            burst = process["burst"]

            # If a process hasn't arrived yet, idle until it does
            if arrival > self.current_time:
                self.timeline.append({"id": "idle",
                                      "finish": process["arrival"],
                                      "start": self.current_time})
                self.current_time = process["arrival"]

            # Calculate waiting and turnaround times for the current process
            waiting = self.current_time - arrival
            turnaround = waiting + burst

            # Extract process index from ID (e.g. P1 -> 0)
            process_idx = int(process["id"][1:]) - 1

            self.get_response_time(process_idx, arrival)

            # Store calculated times and update scheduler state
            self.turnaround_time[process_idx] = turnaround
            self.waiting_time[process_idx] = waiting
            self.current_time += burst

            # Store timeline information for visualization
            self.timeline.append({"id": process["id"],
                                  "finish": self.current_time,
                                  "start": self.current_time - burst})
            self.completed.append(process)

        self.show_stats("FCFS")