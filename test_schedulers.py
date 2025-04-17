import copy
from schedulers.FcfsScheduler import FcfsScheduler
from schedulers.SjfScheduler import SjfScheduler
from schedulers.SjfPreScheduler import SjfPreScheduler
from schedulers.PriorityScheduler import PriorityScheduler
from schedulers.RoundRobin import RoundRobin
from schedulers.Scheduler import Scheduler
import util
import traceback


def mock_show_stats(self, name):
    print(f"\nTesting {name} Scheduler")


def mock_show_gantt_chart(self, algo):
    pass



original_show_stats = Scheduler.show_stats
original_show_gantt_chart = Scheduler.show_gantt_chart
original_read_input = util.read_input_processes


Scheduler.show_stats = mock_show_stats
Scheduler.show_gantt_chart = mock_show_gantt_chart

test_cases = [
    {
    # Different arrival times
        "processes": [
            {"id": "P1", "arrival": 0, "burst": 5, "priority": 1},
            {"id": "P2", "arrival": 1, "burst": 3, "priority": 2},
            {"id": "P3", "arrival": 2, "burst": 1, "priority": 3}
        ],
        "expected": {
            "FCFS": {
                "waiting": [0, 4, 6],
                "turnaround": [5, 7, 7],
                "response": [0, 4, 6]
            },
            "SJF": {
                "waiting": [0, 5, 3],
                "turnaround": [5, 8, 4],
                "response": [0, 5, 3]
            },
            "SJF-Pre": {
                "waiting": [4, 1, 0],
                "turnaround": [9, 4, 1],
                "response": [0, 0, 0]
            },
            "Priority": {
                "waiting": [0, 4, 6],
                "turnaround": [5, 7, 7],
                "response": [0, 4, 6]
            },
            "Round-Robin": {
                "waiting": [4, 4, 2],
                "turnaround": [9, 7, 3],
                "response": [0, 1, 2]
            }

        }
    },

    {
    # Same arrival times
        "processes": [
            {"id": "P1", "arrival": 0, "burst": 6, "priority": 3},
            {"id": "P2", "arrival": 0, "burst": 8, "priority": 1},
            {"id": "P3", "arrival": 0, "burst": 7, "priority": 2}
        ],
        "expected": {
            "FCFS": {
                "waiting": [0, 6, 14],
                "turnaround": [6, 14, 21],
                "response": [0, 6, 14]
            },
            "SJF": {
                "waiting": [0, 13, 6],
                "turnaround": [6, 21, 13],
                "response": [0, 13, 6]
            },
            "SJF-Pre": {
                "waiting": [0, 13, 6],
                "turnaround": [6, 21, 13],
                "response": [0, 13, 6]
            },
            "Priority": {
                "waiting": [15, 0, 8],
                "turnaround": [21, 8, 15],
                "response": [15, 0, 8]
            },
            "Round-Robin": {
                "waiting": [8, 12, 14],
                "turnaround": [14, 20, 21],
                "response": [0, 2, 4]
            }
        }
    },

    # Idle times
    {
        "processes": [
            {"id": "P1", "arrival": 0, "burst": 2, "priority": 2},
            {"id": "P2", "arrival": 5, "burst": 4, "priority": 1},
            {"id": "P3", "arrival": 7, "burst": 3, "priority": 3}
        ],
        "expected": {
            "FCFS": {
                "waiting": [0, 0, 2],
                "turnaround": [2, 4, 5],
                "response": [0, 0, 2]
            },
            "SJF": {
                "waiting": [0, 0, 2],
                "turnaround": [2, 4, 5],
                "response": [0, 0, 2]
            },
            "SJF-Pre": {
                "waiting": [0, 0, 2],
                "turnaround": [2, 4, 5],
                "response": [0, 0, 2]
            },
            "Priority": {
                "waiting": [0, 0, 2],
                "turnaround": [2, 4, 5],
                "response": [0, 0, 2]
            },
            "Round-Robin": {
                "waiting": [0, 2, 2],
                "turnaround": [2, 6, 5],
                "response": [0, 0, 0]
            }
        }
    }
]


mock_processes = None


def mock_read_input_processes(priority=False, interval=False):
    global mock_processes
    return copy.deepcopy(mock_processes), len(mock_processes), 2  # Set quantum/interval to 2



def run_tests():
    global mock_processes

    total_tests = 0
    passed_tests = 0

    for test_idx, test_case in enumerate(test_cases):
        print(f"\n{'=' * 50}")
        print(f"TEST CASE {test_idx + 1}")
        print(f"{'=' * 50}")

        mock_processes = test_case["processes"]

        try:
            fcfs = FcfsScheduler()
            fcfs.run()
            verify_results(fcfs, test_case["expected"]["FCFS"], "FCFS")
            passed_tests += 1
        except AssertionError as e:
            print(f"❌ FCFS Test Failed: {e}")
        total_tests += 1

        try:
            sjf = SjfScheduler()
            sjf.run()
            verify_results(sjf, test_case["expected"]["SJF"], "SJF")
            passed_tests += 1
        except AssertionError as e:
            print(f"❌ SJF Test Failed: {e}")
        total_tests += 1

        try:
            sjf_pre = SjfPreScheduler()
            sjf_pre.run()
            verify_results(sjf_pre, test_case["expected"]["SJF-Pre"], "SJF-Pre")
            passed_tests += 1
        except AssertionError as e:
            print(f"❌ SJF Preemptive Test Failed: {e}")
        total_tests += 1

        try:
            priority = PriorityScheduler()
            priority.run()
            verify_results(priority, test_case["expected"]["Priority"], "Priority")
            passed_tests += 1
        except AssertionError as e:
            print(f"❌ Priority Test Failed: {e}")
        total_tests += 1

        try:
            rr = RoundRobin()
            rr.run()
            verify_results(rr, test_case["expected"]["Round-Robin"], "Round-Robin")
            passed_tests += 1
        except AssertionError as e:
            print(f"❌ Round Robin Test Failed: {e}")
        total_tests += 1

    print(f"\n{'=' * 50}")
    print(f"TEST SUMMARY: {passed_tests}/{total_tests} tests passed")
    print(f"{'=' * 50}")

    Scheduler.show_stats = original_show_stats
    Scheduler.show_gantt_chart = original_show_gantt_chart
    util.read_input_processes = original_read_input


def verify_results(scheduler, expected, name):

    for i, expected_waiting in enumerate(expected["waiting"]):
        actual_waiting = scheduler.waiting_time[i]
        assert abs(actual_waiting - expected_waiting) < 0.001, \
            f"{name}: Process P{i + 1} waiting time mismatch. Expected {expected_waiting}, got {actual_waiting}"

    for i, expected_turnaround in enumerate(expected["turnaround"]):
        actual_turnaround = scheduler.turnaround_time[i]
        assert abs(actual_turnaround - expected_turnaround) < 0.001, \
            f"{name}: Process P{i + 1} turnaround time mismatch. Expected {expected_turnaround}, got {actual_turnaround}"

    for i, expected_response in enumerate(expected["response"]):
        actual_response = scheduler.response_time[i]
        assert abs(actual_response - expected_response) < 0.001, \
            f"{name}: Process P{i + 1} response time mismatch. Expected {expected_response}, got {actual_response}"

    print(f"✅ {name} Scheduler: All metrics match expected values")


if __name__ == "__main__":

    util.read_input_processes = mock_read_input_processes

    try:
        run_tests()
    except Exception as e:
        print(f"Test execution failed: {e}")

        traceback.print_exc()