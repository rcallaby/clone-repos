import os
import json
from subprocess import run

CONFIG_FILE = "config.json"

def save_config(data):
    """Save the configuration data to a JSON file."""
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_config():
    """Load the configuration data from a JSON file, if it exists."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}

def clone_repos(repos, base_dir):
    """Clone the specified repositories into the base directory."""
    os.makedirs(base_dir, exist_ok=True)
    for repo in repos:
        repo_name = repo.split("/")[-1].replace(".git", "")
        repo_path = os.path.join(base_dir, repo_name)
        if not os.path.exists(repo_path):
            print(f"Cloning {repo} into {repo_path}...")
            run(["git", "clone", repo, repo_path])
        else:
            print(f"{repo_name} already exists in {base_dir}. Skipping.")

def main():
    """Main function to load configuration and clone repositories."""
    config = load_config()

    base_dir = config.get("base_dir") or input("Enter base directory for cloning repos: ").strip()
    repos = config.get("repositories")

    if not repos:
        print("No repositories found in the configuration file.")
        repos = input("Enter the repository URLs to clone (comma-separated): ").strip().split(",")
        config["repositories"] = [repo.strip() for repo in repos]

    print(f"\nYou have specified {len(config['repositories'])} repositories to clone.")

    confirmation = input("Proceed with cloning? (y/n): ").strip().lower()
    if confirmation == "y":
        clone_repos(config["repositories"], base_dir)
        print("\nAll specified repositories have been cloned.")
    else:
        print("\nOperation cancelled.")

    # Save preferences
    config["base_dir"] = base_dir
    save_config(config)

if __name__ == "__main__":
    main()
