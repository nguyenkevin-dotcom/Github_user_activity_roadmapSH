# Copyright (c) 2026 nguyenkevin-dotcom
#
# -*- coding:utf-8 -*-
# @Script: github_user_activity.py
# @Author: nguyenkevin-dotcom
# @Email: nguk0907@gmail.com
# @Create At: 2026-02-20 14:21:29
# @Last Modified By: nguyenkevin-dotcom
# @Last Modified At: 2026-02-23 00:56:33
# @Description: Getting data from GitHub API and the save them in JSON file 
# (if JSON file doesn't exist it will create one and
# the name of the file is based on variable 'file')

import urllib.request
import os
import stat
import json

class Datas:
    def __init__(self, file = "API_user_data.json"):
        self.file = file
        
    def get_url(self, username):
        """
        Get the url of user recent activity on github.com

        :param self.url: saving the information into class Datas
        :param username: The username of user on github.com
        """
        self.url = f"https://api.github.com/users/{username}/events"

    def fetch_data(self):
        """
        Get the data in JSON format by acquired url and at the same time being saved into JSON file.
        If JSON file doesn't exist it will create one

        :param self: description
        """
        try:
            with urllib.request.urlopen(self.url) as response:
                if response.status == 200:
                    raw_data = response.read().decode('UTF-8')
                    data = json.loads(raw_data)

                    # Check if file exists => change permission from read to write
                    if os.path.exists(self.file):
                        os.chmod(self.file, stat.S_IRUSR | stat.S_IWUSR)

                    # If file files exists => overwrites the existing data for new, If not
                    # then will create a new file
                    with open(self.file, "w", encoding = "UTF-8") as f:
                        json.dump(data, f, indent = 4, ensure_ascii = False)

                    # Changes permission from write to read
                    os.chmod(self.file, stat.S_IREAD)
                else:
                    print(f"Error!!: Status code {response.status}")
                    return 0
        except Exception as e:
            print(f"An error occurred: {e}")
            return 0

    def read_data(self):
        """
        Read a JSON file

        :param self: Description
        """
        # Check if there is file with a name that we set on variable file
        if not os.path.exists(self.file):
            return []
        # Reading JSON file
        with open(self.file, "r", encoding="UTF-8") as f:
            try:
                # file only with characters (no special characters)
                content = f.read().strip()
                if not content:
                    return []
                # return the items in JSON file
                return json.loads(content)
            except json.JSONDecodeError:
                return []
