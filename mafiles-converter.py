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
from json import loads


def get_from_mafile(mafile, argument):
    file = open(mafile, 'r', encoding='ISO-8859-1').read()
    if argument in 'account_name':
        return loads(file).get('account_name')
    elif argument in 'steam_id':
        return loads(file).get('Session').get('SteamID')
    elif argument in 'shared_secret':
        return loads(file).get('shared_secret')
    elif argument in 'identity_secret':
        return loads(file).get('identity_secret')
    elif argument in 'all':
        return file


def create_name_file(mafile, name_type):
    if name_type in "account_name":
        return get_from_mafile(mafile, "account_name")
    elif name_type in "steam_id64":
        return get_from_mafile(mafile, "steam_id")
    elif name_type in "account_name_and_steam_id64":
        return f'{get_from_mafile(mafile, "account_name")} [{get_from_mafile(mafile, "steam_id")}]'


def create_data_save(mafile, data_type):
    if data_type in "all":
        return get_from_mafile(mafile, "all")
    elif data_type in "sha_ide":
        return {'shared_secret': get_from_mafile(mafile, "shared_secret"),
                'identity_secret': get_from_mafile(mafile, "identity_secret")}
    elif data_type in "id_name_sha_ide":
        return {"steam_id": get_from_mafile(mafile, "steam_id"),
                "account_name": get_from_mafile(mafile, "account_name"),
                "shared_secret": get_from_mafile(mafile, "shared_secret"),
                "identity_secret": get_from_mafile(mafile, "identity_secret")}


def convert(path_mafiles, name_type, extension_type, data_save_type, path_save_files):
    mafiles = glob.glob(path_mafiles + '/*.maFile')
    for mafile in mafiles:
        file_name = str(create_name_file(mafile, name_type)) + "." + extension_type
        file_data = create_data_save(mafile, data_save_type)
        file = open(path_save_files + '\\' + file_name, 'w+')
        file.write(str(file_data))
        file.close()
        print(f'[{mafiles.index(mafile) + 1}/{len(mafiles)}] Created a new file - {file_name}')
    print('\nFinished work!')


if __name__ == '__main__':
    print('Specify the folder with your maFiles')
    path_mafiles = str(input())

    if glob.glob(path_mafiles + "/*.maFile"):
        print('What to use as filename?')

        print('1. SteamID64')
        print('2. Account name')
        print('3. Account name + SteamID64')
        choice_filename = int(input())
        if choice_filename == 1:
            choice_filename = "steam_id64"
        elif choice_filename == 2:
            choice_filename = "account_name"
        elif choice_filename == 3:
            choice_filename = "account_name_and_steam_id64"
        else: print('Incorrect value!')

        print('In what file extension to save?')
        print('1. maFile')
        print('2. json')
        print('3. txt')
        choice_extension = int(input())
        if choice_extension == 1:
            choice_extension = "maFile"
        elif choice_extension == 2:
            choice_extension = "json"
        elif choice_extension == 3:
            choice_extension = "txt"
        else: print('Incorrect value!')


        print('What to save in a file?')
        print('1. All')
        print('2. Shared secret + Identity Secret')
        print('3. SteamID64 + Account name + Shared secret + Identity Secret')
        choice_data_save = int(input())
        if choice_data_save == 1:
            choice_data_save = "all"
        elif choice_data_save == 2:
            choice_data_save = "sha_ide"
        elif choice_data_save == 3:
            choice_data_save = "id_name_sha_ide"
        else: print('Incorrect value!')

        print('Choose a path to save new files')
        path_save_files = str(input())
        if not glob.glob(path_save_files):
            os.mkdir(path_save_files)

        convert(path_mafiles, choice_filename, choice_data_save, choice_extension, path_save_files)

    else: print('There are no ".maFile" files inside the directory')

    print('\nPress any key')
    input()
