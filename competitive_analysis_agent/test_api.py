import requests
import time
import sys

BASE_URL = "http://127.0.0.1:5000/api/v1"

def test_api():
    print("Testing API...")
    
    # 1. Check Status
    try:
        resp = requests.get(f"{BASE_URL}/status")
        print(f"Status Response: {resp.status_code}, {resp.json()}")
    except Exception as e:
        print(f"Failed to connect: {e}")
        return

    # 2. Trigger Analysis
    print("Triggering Analysis...")
    resp = requests.post(f"{BASE_URL}/analyze")
    print(f"Analyze Response: {resp.status_code}, {resp.json()}")
    
    if resp.status_code != 202:
        print("Failed to start analysis.")
        return

    # 3. Poll for completion
    for _ in range(10): 
        time.sleep(2)
        resp = requests.get(f"{BASE_URL}/status")
        data = resp.json()
        print(f"Polling Status: {data['status']}")
        if data['status'] == "Completed":
            print("Analysis Completed!")
            break
        if "Error" in data['status']:
            print(f"Analysis Failed: {data['status']}")
            break
    else:
        print("Timeout waiting for analysis.")

    # 4. Check Report
    if data['status'] == "Completed":
        print("Downloading Report...")
        resp = requests.get(f"{BASE_URL}/report/latest")
        if resp.status_code == 200:
            print(f"Report downloaded successfully. Size: {len(resp.content)} bytes")
        else:
            print(f"Failed to download report: {resp.status_code}")

if __name__ == "__main__":
    try:
        test_api()
    except Exception as e:
        print(f"Test crashed: {e}")
