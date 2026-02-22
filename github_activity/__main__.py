# Copyright (c) 2026 nguyenkevin-dotcom
#
# -*- coding:utf-8 -*-
# @Script: __main__.py
# @Author: nguyenkevin-dotcom
# @Email: nguk0907@gmail.com
# @Create At: 2026-02-19 16:42:32
# @Last Modified By: nguyenkevin-dotcom
# @Last Modified At: 2026-02-22 12:49:18
# @Description: This is description.

import argparse
from github_activity.github_user_activity import Datas

def main():
    
    github_activity = argparse.ArgumentParser(prog = "Github User Activity", description = "Github User Activity CLI program", epilog = "Example: github-activity <username>")
    github_activity.add_argument("username", type = str, help = "username of github.com")

    args = github_activity.parse_args()

    data = Datas()

    data.get_url(args.username)
    data.fetch_data()
    
    informations = data.read_data()

    repo_name = []
    repo_count = {}
    for event in informations:
            if event["type"] == "DeleteEvent":
                repo_name.append(f"{event['type']}:{event['payload']['ref_type']}:{event['payload']['ref']}:{event['repo']['name']}")
            else:
                repo_name.append(f"{event['type']}:{event['repo']['name']}")
    repo_name.sort()    
    for i in repo_name:
            repo_count[i] = repo_count.get(i, 0) + 1
    print(repo_count)
    for repo, count in repo_count.items():
            repo = repo.split(":")
            name = repo[-1]
            if "PushEvent" in repo:
                print(f"- Pushed {count} commits to {name}")
            elif "WatchEvent" in repo:
                print(f"- Starred {name}")
            elif "DeleteEvent" in repo:
                print(f"- Deleted {repo[1]} '{repo[2]}' from {name}")
            elif "CreateEvent" in repo:
                print(f"- Created a new repository {name}")
if __name__ == "__main__":
    main()