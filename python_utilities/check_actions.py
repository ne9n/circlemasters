import requests
r = requests.get('https://api.github.com/repos/ne9n/circlemasters/actions/runs').json()
runs = r.get('workflow_runs', [])
for run in runs[:3]:
    print(f"{run['name']} - {run['status']} - {run['conclusion']}")
