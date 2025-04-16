from schdulers.FcfsScheduler import FcfsScheduler
from schdulers.PriorityScheduler import PriorityScheduler
from schdulers.SfjPreScheduler import SfjPreScheduler
from schdulers.SjfScheduler import SjfScheduler

while True:
    print("====CPU SCHEDULER====")
    print("Choose an option:")
    print("1. FCFS Scheduler")
    print("2. Non-Preemptive-SJF Scheduler")
    print("3. Preemptive-SJF Scheduler")
    print("4. Priority Scheduler")

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
            sjf_pre = SfjPreScheduler()
            sjf_pre.run()
        except Exception as e:
            print(e)
            continue

    elif choice == "4":
        try:
            priority = PriorityScheduler()
            priority.run()
        except Exception as e:
            print(e)
            continue