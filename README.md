# ATM Queue System

The ATM Queue System is a Python‐based simulation that models customers arriving at an ATM, waiting in a queue, being served, and leaving. The goal is to study queue behaviour under different parameter settings.
This simulation can be applied to study queueing systems, performance optimization, or customer service strategies in banking environments.

## 🚀 Getting Started

- Python 3.x (recommend version 3.6+)
- Install dependencies:
  ```bash
  pip install simpy numpy pandas matplotlib

- Clone the repository
  ```bash
  git clone https://github.com/FaznaS/ATM-Queue-System.git

## 🧠 How It Works
  1.	Each customer arrives at the ATM at random times
  2.	Each customer requests an ATM resource
  3.	If all ATMs are occupied, they wait in a queue
  4.	Use the ATM for a short time
  5.	Leave after finishing


## 📊 Simulation Scenarios Used
Three scenarios used for testing under a simulation time of 180 minutes:

| **Scenario**      | **Description** | **Number of ATMs** | **Average Service Time (min)** | **Mean Time Between Arrivals (min)** |
|--------------------|-----------------|--------------------|---------------------------------|--------------------------------------|
| Base Case          | Normal operation | 1 | 3 | 4 |
| Increased ATMs     | More ATMs to reduce waiting time | 2 | 3 | 4 |
| More Customers     | More customers to analyze ATM utilization | 2 | 3 | 3 |

## Output
Average waiting time, average queue length, ATM usage and the number of customers handled
| More Customers     | Higher customer arrival rate | 2 | 3 | 3 |

