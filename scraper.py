import os
import requests
import zipfile
import io
from colorama import init, Fore, Style

init(autoreset=True)

username = 'Purv06'
dl_dir = 'DD-SCRAPE'

api_url = f'https://api.github.com/users/{username}/repos'

if not os.path.exists(dl_dir):
    os.makedirs(dl_dir)

def download_repo(repo_name, zip_url):
    print(f"{Fore.CYAN}Downloading repository: {repo_name}")
    
    response = requests.get(zip_url)
    if response.status_code == 200:
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
            zip_ref.extractall(os.path.join(dl_dir, repo_name))
        print(f"{Fore.GREEN}Repository {repo_name} downloaded successfully!\n")
    else:
        print(f"{Fore.RED}Failed to download {repo_name}. Status Code: {response.status_code}\n")

def select_repos(repos):
    print(f"\n{Fore.MAGENTA}Available repositories:")
    for i, repo in enumerate(repos):
        print(f"{Fore.YELLOW}{i+1}. {repo['name']}")

    selected_indices = input(f"\n{Fore.CYAN}Enter the numbers of the repositories you want to download, separated by commas eg. 1,2,3 : {Style.RESET_ALL}")

    selected_indices = [int(i.strip()) - 1 for i in selected_indices.split(',') if i.strip().isdigit()]

    return [repos[i] for i in selected_indices]

def fetch_all_repos(api_url):
    repos = []
    page = 1
    print(f"{Fore.BLUE}Fetching repositories ...\n")
    while True:
        response = requests.get(api_url, params={'page': page, 'per_page': 100})
        if response.status_code == 200:
            page_repos = response.json()
            if not page_repos:
                break
            repos.extend(page_repos)
            page += 1
        else:
            print(f"{Fore.RED}Failed to fetch repositories. Status Code: {response.status_code}")
            break
    return repos

repos = fetch_all_repos(api_url)

if repos:
    selected_repos = select_repos(repos)
    for repo in selected_repos:
        repo_name = repo['name']
        zip_url = f"https://github.com/{username}/{repo_name}/archive/refs/heads/main.zip"
        download_repo(repo_name, zip_url)
else:
    print(f"{Fore.RED}No public repositories found.")
