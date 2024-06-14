import matplotlib.pyplot as plt
from IPython.display import display, clear_output
import ipywidgets as widgets
from collections import deque
import time

class Truck:
    def __init__(self, truck_id, loading_time, arrival_time):
        self.truck_id = truck_id
        self.loading_time = loading_time
        self.remaining_loading_time = loading_time
        self.arrival_time = arrival_time
        self.departure_time = None

def round_robin_scheduling(trucks, time_frame, progress_bar):
    queue = deque(sorted(trucks, key=lambda truck: truck.arrival_time))  # Sort trucks by arrival time
    current_time = 0

    while queue:
        current_truck = queue.popleft()

        # Wait for the truck to arrive
        if current_truck.arrival_time > current_time:
            current_time = current_truck.arrival_time
            print(f"\nWaiting for Truck {current_truck.truck_id} to arrive at time {current_time}")

        # Load the truck for the specified time frame
        time_to_load = min(current_truck.remaining_loading_time, time_frame)
        current_truck.remaining_loading_time -= time_to_load
        current_time += time_to_load

        progress_bar.value = 100 - (current_truck.remaining_loading_time / current_truck.loading_time) * 100

        # Visualization using matplotlib
        plt.bar([f'Truck {i.truck_id}' for i in trucks], [i.remaining_loading_time for i in trucks], color='lightblue')
        plt.xlabel('Truck ID')
        plt.ylabel('Remaining Loading Time')
        plt.title('Truck Loading Simulation')
        plt.show()
        clear_output(wait=True)

        # Sleep for 30 seconds after each update
        time.sleep(20)

        print(f"\nLoaded Truck {current_truck.truck_id} for {time_to_load} units of time. Remaining loading time: {current_truck.remaining_loading_time}")

        if current_truck.remaining_loading_time == 0:
            current_truck.departure_time = current_time
            print(f"\nTruck {current_truck.truck_id} completely loaded and ready for departure at time {current_truck.departure_time}")
        else:
            # Time frame exhausted for this iteration, put the truck back in the queue
            queue.append(current_truck)
            print(f"\nTruck {current_truck.truck_id} partially loaded. Putting it back in the queue.")

    print("\nAll trucks loaded and departed.")

def run_simulation(num_trucks, time_frame):
    trucks = []

    for i in range(1, num_trucks + 1):
        loading_time = int(input(f"Enter loading time for Truck {i}: "))
        arrival_time = int(input(f"Enter arrival time for Truck {i}: "))
        trucks.append(Truck(i, loading_time, arrival_time))

    # Create a progress bar widget
    progress_bar = widgets.FloatProgress(
        value=0,
        min=0,
        max=100,
        description='Loading:',
        style={'bar_color': 'lightblue'}
    )

    # Display the progress bar
    display(progress_bar)

    round_robin_scheduling(trucks, time_frame, progress_bar)

# Get user input for simulation
num_trucks = int(input("Enter the number of trucks: "))
time_frame = int(input("Enter the time frame for loading: "))

# Run the simulation
run_simulation(num_trucks, time_frame)