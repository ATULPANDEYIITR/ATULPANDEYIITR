import os
import requests

TOKEN = os.environ["GITHUB_TOKEN"]
USERNAME = os.environ["GITHUB_USERNAME"]

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json"
}

query = """
query($login: String!) {
  user(login: $login) {
    login
    name

    followers {
      totalCount
    }

    following {
      totalCount
    }

    repositories(
      first: 20
      ownerAffiliations: OWNER
      orderBy: {field: UPDATED_AT, direction: DESC}
    ) {
      totalCount

      nodes {
        name
        stargazerCount
        forkCount

        watchers {
          totalCount
        }

        defaultBranchRef {
          target {
            ... on Commit {
              history(first: 5) {
                nodes {
                  messageHeadline
                  committedDate
                  url
                }
              }
            }
          }
        }
      }
    }

    contributionsCollection {
      contributionCalendar {
        totalContributions

        weeks {
          contributionDays {
            contributionCount
            date
          }
        }
      }
    }

    pullRequests(first: 1) {
      totalCount
    }

    issues(first: 1) {
      totalCount
    }
  }
}
"""

response = requests.post(
    "https://api.github.com/graphql",
    json={
        "query": query,
        "variables": {
            "login": USERNAME
        }
    },
    headers=headers
)

response.raise_for_status()

data = response.json()

if "errors" in data:
    raise RuntimeError(data["errors"])

user = data["data"]["user"]

contributions = (
    user["contributionsCollection"]
    ["contributionCalendar"]
    ["totalContributions"]
)

print(f"GitHub activity data collected for {user['login']}")
print(f"Followers: {user['followers']['totalCount']}")
print(f"Following: {user['following']['totalCount']}")
print(f"Repositories: {user['repositories']['totalCount']}")
print(f"Pull Requests: {user['pullRequests']['totalCount']}")
print(f"Issues: {user['issues']['totalCount']}")
print(f"Contributions: {contributions}")

print("Dynamic GitHub activity data collected successfully.")
