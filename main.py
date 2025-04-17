from schedulers.FcfsScheduler import FcfsScheduler
from schedulers.PriorityScheduler import PriorityScheduler
from schedulers.RoundRobin import RoundRobin
from schedulers.SjfPreScheduler import SjfPreScheduler
from schedulers.SjfScheduler import SjfScheduler

def run_app():
    while True:
        print("====CPU SCHEDULER====")
        print("Choose an option:\n")
        print("1. FCFS Scheduler")
        print("2. Non-Preemptive-SJF Scheduler")
        print("3. Preemptive-SJF Scheduler")
        print("4. Priority Scheduler")
        print("5. Round-Robin Scheduler")
        print("6. Exit\n")

        try:
            choice = input("Your choice is: ")
        except KeyboardInterrupt:
            print("\nExiting...\n")
            break
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
                sjf_pre = SjfPreScheduler()
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
        elif choice == "5":
            try:
                rr = RoundRobin()
                rr.run()
            except Exception as e:
                print(e)
                continue
        elif choice == "6":
            print("Exiting...\n")
            break
        else:
            print("Invalid choice. Please try again.\n")
            continue


if __name__ == "__main__":
    try:
        run_app()
    except Exception:
        print("Failed to run app")