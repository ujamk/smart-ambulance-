import random
import time
import os

def clear_screen():
    # Clear the terminal to keep the dashboard tidy
    os.system('cls' if os.name == 'nt' else 'clear')

def generate_patient_data():
    # FIXED: Added quotes to make these strings
    conditions = ["Broken Leg", "Broken Arm", "Chest Pain", "Head Injury", "Severe Burn"]
    condition = random.choice(conditions)
    heart_rate = random.randint(60, 140)
    oxygen_level = random.randint(88, 100)

    # FIXED: Added quotes to status values
    if heart_rate > 120 or oxygen_level < 92:
        status = "Critical"
    else:
        status = "Stable"

    return condition, heart_rate, oxygen_level, status

def display_dashboard():
    # Generate initial patient info
    condition, heart_rate, oxygen_level, status = generate_patient_data()

    try:
        while True:
            clear_screen()
            # FIXED: Added quotes and proper f-string formatting
            print("SMART AMBULANCE PATIENT MONITOR")
            print("-------------------------------")
            print(f"Condition:    {condition}")
            print(f"Heart Rate:   {heart_rate} bpm")
            print(f"Oxygen Level: {oxygen_level} %")
            print(f"Status:       {status}")
            print("-------------------------------")

            # Countdown before updating data
            for i in range(10, 0, -1):
                # FIXED: Added quotes and set end to an empty string
                print(f"\rNext update in {i} seconds...", end="")
                time.sleep(1)

            # Update data for next cycle
            condition, heart_rate, oxygen_level, status = generate_patient_data()

    except KeyboardInterrupt:
        # FIXED: Added quotes and proper newline character
        print("\n\nMonitor stopped by user.")

# FIXED: Added quotes around "__main__"
if __name__ == "__main__":
    display_dashboard()
