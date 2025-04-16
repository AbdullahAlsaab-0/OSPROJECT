import util


class Scheduler():
    def __init__(self, priority=False, interval=False):
        self.processes, self.num_processes = util.read_input_processes(priority, interval)
        self.waiting_time = [0] * self.num_processes
        self.turnaround_time = [0] * self.num_processes
        self.current_time = 0

    def __str__(self):
        return f"Number of processes = {self.num_processes}, processes = {self.processes}"

    # def read_processes(self, sort:str, priority:bool=False, interval:bool=False):
    #     self.processes, self.num_processes = util.read_input_processes(sort, priority, interval)