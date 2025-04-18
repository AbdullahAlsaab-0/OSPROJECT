from schedulers.Scheduler import Scheduler
import heapq
import copy


class SjfPreScheduler(Scheduler):

        def run(self):
            processes_copy = copy.deepcopy(self.processes)
            remaining_burst = [p["burst"] for p in processes_copy]
            completed_count = 0
            i = 0  # index for tracking which processes have arrived
            heap = []
            current_process = None
            current_index = None
            start_time = None
            #ihatemylifewhatdoesthisshitevenmean
            while completed_count < self.num_processes:
                # Push all processes that have arrived into the heap
                while i < self.num_processes and processes_copy[i]["arrival"] <= self.current_time:
                    heapq.heappush(heap, (remaining_burst[i], i, processes_copy[i]))
                    i += 1

                # If there's a running process and a new shorter one arrives
                if current_process and heap:
                    if heap[0][0] < remaining_burst[current_index]:
                        self.timeline.append({
                            "id": current_process["id"],
                            "start": start_time,
                            "finish": self.current_time
                        })
                        heapq.heappush(heap, (remaining_burst[current_index], current_index, current_process))
                        current_process = None

                # If no process is currently running, pick the next shortest one
                if not current_process and heap:
                    burst_left, current_index, current_process = heapq.heappop(heap)
                    start_time = self.current_time
                    process_idx = int(current_process["id"][1:]) - 1
                    self.get_response_time(process_idx, current_process["arrival"])

                # If CPU is idle 
                if not current_process:
                    if i < self.num_processes:  # If there are still processes to arrive
                        next_arrival = processes_copy[i]["arrival"]
                        self.timeline.append({
                            "id": "idle",
                            "start": self.current_time,
                            "finish": next_arrival
                        })
                        self.current_time = next_arrival
                    else:
                        # This should not happen in a valid input set
                        break
                    continue

                # Execute one unit of the current process
                remaining_burst[current_index] -= 1
                self.current_time += 1

                # If the process finishes
                if remaining_burst[current_index] == 0:
                    self.timeline.append({
                        "id": current_process["id"],
                        "start": start_time,
                        "finish": self.current_time
                    })
                    process_idx = int(current_process["id"][1:]) - 1
                    self.turnaround_time[process_idx] = self.current_time - current_process["arrival"]
                    self.waiting_time[process_idx] = self.turnaround_time[process_idx] - processes_copy[process_idx]["burst"]
                    self.completed.append(processes_copy[process_idx])
                    current_process = None
                    completed_count += 1

            self.show_stats("Preemptive-SJF")
