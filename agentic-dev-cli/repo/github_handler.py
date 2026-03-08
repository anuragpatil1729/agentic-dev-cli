import re


def extract_github_url(text):

    match = re.search(r"https://github.com/[^\s]+", text)

    if match:
        return match.group()

    return None


def get_repo_name(url):

    repo = url.split("/")[-1]

    repo = repo.replace(".git", "")

    return repo