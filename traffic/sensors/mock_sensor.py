import requests
import random
import time

url = 'http://127.0.0.1:5000/api/traffic'

locations = ['Rasulgarh', 'Jaydev Vihar', 'Patia', 'Master Canteen']

while True:
    data = {
        "location": random.choice(locations),
        "vehicle_count": random.randint(5, 50),
        "avg_speed": round(random.uniform(10, 60), 2)
    }
    res = requests.post(url, json=data)
    print(res.json())
    time.sleep(5) 
