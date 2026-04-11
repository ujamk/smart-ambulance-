import random
import time
import os

def clear_screen():
    # Clear the terminal to keep the dashboard tidy
    os.system('cls' if os.name == 'nt' else 'clear')

def generate_patient_data():
    # Possible medical conditions
    conditions = [Broken Leg, Broken Arm, Chest Pain, Head Injury, Severe Burn]
    condition = random.choice(conditions)
    heart_rate = random.randint(60, 140)
    oxygen_level = random.randint(88, 100)

    # Set status based on vitals
    if heart_rate > 120 or oxygen_level < 92:
        status = Critical
    else:
        status = Stable

    return condition, heart_rate, oxygen_level, status

def display_dashboard():
    # Generate initial patient info
    condition, heart_rate, oxygen_level, status = generate_patient_data()

    try:
        while True:
            clear_screen()
            print(SMART AMBULANCE PATIENT MONITOR)
            print(-------------------------------)
            print(fCondition:    {condition})
            print(fHeart Rate:   {heart_rate} bpm)
            print(fOxygen Level: {oxygen_level} %)
            print(fStatus:       {status})
            print(-------------------------------)

            # Countdown before updating data
            for i in range(10, 0, -1):
                print(f\rNext update in {i} seconds..., end=)
                time.sleep(1)

            # Update data for next cycle
            condition, heart_rate, oxygen_level, status = generate_patient_data()

    except KeyboardInterrupt:
        print(\n\nMonitor stopped by user.)

if __name__ == __main__:
    display_dashboard()
