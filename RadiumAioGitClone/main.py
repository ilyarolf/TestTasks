import asyncio
import gitп
from hashlib import sha256
import os

async def clone_repo(repo_url: str, repo_dir: str) -> None:
    """
    Asynchronously clones repositories
    :param repo_url: str
    :param repo_dir: str
    :return: None
    """
    try:
        await asyncio.to_thread(git.Repo.clone_from, repo_url, repo_dir)
    except git.exc.GitCommandError as e:
        print(e.stderr.split("'fatal:")[1][:-1])


def get_hashes(directory:str) -> bool:
    """
    Calculates hashes of all files in repositories in the directory
    :param directory: str
    :return: bool
    """
    try:
        for repo_dir in os.listdir(directory):
            if os.path.isdir(os.path.join(directory, repo_dir)):
                for root, dirs, files in os.walk(os.path.join(directory, repo_dir)):
                    for file in files:
                        file_path = os.path.join(root, file)
                        with open(file_path, 'rb') as f:
                            data = f.read()
                            hash = sha256(data)
                            print(f'{file_path}: {hash.hexdigest()}')
    except TypeError:
        print('Fix your directory, it must be a string.')

async def main() -> None:
    repositories_dir ='temp'
    repo_url = 'https://gitea.radium.group/radium/project-configuration'
    tasks = list()
    for i in range(3):
        tasks.append(asyncio.create_task(clone_repo(repo_url,
                                                    f'{repositories_dir}/repo_{i}')))
    await asyncio.wait(tasks)
    get_hashes(repositories_dir)


asyncio.run(main())