import requests
r = requests.get('https://api.github.com/repos/ne9n/circlemasters/actions/runs').json()
jobs_url = r['workflow_runs'][0]['jobs_url']
jobs = requests.get(jobs_url).json()
for j in jobs['jobs']:
    print(f"{j['name']} - {j['status']} - {j['conclusion']}")
