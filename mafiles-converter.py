# Copyright 2023 The OrangeBonnet <orangebonnets@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import glob
import os
from json import loads, dumps


def get_from_mafile(mafile: str, argument: str) -> str:
    with open(mafile, 'r', encoding='ISO-8859-1') as file:
        if argument in 'account_name':
            return loads(file.read()).get('account_name')
        elif argument in 'steam_id':
            return loads(file.read()).get('Session').get('SteamID')
        elif argument in 'shared_secret':
            return loads(file.read()).get('shared_secret')
        elif argument in 'identity_secret':
            return loads(file.read()).get('identity_secret')
        elif argument in 'all':
            return file.read()
        else:
            raise RuntimeError("Incorrect value!")


def create_name_file(mafile: str, name_type: str) -> str:
    if name_type in "account_name":
        return get_from_mafile(mafile, "account_name")
    elif name_type in "steam_id64":
        return get_from_mafile(mafile, "steam_id")
    elif name_type in "account_name_and_steam_id64":
        return f'{get_from_mafile(mafile, "account_name")} [{get_from_mafile(mafile, "steam_id")}]'


def create_data_save(mafile: str, data_type: str) -> str:
    if data_type in "all":
        return get_from_mafile(mafile, "all")
    elif data_type in "sha_ide":
        return dumps({'shared_secret': get_from_mafile(mafile, "shared_secret"),
                'identity_secret': get_from_mafile(mafile, "identity_secret")}, indent=4)
    elif data_type in "id_name_sha_ide":
        return dumps({"steam_id": get_from_mafile(mafile, "steam_id"),
                "account_name": get_from_mafile(mafile, "account_name"),
                "shared_secret": get_from_mafile(mafile, "shared_secret"),
                "identity_secret": get_from_mafile(mafile, "identity_secret")}, indent=4)


def convert(mafiles_path: str, name_type: str, extension_type: str,
            data_save_type: str, path_save_files: str):
    mafiles = glob.glob(mafiles_path + '/*.maFile')
    for mafile in mafiles:
        file_name = str(create_name_file(mafile, name_type)) + "." + extension_type
        file_data = create_data_save(mafile, data_save_type)
        with open(f'{path_save_files}\\{file_name}', 'w+') as file:
            file.write(file_data)
        print(f'[{mafiles.index(mafile) + 1}/{len(mafiles)}] Created a new file - {file_name}')
    return True


if __name__ == '__main__':
    while True:
        print('Specify the folder with your maFiles')
        mafiles_path = input()
        if glob.glob(f'{mafiles_path}/*.maFile'):
            break
        else:
            print('There are no ".maFile" files inside the directory')

    while True:
        print('What to use as filename?')

        print('1. SteamID64')
        print('2. Account name')
        print('3. Account name + SteamID64')
        choice_filename = input()
        if choice_filename in '1':
            choice_filename = "steam_id64"
            break
        elif choice_filename in '2':
            choice_filename = "account_name"
            break
        elif choice_filename in '3':
            choice_filename = "account_name_and_steam_id64"
            break
        else:
            print('Incorrect value!')

    while True:
        print('In what file extension to save?')
        print('1. maFile')
        print('2. json')
        print('3. txt')
        choice_extension = input()
        if choice_extension in '1':
            choice_extension = "maFile"
            break
        elif choice_extension in '2':
            choice_extension = "json"
            break
        elif choice_extension in '3':
            choice_extension = "txt"
            break
        else: print('Incorrect value!')

    while True:
        print('What to save in a file?')
        print('1. All')
        print('2. Shared secret + Identity Secret')
        print('3. SteamID64 + Account name + Shared secret + Identity Secret')
        choice_data_save = input()
        if choice_data_save in '1':
            choice_data_save = "all"
            break
        elif choice_data_save in '2':
            choice_data_save = "sha_ide"
            break
        elif choice_data_save in '3':
            choice_data_save = "id_name_sha_ide"
            break
        else: print('Incorrect value!')

    while True:
        print('Choose a path to save new files')
        path_save_files = input()
        try:
            if not glob.glob(path_save_files):
                os.mkdir(path_save_files)
            break
        except:
            print('Incorrect value!')

    try:
        convert(mafiles_path, choice_filename, choice_extension,
                choice_data_save, path_save_files)
    finally:
        print('Finished work!', end='\n\n')
        print('Press any key')
        input()
