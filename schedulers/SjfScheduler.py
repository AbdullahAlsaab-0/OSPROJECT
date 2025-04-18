    from schedulers.Scheduler import Scheduler

    class SjfScheduler(Scheduler):

        def run(self):

            self.current_time = 0  # Reset current time to 0
            remaining = self.processes.copy()  # Copy original list to modify

            while remaining:
                available = []

                # Gather processes that have arrived
                for p in remaining:
                    if p["arrival"] <= self.current_time:
                        available.append(p)

                # If no process is ready CPU is idle
                if not available:
                    # Find the next process that will arrive
                    next_arrival = min(p["arrival"] for p in remaining)
                    self.timeline.append({
                        "id": "idle", 
                        "start": self.current_time, 
                        "finish": next_arrival
                    })
                    self.current_time = next_arrival
                    continue

                # Sort available processes by burst time
                available.sort(key=lambda x: (x["burst"], x["arrival"]))
                process = available[0]
                process_idx = int(process["id"][1:]) - 1  

                # Set response time if not already set
                self.get_response_time(process_idx, process["arrival"])

                # Simulate process execution
                start = self.current_time
                self.current_time += process["burst"]
                finish = self.current_time

                # Update the Gantt chart timeline
                self.timeline.append({
                    "id": process["id"],
                    "start": start,
                    "finish": finish
                })

                # Compute turnaround and waiting times
                self.turnaround_time[process_idx] = finish - process["arrival"]
                self.waiting_time[process_idx] = self.turnaround_time[process_idx] - process["burst"]

                # Add process to completed list
                self.completed.append(process)

                # Remove the finished process
                remaining.remove(process)

            self.show_stats("Non-Preemptive-SJF")
