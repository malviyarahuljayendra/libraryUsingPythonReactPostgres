import urllib.request
import json
import urllib.error

url = 'http://localhost:3001/api/members'
data = json.dumps({"name": "Duplicate Tester", "email": "duplicate@test.com"}).encode('utf-8')
headers = {'Content-Type': 'application/json'}

def create_member():
    req = urllib.request.Request(url, data=data, headers=headers, method='POST')
    try:
        with urllib.request.urlopen(req) as response:
            return response.status, response.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()

print("Attempt 1: Create Member")
status1, body1 = create_member()
print(f"Status: {status1}, Body: {body1}")

print("\nAttempt 2: Create Duplicate Member")
status2, body2 = create_member()
print(f"Status: {status2}, Body: {body2}")
if "Member with this email already exists" in body2:
    print("SUCCESS: Specific error message received.")
else:
    print("FAILURE: Specific error message NOT received.")
