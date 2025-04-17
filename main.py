from schedulers.FcfsScheduler import FcfsScheduler
from schedulers.PriorityScheduler import PriorityScheduler
from schedulers.RoundRobin import RoundRobin
from schedulers.SjfPreScheduler import SjfPreScheduler
from schedulers.SjfScheduler import SjfScheduler

def run_scheduler(scheduler_class):
    try:
        scheduler = scheduler_class()
        scheduler.run()
    except Exception as e:
        print(e)
        return False
    return True


def run_app():
    scheduler_map = {
        "1": FcfsScheduler,
        "2": SjfScheduler,
        "3": SjfPreScheduler,
        "4": PriorityScheduler,
        "5": RoundRobin
    }
    
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

        if choice in scheduler_map:
            run_scheduler(scheduler_map[choice])
        elif choice == "6":
            print("Exiting...\n")
            break
        else:
            print("Invalid choice. Please try again.\n")


if __name__ == "__main__":
    try:
        run_app()
    except Exception:
        print("Failed to run app")