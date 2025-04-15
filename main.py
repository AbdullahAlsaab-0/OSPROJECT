from schdulers.FCFS_Scheduler import FCFS_Scheduler

fifo = FCFS_Scheduler()
fifo.read_processes()
print(fifo)
fifo.run()