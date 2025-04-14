from schdulers.FIFO_Scheduler import FIFO_Scheduler

fifo = FIFO_Scheduler()
fifo.read_processes()
print(fifo)
fifo.run()
fifo.show_stats()