import os
import requests
from datetime import datetime


def get_today_datetime_filter():
    today = datetime.now()
    start_of_today = today.replace(hour=0, minute=0, second=0, microsecond=0)
    return start_of_today.isoformat() + 'Z'


def get_updated_issues(token, repo):
    url = f'https://api.github.com/repos/{repo}/issues'
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github.v3+json',
    }
    params = {'since': get_today_datetime_filter()}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        print(f'{response.status_code}, {response.json()}')
        return False, [f'{response.status_code}, {response.json()}']

    issues = response.json()
    return True, [issue for issue in issues if 'pull_request' not in issue]


def main(args):
    if len(args) < 2:
        return 'Usage: value_github_issue.py <github-token> <repo>'
    token = args[0]
    if not token:
        from dotenv import load_dotenv
        load_dotenv()
        token = os.getenv('GITHUB_TOKEN')
    repo = args[1]
    format = f'#{{number}}: {{title}}'
    if len(args) > 2:
        format = args[2]
    is_ok, issues = get_updated_issues(token, repo)
    if not is_ok:
        return issues[0]
    result = ''
    for issue in issues:
        if result:
            result += '\n'
        result += format.replace('{{', '{').replace('}}', '}').format(**issue)
    return result
