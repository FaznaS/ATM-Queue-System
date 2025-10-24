import random
import simpy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

RANDOM_SEED = 42
SIM_TIME = 180            # Simulation time in minutes (3 hours)

random.seed(RANDOM_SEED)

# AVG_SERVICE_TIME - Average service time per customer in minutes
# INTER_ARRIVAL_MEAN - Mean time between customer arrivals in minutes

scenarios = [
    {"NAME": "Base Case", "NUM_ATMS": 1, "AVG_SERVICE_TIME": 3, "INTER_ARRIVAL_MEAN": 4},
    {"NAME": "Increased ATMs", "NUM_ATMS": 2, "AVG_SERVICE_TIME": 3, "INTER_ARRIVAL_MEAN": 4},
    {"NAME": "More Customers", "NUM_ATMS": 2, "AVG_SERVICE_TIME": 3, "INTER_ARRIVAL_MEAN": 3},
]

# To store results of each scenario
results = []

class ATMQueueSimulation:
    # Initialize the ATM queue simulation with the number of ATMs and average service time
    def __init__(self, env, num_atms, avg_service_time):
        self.env = env
        self.num_atms = simpy.Resource(env, num_atms)
        self.avg_service_time = avg_service_time

    # Simulate the service time for a customer at the ATM 
    # The service time is randomly generated based on a normal distribution but is at least 2 minutes
    def service_customer(self, customer):
        random_service_time = max(2, np.random.normal(self.avg_service_time, 5))
        yield self.env.timeout(random_service_time)

def customer(env, name, atm, wait_times, customers_handled):
    arrival_time = env.now

    # Customer arrives and requests service at the ATM
    # If the ATM is busy, the customer waits in the queue until the ATM is free
    with atm.num_atms.request() as request:
        yield request
        
        # Record wait time
        wait_time = env.now - arrival_time
        wait_times.append(wait_time)

        # Service the customer
        yield env.process(atm.service_customer(name))
        customers_handled[0] += 1

def setup(env, num_atms, service_time, inter_arrival_mean, wait_times, queue_lengths, customers_handled):
    # Create the ATM queue simulation
    atm = ATMQueueSimulation(env, num_atms, service_time)
    customer_id = 0

    # Generate customers arriving at the ATM
    while True:
        yield env.timeout(random.expovariate(1.0 / inter_arrival_mean))
        customer_id += 1
        env.process(customer(env, customer_id, atm, wait_times, customers_handled))
        queue_lengths.append(len(atm.num_atms.queue))

# ------------  Set up and start the simulation ------------ 
def run_simulation(scenario):
    env = simpy.Environment()
    wait_times = []
    queue_lengths = []
    customers_handled = [0]

    # Start the setup process for the ATM queue simulation and run until SIM_TIME
    env.process(setup(env, scenario["NUM_ATMS"], scenario["AVG_SERVICE_TIME"], scenario["INTER_ARRIVAL_MEAN"], wait_times, queue_lengths, customers_handled))
    env.run(until=SIM_TIME)

    return {
        "Scenario": scenario["NAME"],
        "Number of ATMs": scenario["NUM_ATMS"],
        "Average Service Time": scenario["AVG_SERVICE_TIME"],
        "Inter-arrival Mean": scenario["INTER_ARRIVAL_MEAN"],
        "Total Customers Handled": customers_handled[0],
        "Average Wait Time": np.mean(wait_times) if wait_times else 0,
        "Average Queue Length": np.mean(queue_lengths) if queue_lengths else 0,
        "ATM Utilization (%)": ((customers_handled[0] * scenario["AVG_SERVICE_TIME"]) / (scenario["NUM_ATMS"] * SIM_TIME)) * 100,
        "Wait Times": wait_times
    }

# ------------  Run simulations for all scenarios ------------ 
for s in scenarios:
    result = run_simulation(s)
    results.append(result)

# ------------ Print results ------------ 
df = pd.DataFrame([results[i] for i in range(len(results))], columns=[
    "Scenario", "Number of ATMs", "Average Service Time", "Inter-arrival Mean", 
    "Total Customers Handled", "Average Wait Time", "Average Queue Length", "ATM Utilization (%)"])
print(df.to_string(index=False))

# ------------ Plotting results ------------ 

# Wait Time Distribution
plt.figure(figsize=(8, 5))
for result in results:
    plt.plot(result["Wait Times"], label=result["Scenario"])
plt.title('Wait Time of Customers over Simulation Time')
plt.xlabel('Customer')
plt.ylabel('Wait Time (minutes)')
plt.legend()
plt.show()

# Queue Length Comparison
plt.figure(figsize=(8, 5))
plt.bar(df["Scenario"], df["Average Queue Length"], color='salmon')
plt.title('Average Queue Length by Scenario')
plt.xlabel('Scenario')
plt.ylabel('Average Queue Length (customers)')
plt.show()

# Customers Handled Comparison
plt.figure(figsize=(8, 5))
plt.bar(df["Scenario"], df["Total Customers Handled"], color='lightgreen')
plt.title('Total Customers Handled by Scenario')
plt.xlabel('Scenario')
plt.ylabel('Total Customers Handled')
plt.show()