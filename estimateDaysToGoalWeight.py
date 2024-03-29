from tabulate import tabulate

def calculate_TDEE(sex: str, weight: float, height: float, age: int, activity_level: str) -> float:
    """
    Calculate the Total Daily Energy Expenditure (TDEE) using the Mifflin-St Jeor equation.
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


def calculate_days_to_goal_weight(start_weight: float, goal_weight: float, sex: str, height: float, age: int, activity_level: str) -> list:
    """
    Calculates the number of days required to reach the goal weight.
    """
    scenarios = []
    initial_TDEE = calculate_TDEE(sex, start_weight, height, age, activity_level)

    # Adjust the calculation for daily calories as suggested
    daily_calories_scenarios = [initial_TDEE - i for i in range(0, int(initial_TDEE)+1, 500)] + [0]

    for daily_calories in daily_calories_scenarios:
        current_weight = start_weight
        days = 0

        while current_weight > goal_weight:
            TDEE = calculate_TDEE(sex, current_weight, height, age, activity_level)
            daily_deficit = TDEE - daily_calories
            if daily_deficit <= 0:  # Prevent infinite loops
                break

            daily_loss = daily_deficit / 3500  # Assuming 3500 calories per pound of body weight
            current_weight -= daily_loss
            days += 1

        if current_weight <= goal_weight:
            scenarios.append({'Daily Calorie Intake': int(daily_calories), 'Days to Goal': days})

    return scenarios


def get_input(prompt: str, input_type: type, min_value=None, custom_error_message=None) -> float:
    """
    Prompt the user for input, convert it to a specified type, and ensure it meets a minimum value criterion.
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
    """
    sex = get_input("Enter your gender (male/female): ", str).lower()
    age = get_input("Enter your age: ", int, 14, "Age should be more than 14.")
    height = get_input("Enter your height (in inches): ", float, 47.9, "Height should be more than 48 inches.")
    start_weight = get_input("Enter your starting weight (in lbs): ", float, 89.9, "Weight should be more than 90 pounds.")
    activity_level = get_input("Enter your activity level (sedentary, lightly active, moderately active, very active, extra active): ", str, None).lower()
    goal_weight = get_input("Enter goal weight (lbs): ", float, 0, "Goal weight should be a positive number.")
    return sex, age, height, start_weight, activity_level, goal_weight

def main():
    """
    Streamlined main function to gather user info and calculate days to goal weight.
    """
    sex, age, height, start_weight, activity_level, goal_weight = get_user_info()

    days_table = calculate_days_to_goal_weight(start_weight, goal_weight, sex, height, age, activity_level)
    print(tabulate(days_table, headers='keys', tablefmt='pretty', showindex=False))


if __name__ == "__main__":
    main()