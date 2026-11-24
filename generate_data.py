import pandas as pd
import random

# Generate realistic car data for the Indian market
car_models = [
    ("Maruti Suzuki Alto 800", "Hatchback", "Petrol", "Manual", 22.05, 354000, 5),
    ("Maruti Suzuki Swift", "Hatchback", "Petrol", "Manual", 23.20, 599000, 5),
    ("Maruti Suzuki Swift AMT", "Hatchback", "Petrol", "Automatic", 23.76, 750000, 5),
    ("Hyundai Grand i10 Nios", "Hatchback", "Petrol", "Manual", 20.7, 584000, 5),
    ("Tata Tiago", "Hatchback", "Petrol", "Manual", 19.01, 560000, 5),
    ("Tata Altroz", "Hatchback", "Diesel", "Manual", 23.64, 880000, 5),
    ("Hyundai i20", "Hatchback", "Petrol", "Automatic", 19.6, 850000, 5),
    ("Maruti Suzuki Baleno", "Hatchback", "Petrol", "Manual", 22.35, 661000, 5),
    
    ("Honda Amaze", "Sedan", "Petrol", "Manual", 18.6, 705000, 5),
    ("Maruti Suzuki Dzire", "Sedan", "Petrol", "Automatic", 22.61, 860000, 5),
    ("Hyundai Verna", "Sedan", "Petrol", "Manual", 18.6, 1096000, 5),
    ("Honda City", "Sedan", "Petrol", "Automatic", 18.4, 1360000, 5),
    ("Skoda Slavia", "Sedan", "Petrol", "Manual", 19.47, 1139000, 5),
    ("Volkswagen Virtus", "Sedan", "Petrol", "Automatic", 18.12, 1450000, 5),
    
    ("Tata Nexon", "SUV", "Petrol", "Manual", 17.33, 810000, 5),
    ("Tata Nexon EV", "SUV", "Electric", "Automatic", 0.0, 1449000, 5),
    ("Hyundai Venue", "SUV", "Petrol", "Automatic", 18.15, 1000000, 5),
    ("Kia Sonet", "SUV", "Diesel", "Automatic", 19.0, 1150000, 5),
    ("Maruti Suzuki Brezza", "SUV", "Petrol", "Manual", 20.15, 829000, 5),
    ("Mahindra XUV300", "SUV", "Diesel", "Manual", 20.0, 930000, 5),
    ("Hyundai Creta", "SUV", "Petrol", "Automatic", 16.8, 1500000, 5),
    ("Kia Seltos", "SUV", "Diesel", "Manual", 20.7, 1200000, 5),
    ("Mahindra Scorpio-N", "SUV", "Diesel", "Automatic", 15.0, 1800000, 7),
    ("Mahindra XUV700", "SUV", "Petrol", "Automatic", 13.0, 1950000, 7),
    ("Tata Harrier", "SUV", "Diesel", "Automatic", 14.6, 1900000, 5),
    ("Toyota Fortuner", "SUV", "Diesel", "Automatic", 10.0, 3500000, 7),
    
    ("Maruti Suzuki Ertiga", "MUV", "Petrol", "Manual", 20.51, 864000, 7),
    ("Kia Carens", "MUV", "Diesel", "Manual", 21.3, 1200000, 7),
    ("Toyota Innova Crysta", "MUV", "Diesel", "Manual", 12.0, 1999000, 7),
    ("Toyota Innova Hycross", "MUV", "Hybrid", "Automatic", 21.1, 2500000, 7),
]

data = []
for name, type_, fuel, transmission, mileage, price, seats in car_models:
    data.append({
        "name": name,
        "type": type_,
        "fuel": fuel,
        "transmission": transmission,
        "mileage": mileage,
        "price": price,
        "seats": seats
    })

df = pd.DataFrame(data)
df.to_csv("cars.csv", index=False)
print("cars.csv generated successfully.")
