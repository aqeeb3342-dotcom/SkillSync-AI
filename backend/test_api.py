import requests

url = "http://127.0.0.1:5000/api/predict"

student = {
    "gender": "M",
    "ssc_p": 75,
    "ssc_b": "Central",
    "hsc_p": 72,
    "hsc_b": "Central",
    "hsc_s": "Science",
    "degree_p": 70,
    "degree_t": "Sci&Tech",
    "workex": "Yes",
    "etest_p": 75,
    "specialisation": "Mkt&Fin",
    "mba_p": 70
}

response = requests.post(url, json=student)

print("Status Code:", response.status_code)
print("Response:")
print(response.json())