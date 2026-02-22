# Copyright (c) 2026 nguyenkevin-dotcom
#
# -*- coding:utf-8 -*-
# @Script: __main__.py
# @Author: nguyenkevin-dotcom
# @Email: nguk0907@gmail.com
# @Create At: 2026-02-19 16:42:32
# @Last Modified By: nguyenkevin-dotcom
# @Last Modified At: 2026-02-23 00:58:54
# @Description: Here is the main function which is solving inputs on terminal.

import argparse
from github_activity.github_user_activity import Datas
import functools

@functools.cache
def main():
    
    # CLI settings
    github_activity = argparse.ArgumentParser(prog = "Github User Activity", description = "Github User Activity CLI program", epilog = "Example: github-activity <username>")
    github_activity.add_argument("username", type = str, help = "username of github.com")

    # Takes arguments in terminal
    args = github_activity.parse_args()

    # Call class Datas from github_user_activity.py
    data = Datas()

    # Get the url, for example: "https://api.github.com/users/nguyenkevin-dotcom/events" 
    # it takes the argument, which is a username of the user in github.com
    data.get_url(args.username)

    # Get data with urllib library. The output is data in JSON structure and at the same time 
    # it is being saved to the JSON file 
    # (if the name of JSON file is non-existent => it will create one)
    data.fetch_data()
    
    # Read the data from the JSON file
    informations = data.read_data()

    # If there is no data from JSON file
    if not informations:
        print(f"The username \033[1;92m{args.username}\033[0m has no \033[1;31mrecent activity\033[0m or \033[1;31mdoesn't exist\033[0m on \033[1mgithub.com\033[0m")
        return 
    
    # Create an empty table to get the customly-made informations from JSON file
    repo_name = []

    # Creating a dictionary to count the same action on the same repository
    repo_count = {}

    # Their purpose is for visual reasons => better appearance of output
    delimiters = ["/", "-"]

    # Checking what type of event it is => different values for each event, 
    # decided to divide each value by ':'
    for event in informations:
            type_event = event['type']
            repo = event['repo']['name']
            if event["type"] == "DeleteEvent":
                repo_name.append(f"{type_event}:{event['payload']['ref_type']}:{event['payload']['ref']}:{repo}")
            elif event["type"] == "ReleaseEvent":
                repo_name.append(f"{type_event}:{event['payload']['release']['tag_name']}:{repo}")
            elif event["type"] == "IssueCommentEvent":
                repo_name.append(f"{type_event}:{event['payload']['issue']['title']}:{repo}")
            elif event["type"] == "ForkEvent":
                repo_name.append(f"{type_event}:{event['payload']['forkee']['full_name']}:{repo}")
            else:
                # other Events
                repo_name.append(f"{type_event}:{repo}")
    
    # Sorting events by aplhabet for better readiness
    repo_name.sort()

    # Counting same event by repository's name
    for i in repo_name:
            repo_count[i] = repo_count.get(i, 0) + 1
    
    # Title of header
    title = f"Recent activity on \033[1mgithub.com\033[0m from \033[1;92m{args.username}\033[0m:"
    
    # Header of output
    print('-' * len(title))
    print(title)
    print('-' * len(title))

    # Transforming the data from the created list repo_name into output on terminal
    for repo, count in repo_count.items():
            
            # Split values by ":"
            repo = repo.split(":")
            # Set the repository as the last index in list
            name = "".join(f'\033[1;31m{repo[-1][i]}\033[0m' if repo[-1][i] in delimiters else f'\033[1m{repo[-1][i]}\033[0m' for i in range(len(repo[-1])))
            
            # Different outputs for each event, also adding colour for text 
            # (trying to make it resemble the output of the project in roadmap.sh)
            if "PushEvent" in repo:
                print(f"\033[1;31m-\033[0m Pushed \033[94m{count}\033[0m commit{'s' if count != 1 else ''} \033[31mto\033[0m {name}")
            elif "WatchEvent" in repo:
                print(f"\033[1;31m-\033[0m Starred {name}")
            elif "DeleteEvent" in repo:
                print(f"\033[1;31m-\033[0m Deleted {repo[1]} '\033[1;33m{repo[2]}\033[0m' \033[31min\033[0m {name}")
            elif "CreateEvent" in repo:
                print(f"\033[1;31m-\033[0m Created a \033[31mnew\033[0m repository {name}")
            elif "ReleaseEvent" in repo:
                print(f"\033[1;31m-\033[0m Released tag '\033[1;33m{repo[1]}\033[0m' \033[31min\033[0m {name}")
            elif "IssueCommentEvent" in repo:
                
                # Checking whether if the number of count is higher then 1 
                # => if yes print the number with its selected colour
                # else just print 'a'
                if count > 1:
                    count_event = f"\033[94m{count}\033[0m"
                else:
                    count_event = "a"

                print(f"\033[1;31m-\033[0m Created {count_event} comment{'s' if count > 1 else ''} \033[31mon\033[0m issue '\033[1;33m{repo[1]}\033[0m' \033[31min\033[0m {name}")
            elif "ForkEvent" in repo:
                forked_name = "".join(f'\033[1;31m{repo[1][i]}\033[0m' if repo[1][i] in delimiters else f'\033[1m{repo[1][i]}\033[0m' for i in range(len(repo[1])))
                print(f"\033[1;31m-\033[0m Forked {name} \033[31mto\033[0m {forked_name}")

if __name__ == "__main__":
    main()