import urllib.request
import json
import time
import sys

url = 'https://api.github.com/repos/ne9n/circlemasters/actions/runs/31176826608/jobs'
for _ in range(30):
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read())
            all_completed = True
            for job in data.get('jobs', []):
                print(f"Job: {job['name']}, Status: {job['status']}, Conclusion: {job['conclusion']}")
                if job['status'] != 'completed':
                    all_completed = False
            
            if all_completed:
                print("All jobs completed!")
                sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        
    time.sleep(5)
print("Timeout waiting for jobs to complete.")
