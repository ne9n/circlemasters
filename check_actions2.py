import urllib.request
import json

url = 'https://api.github.com/repos/ne9n/circlemasters/actions/runs'
try:
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read())
        for run in data.get('workflow_runs', [])[:10]:
            msg = run['head_commit']['message'].splitlines()[0] if run.get('head_commit') else 'No commit'
            print(f"ID: {run['id']}, Status: {run['status']}, Conclusion: {run['conclusion']}, Commit: {msg}")
except Exception as e:
    print(f"Error: {e}")
