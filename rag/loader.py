import subprocess
from pathlib import Path
from urllib.parse import urlparse


def clone_repo(url: str, destination: str = None) -> None:
    """
    Clones a GitHub repository into a specified destination folder. If the destination folder
    already exists and contains a valid git repository, it attempts to pull the latest changes.

    :param url: The URL of the GitHub repository to clone.
    :param destination: The destination path where the repository will be cloned. If None,
                        the repository will be cloned to a default location.
    :return: None
    """
    repo_name = Path(urlparse(url).path).stem

    base_path = Path("data") if destination is None else Path(destination)
    destination = (base_path / repo_name).resolve()

    if destination.exists() and (destination / ".git").exists():
        print(f"Repository exists at {destination}, pulling updates...")
        try:
            subprocess.run(["git", "-C", str(destination), "pull"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Pull failed: {e}")
    else:
        print(f"Cloning {url} into {destination}...")
        try:
            subprocess.run(["git", "clone", "--depth", "1", url, str(destination)], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Clone failed: {e}")
