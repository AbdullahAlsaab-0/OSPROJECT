from schdulers.FcfsScheduler import FcfsScheduler
from schdulers.PriorityScheduler import PriorityScheduler
from schdulers.SjfScheduler import SjfScheduler

while True:
    print("====CPU SCHEDULER====")
    print("Choose an option:")
    print("1. FCFS Scheduler")
    print("2. SJF Scheduler")
    print("3. Priority Scheduler")

    choice = input("Your choice is: ")
    print()

    if choice == "1":
        try:
            fcfs = FcfsScheduler()
            fcfs.run()
        except Exception as e:
            print(e)
            continue

    elif choice == "2":
        try:
            sjf = SjfScheduler()
            sjf.run()
        except Exception as e:
            print(e)
            continue

    elif choice == "3":
        try:
            priority = PriorityScheduler()
            priority.run()
        except Exception as e:
            print(e)
            continue