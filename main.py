import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def fuzzy_fan_control(temp_value):
    """
    Given a temperature value, determine the fan speed using fuzzy logic.
    """

    # 1. Define fuzzy variables (Antecedent(s) and Consequent(s))

    # Temperature can range from 0 to 40 °C
    temperature = ctrl.Antecedent(np.arange(0, 41, 1), 'temperature')

    # Fan speed can range from 0 to 100 %
    fan_speed = ctrl.Consequent(np.arange(0, 101, 1), 'fan_speed')

    # 2. Define fuzzy membership functions for Temperature

    # We'll use trapezoidal or triangular membership functions for simplicity
    temperature['cold'] = fuzz.trapmf(temperature.universe, [0, 0, 10, 15])
    temperature['warm'] = fuzz.trimf(temperature.universe, [10, 20, 30])
    temperature['hot']  = fuzz.trapmf(temperature.universe, [25, 30, 40, 40])

    # 3. Define fuzzy membership functions for Fan Speed
    fan_speed['low']    = fuzz.trapmf(fan_speed.universe, [0, 0, 30, 40])
    fan_speed['medium'] = fuzz.trimf(fan_speed.universe, [30, 50, 70])
    fan_speed['high']   = fuzz.trapmf(fan_speed.universe, [60, 70, 100, 100])

    # 4. Define the rules
    #
    # - If temperature is cold, then fan_speed is low
    # - If temperature is warm, then fan_speed is medium
    # - If temperature is hot,  then fan_speed is high

    rule1 = ctrl.Rule(temperature['cold'], fan_speed['low'])
    rule2 = ctrl.Rule(temperature['warm'], fan_speed['medium'])
    rule3 = ctrl.Rule(temperature['hot'],  fan_speed['high'])

    # 5. Build the control system
    fan_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
    fan = ctrl.ControlSystemSimulation(fan_ctrl)

    # 6. Pass the input (temperature value) to the control system
    fan.input['temperature'] = temp_value

    # 7. Compute the result
    fan.compute()

    # Return the crisp output value
    return fan.output['fan_speed']

def main():
    # Example usage:
    while True:
        # Prompt user for a temperature value
        user_input = input("Enter temperature value (0-40 °C), or 'q' to quit: ")
        if user_input.lower() == 'q':
            print("Exiting program.")
            break
        
        try:
            temp_value = float(user_input)
            if not (0 <= temp_value <= 40):
                print("Please enter a temperature between 0 and 40.")
                continue

            # Get the fuzzy logic fan speed
            speed = fuzzy_fan_control(temp_value)

            # Print the result
            print(f"Temperature: {temp_value} °C => Fan Speed: {speed:.2f}%")

        except ValueError:
            print("Invalid input. Please enter a number between 0 and 40, or 'q' to quit.")

if __name__ == "__main__":
    main()
