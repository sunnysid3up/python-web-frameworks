import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import List
import requests


@dataclass
class Repo:
    name: str
    description: str
    url: str
    stars: str
    forks: str
    issues: str
    created_at: str
    updated_at: str


def main():
    result = []
    repos = file_read()
    headers = {
        "Authorization": f"token {os.environ.get('GTOKEN')}",
        "Content-Type": "application/json"
    }
    for repo in repos:
        url = "https://api.github.com/repos/" + repo
        resp = requests.get(url, headers=headers)
        status_code, body = resp.status_code, resp.json()
        if status_code != 200:
            print(f"{status_code} : {body}")
        else:
            result.append(format_body(body))
    file_write(sort_by_stars(result))
    return


def format_body(body):
    data = Repo(**{
        "name": body["name"],
        "description": body["description"],
        "url": body["html_url"],
        "stars": body["stargazers_count"],
        "forks": body["forks"],
        "issues": body["open_issues"],
        "created_at": body["created_at"],
        "updated_at": body["updated_at"]
    })
    print(data)
    return data


def sort_by_stars(repos: List[Repo]):
    def by_stars(elem):
        return elem.stars

    sorted_repos = sorted(repos, key=by_stars, reverse=True)
    print("Sorted repos.")
    return sorted_repos


def file_read():
    with open("repos.txt", "r") as reader:
        repos = reader.read().splitlines()
        print("Accessed repos.txt")
        return repos


def file_write(repos):
    with open("README.md", "w") as writer:
        body = f"""# Popular Python Web Frameworks \nA list of popular Python web frameworks ranked by the number of GitHub stars, automatically updated every week.\n\nLast update: {datetime.now(tz=timezone.utc).strftime("%m/%d/%Y, %H:%M:%S")} (UTC)

| Name          | Description          | Stars                     | Forks          | Issues               | First Commit        | Last Commit         |
|---------------|----------------------|---------------------------|----------------|----------------------|---------------------|---------------------|"""
        for repo in repos:
            body += f"\n| [{repo.name}]({repo.url}) | {repo.description.replace(' |', '.')} | {repo.stars} | {repo.forks} | {repo.issues} | {repo.created_at[:4]} | {repo.updated_at[:-10]} |"
        body += "\n\n## Contribute \n\nCreate an issue or pull request if you would like to add more frameworks :)"
        writer.write(body)

    print("Updated README.")


if __name__ == "__main__":
    main()
