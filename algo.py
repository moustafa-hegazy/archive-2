import pandas as pd

# Load the CSV files into dataframes
flights_df = pd.read_csv('flights.csv')
hotels_df = pd.read_csv('hotels.csv')
users_df = pd.read_csv('users.csv')

# Define a function to find the maximum number of attractions within the budget
def knapsack(user_data, budget, n):
    if n == 0 or budget == 0:
        return 0

    trip = user_data.iloc[n - 1]

    if trip['total_cost'] > budget:
        return knapsack(user_data, budget, n - 1)
    
    return max(
        trip['days'] + knapsack(user_data, budget - trip['total_cost'], n - 1),
        knapsack(user_data, budget, n - 1)
    )

# Define a function to recommend cities based on the user's budget and the number of cities to visit
def recommend_cities(user_code, budget, num_cities):
    # Get user's flights and hotels data
    user_flights = flights_df[flights_df['userCode'] == user_code]
    user_hotels = hotels_df[hotels_df['userCode'] == user_code]
    
    # Merge flights and hotels data
    user_data = pd.merge(user_flights, user_hotels, on=['travelCode', 'userCode', 'date'])
    
    # Calculate the total cost of each trip
    user_data['total_cost'] = user_data['price_x'] + user_data['total']
    
    # Filter trips within the user's budget
    affordable_trips = user_data[user_data['total_cost'] <= budget]
    
    # Find the maximum number of attractions using dynamic programming
    max_attractions = knapsack(affordable_trips, budget, len(affordable_trips))

    # Sort trips by the number of attractions (days) in descending order
    sorted_trips = affordable_trips.sort_values(by='days', ascending=False)
    
    # Select the top N cities to visit
    recommended_cities = sorted_trips['place'].head(num_cities).tolist()

    # Print the maximum number of attractions
    print(f"Maximum number of attractions: {max_attractions}")
    
    return recommended_cities

# Use the function to get recommendations for a specific user
user_code = int(input("Enter user code: "))
budget = int(input("Enter budget: "))
num_cities = int(input("Enter number of cities to visit: "))

recommended_cities = recommend_cities(user_code, budget, num_cities)
print(recommended_cities)
