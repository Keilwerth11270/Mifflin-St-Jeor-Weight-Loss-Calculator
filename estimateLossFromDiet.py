import matplotlib.pyplot as plt

def calculate_TDEE(sex: str, weight: float, height: float, age: int, activity_level: str) -> float:
    """
    Calculate the Total Daily Energy Expenditure (TDEE) using the Mifflin-St Jeor equation based on the individual's
    sex, weight, height, age, and activity level.

    Args:
    - sex (str): The gender of the individual, either 'male' or 'female'.
    - weight (float): The individual's weight in pounds.
    - height (float): The individual's height in inches.
    - age (int): The individual's age in years.
    - activity_level (str): The individual's level of daily activity, which can be one of the following options:
        'sedentary', 'lightly active', 'moderately active', 'very active', or 'extra active'.

    Returns:
    - float: The calculated TDEE.
    """
    if sex.lower() == 'male':
        BMR = (10 * weight / 2.2) + (6.25 * height * 2.54) - (5 * age) + 5
    else:
        BMR = (10 * weight / 2.2) + (6.25 * height * 2.54) - (5 * age) - 161

    activity_multipliers = {
        'sedentary': 1.2,
        'lightly active': 1.375,
        'moderately active': 1.55,
        'very active': 1.725,
        'extra active': 1.9
    }

    return BMR * activity_multipliers[activity_level]

def calculate_weight_loss(sex: str, start_weight: float, height: float, age: int, activity_level: str, daily_intake: float, days: int) -> list:
    """
    Calculate daily weight loss based on the individual's TDEE, recalculating it daily to account for the updated weight,
    and return a list of weights for each day of the simulation.

    Args:
    - sex (str): The gender of the individual, either 'male' or 'female'.
    - start_weight (float): The individual's starting weight in pounds.
    - height (float): The individual's height in inches.
    - age (int): The individual's age in years.
    - activity_level (str): The individual's level of daily activity.
    - daily_intake (float): The individual's daily caloric intake.
    - days (int): The number of days for which the weight loss is to be simulated.

    Returns:
    - list: A list of weights for each day of the simulation.
    """
    weight_records = [start_weight]
    for day in range(1, days + 1):
        current_weight = weight_records[-1]
        TDEE = calculate_TDEE(sex, current_weight, height, age, activity_level)
        daily_deficit = TDEE - daily_intake
        daily_loss = daily_deficit / 3500
        new_weight = max(0, current_weight - daily_loss)  # Ensure weight doesn't go negative
        weight_records.append(new_weight)
    return weight_records

def plot_weight_loss(weight_records: list, days: int):
    """
    Plot the trend of weight loss over the specified number of days using matplotlib.

    Args:
    - weight_records (list): A list containing the weight of the individual for each day.
    - days (int): The total number of days for which the simulation was run.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, days + 2), weight_records, marker='o', linestyle='-', color='blue')
    plt.title('Weight Loss Trend over Time')
    plt.xlabel('Day')
    plt.ylabel('Weight (lbs)')
    plt.grid(True)
    plt.show()

def get_input(prompt: str, input_type: type, min_value=None, custom_error_message=None) -> float:
    """
    Prompt the user for input, convert it to a specified type, and ensure it meets a minimum value criterion.

    Args:
    - prompt (str): The question or statement to display to the user.
    - input_type (type): The data type to which the user's input should be converted.
    - min_value (float|int, optional): The minimum value that the user's input must exceed.
    - custom_error_message (str, optional): A custom error message to display if the input does not meet the criteria.

    Returns:
    - float|int: The user's input, converted to the specified type, and validated against the minimum value.
    """
    while True:
        try:
            user_input = input_type(input(prompt))
            if min_value is not None and user_input <= min_value:
                error_message = custom_error_message if custom_error_message else f"Please enter a value greater than {min_value}."
                raise ValueError(error_message)
            return user_input
        except ValueError as e:
            print(e)

def get_user_info() -> tuple:
    """
    Interactively collect information from the user necessary for TDEE calculation and weight loss simulation.

    This function validates the input for each parameter, ensuring logical values are entered. For age, height,
    and starting weight, it enforces minimum values of 15 years, 48 inches, and 90 pounds, respectively, to ensure
    realistic and safe parameters for the simulation.

    Returns:
    - tuple: A collection of all user-provided information, including sex, age, height, starting weight, activity level,
             daily caloric intake, and the number of days for the simulation.
    """
    sex = get_input("Enter your gender (male/female): ", str, None).lower()
    while sex not in ['male', 'female']:
        print("Please choose 'male' or 'female'.")
        sex = get_input("Enter your gender (male/female): ", str, None).lower()
    age = get_input("Enter your age: ", int, 14, "Age should be more than 14.")
    height = get_input("Enter your height (in inches): ", float, 47.9, "Height should be more than 48 inches.")
    start_weight = get_input("Enter your starting weight (in lbs): ", float, 89.9, "Weight should be more than 90 pounds.")
    activity_level = get_input("Enter your activity level (sedentary, lightly active, moderately active, very active, extra active): ", str, None).lower()
    while activity_level not in ['sedentary', 'lightly active', 'moderately active', 'very active', 'extra active']:
        print("Please choose a valid activity level.")
        activity_level = get_input("Enter your activity level (sedentary, lightly active, moderately active, very active, extra active): ", str, None).lower()
    daily_intake = get_input("Enter your daily caloric intake: ", int, -1, "Daily caloric intake should be a positive number.")
    days = get_input("Enter the number of days: ", int, 0, "Number of days should be more than 0.")

    return sex, age, height, start_weight, activity_level, daily_intake, days

def main():
    """
    The main function to execute the program's workflow, starting with gathering user information, calculating TDEE,
    simulating weight loss, and finally plotting the weight loss trend.
    """
    sex, age, height, start_weight, activity_level, daily_intake, days = get_user_info()
    weight_records = calculate_weight_loss(sex, start_weight, height, age, activity_level, daily_intake, days)
    final_weight = weight_records[-1]
    print(f"Your weight after {days} days will be approximately: {final_weight:.2f} lbs.")
    plot_weight_loss(weight_records, days)

if __name__ == "__main__":
    main()
