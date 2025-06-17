import random
from datetime import datetime, timedelta
import json

cities = ["Goa", "Shimla", "Jaipur", "Darjeeling", "Kerela", "Delhi", "Indore"]
train_names = ["Shatabdi Express", "Rajdhani Express", "Special Train", "Vande Bharat"]
start_date = datetime(2025, 6, 17)
num_days = 7
train_classes = [
    {"name": "AC Chair Car", "fare_range": (1000, 1500)},
    {"name": "AC 2 Tier", "fare_range": (1500, 2500)},
    {"name": "AC 3 Tier", "fare_range": (800, 1200)},
    {"name": "Sleeper", "fare_range": (500, 800)}
]

trains = []
train_number = 12045  # Starting train number

for day in range(num_days):
    current_date = start_date + timedelta(days=day)
    for origin in cities:
        for destination in cities:
            if origin != destination:
                # Generate 1-2 trains per route per day
                for _ in range(random.randint(1, 2)):
                    dep_hour = random.randint(5, 23)
                    dep_minute = random.choice([0, 15, 30, 45])
                    departure = current_date.replace(hour=dep_hour, minute=dep_minute)
                    
                    # Generate duration (1-40 hours)
                    duration_hours = random.randint(1, 40)
                    duration_mins = random.choice([0, 15, 30, 45])
                    arrival = departure + timedelta(hours=duration_hours, minutes=duration_mins)
                    
                    # Format travel time
                    travel_time = f"{duration_hours}h {duration_mins:02d}m"
                    
                    # Generate classes with random availability and fares
                    selected_classes = random.sample(train_classes, k=random.randint(1, 3))
                    classes = []
                    for cls in selected_classes:
                        classes.append({
                            "name": cls["name"],
                            "available": random.randint(10, 100),
                            "fare": random.randint(*cls["fare_range"])
                        })

                    trains.append({
                        "train_number": str(train_number),
                        "train_name": random.choice(train_names),
                        "from": origin,
                        "to": destination,
                        "departure": departure.strftime("%Y-%m-%dT%H:%M:%S"),
                        "arrival": arrival.strftime("%Y-%m-%dT%H:%M:%S"),
                        "travel_time": travel_time,
                        "classes": classes
                    })
                    train_number += 10  # Increment train number by 10 for uniqueness

# Save to JSON file
with open("trains.json", "w") as f:
    json.dump({"trains": trains}, f, indent=2)

print("Train data generated successfully in trains.json")
