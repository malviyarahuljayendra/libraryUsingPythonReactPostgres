import urllib.request
import json

try:
    print("Sending request to Gateway...")
    with urllib.request.urlopen('http://localhost:3001/api/books?limit=1') as response:
        print(f"Response Status: {response.status}")
        if response.status == 200:
            print("Success! detailed logs should be in backend container.")
        else:
            print(f"Failed: {response.read().decode('utf-8')}")
except Exception as e:
    print(f"Error: {e}")
