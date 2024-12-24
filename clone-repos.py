import os
import json
from github import Github
from subprocess import run

CONFIG_FILE = "repo_clone_config.json"

def save_config(data):
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f)

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}

def get_github_repos(token):
    g = Github(token)
    user = g.get_user()
    return [repo for repo in user.get_repos()]

def clone_repos(repos, base_dir):
    os.makedirs(base_dir, exist_ok=True)
    os.chdir(base_dir)
    for repo in repos:
        if not os.path.exists(repo.name):
            print(f"Cloning {repo.name}...")
            run(["git", "clone", repo.ssh_url])
        else:
            print(f"{repo.name} already exists. Skipping.")

def main():
    config = load_config()
    
    token = config.get("token") or input("Enter your GitHub Personal Access Token: ").strip()
    base_dir = config.get("base_dir") or input("Enter base directory for cloning repos: ").strip()
    
    repos = get_github_repos(token)
    
    print("\nAvailable repositories:")
    for i, repo in enumerate(repos):
        print(f"{i + 1}. {repo.name}")
    
    saved_selection = config.get("selected_repos", [])
    selected_indices = (
        saved_selection 
        or input("\nEnter the numbers of repos to clone (comma-separated) or press Enter to select all: ").strip()
    )
    
    if not selected_indices:
        selected_repos = repos
    else:
        selected_indices = [int(i) - 1 for i in selected_indices.split(",")]
        selected_repos = [repos[i] for i in selected_indices]
    
    print(f"\nYou have selected {len(selected_repos)} repositories to clone.")
    confirmation = input("Proceed? (y/n): ").lower()
    if confirmation == "y":
        clone_repos(selected_repos, base_dir)
        print("\nAll selected repositories have been cloned.")
    else:
        print("\nOperation cancelled.")

    # Save preferences
    config["token"] = token
    config["base_dir"] = base_dir
    config["selected_repos"] = [repos.index(repo) + 1 for repo in selected_repos]
    save_config(config)

if __name__ == "__main__":
    main()
