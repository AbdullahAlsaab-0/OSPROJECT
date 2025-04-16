from schdulers.FCFS_Scheduler import FCFSScheduler
from schdulers.SJF_Scheduler import SJFScheduler

while True:
    print("====CPU SCHEDULER====")
    print("Choose an option:")
    print("1. FCFS Scheduler")
    print("2. SJF Scheduler")

    choice = input("Your choice is: ")
    print()

    if choice == "1":
        try:
            fcfs = FCFSScheduler()
            fcfs.run()
        except Exception as e:
            print(e)
            continue

    elif choice == "2":
        try:
            sjf = SJFScheduler()
            sjf.run()
        except Exception as e:
            print(e)
            continue