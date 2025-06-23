import requests

def get_today_prayer_times(lat, lon):
    url = f"http://api.aladhan.com/v1/timings?latitude={lat}&longitude={lon}&method=2"
    response = requests.get(url)
    data = response.json()
    timings = data['data']['timings']
    result = "\n".join([f"{k}: {v}" for k, v in timings.items() if k in ['Fajr', 'Dhuhr', 'Asr', 'Maghrib', 'Isha']])
    return result