# CPU Scheduler Simulator

A Python-based simulation tool for visualizing and analyzing common CPU scheduling algorithms used in operating systems.

## Overview

This project implements five popular CPU scheduling algorithms:

1. First-Come-First-Serve (FCFS)
2. Shortest Job First (SJF) - Non-Preemptive
3. Shortest Job First (SJF) - Preemptive
4. Priority Scheduling
5. Round Robin Scheduling

Each algorithm calculates important metrics like waiting time, turnaround time, and response time, and visualizes the scheduling process through Gantt charts.

## Features

- Interactive command-line interface
- Input validation for process parameters
- Calculation of key performance metrics:
  - Waiting time: Time a process spends waiting in the ready queue
  - Turnaround time: Total time from arrival to completion
  - Response time: Time from arrival to first CPU execution
  - Average metrics across all processes
- Visual representation of process execution using Gantt charts
- Handling of processes with different arrival times
- Idle time visualization when CPU is not processing
- Context switch counting for Round Robin scheduling
- Comprehensive test suite to verify algorithm implementations:
