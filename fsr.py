#!/usr/bin/env python

from __future__ import print_function
from __future__ import with_statement

import __main__

import os
import sys
import shutil
import filecmp
import difflib
import stat
import datetime
import tarfile

from functools import partial


class Filters(object):
    """Helper class for managing main files."""

    FILE_LINKS = "links.txt"
    FILE_SCRIPT = "fsr.py"
    FILE_REPLICAS = "replicas.txt"
    FILE_IGNORE = "ignore.txt"

    IGNORE_LIST = [
        '2014-12-24-wheezy-raspbian.zip',
        #'2015-02-01-wheezy-raspbian-raspi01.zip',

    ]

    def in_ignore_list(self, script_path, filepath):
        """Verify if filepath is in ignore list."""

        script_directory_contents = os.listdir(script_path)

        if self.check_ignore_in_list(script_directory_contents):
            ignore_list = []
            with open(os.path.join(script_path, self.FILE_IGNORE)) as f:
                for x in f:
                    ignore_list.append(x.strip())
            return filepath in ignore_list

        return filepath in self.IGNORE_LIST

    def check_links_file(self, content):
        """Verify if content string is links file"""

        return self.FILE_LINKS == content

    def check_script_file(self, content):
        """Verify if content string is script file"""

        return self.FILE_SCRIPT == content

    def check_replicas_file(self, content):
        """Verify if content string is replica list file"""

        return self.FILE_REPLICAS == content

    def check_ignore_file(self, content):
        """Verify if content string is replica list file"""

        return self.FILE_IGNORE == content

    def check_links_in_list(self, directory_contents):
        """Verify if file list contains links file"""

        return self.FILE_LINKS in directory_contents

    def check_script_in_list(self, directory_contents):
        """Verify if file list contains script file"""

        return self.FILE_SCRIPT in directory_contents

    def check_replicas_in_list(self, directory_contents):
        """Verify if file list contains replica list file"""

        return self.FILE_REPLICAS in directory_contents

    def check_ignore_in_list(self, directory_contents):
        """Verify if file list contains ignore list file"""

        return self.FILE_IGNORE in directory_contents

    def check_in_replica(self, script_path, elements_list):
        """Verify if any replica path defined in elements_list is contained in the replica repository
        for the current script (script_path).
        """

        # Initialize result map
        retval = {}
        for element in elements_list:
            retval[element] = False

        # check
        with open(os.path.join(script_path, self.FILE_REPLICAS)) as f:
            for x in f:
                if x.strip() in elements_list:
                    retval[x.strip()] = True
                    
        return retval


class Utils(object):

    def create_dir(self, fulldirpath):
        os.mkdir(fulldirpath)

    def remove_empty_dir(self, fulldirpath):
        os.rmdir(fulldirpath)

    def dir_exists(self, fulldirpath):
        return os.path.isdir(fulldirpath)
        
    def read_file_list(self, path):
        elements_list = []
        with open(path) as f:
            for x in f:
                elements_list.append(x.strip())
                
        return elements_list
        
    def write_file_list(self, path, elements_list):
        with open(path, "w") as f:
            for x in elements_list:
                f.write("{}\n".format(x))


#
# Commands and operations
#


def generate_replicas_file(filters, script_path):

    text = "Replica list file will be generated. Only directory from current script will be added."

    print("\n{}".format(text))

    with open(os.path.join(script_path, filters.FILE_REPLICAS), "w") as f:
        print("File {} opened for writing.".format(filters.FILE_REPLICAS))
        f.write(script_path)


def generate_ignore_file(filters, script_path):

    text = "Ignore list file will be generated."

    print("\n{}".format(text))

    with open(os.path.join(script_path, filters.FILE_IGNORE), "w") as f:
        print("File {} opened for writing.".format(filters.FILE_IGNORE))


def show_replicas(filters, script_path):

    title = "Replica list"

    print("\n{}\n{}".format(title, "=" * len(title)))

    with open(os.path.join(script_path, filters.FILE_REPLICAS)) as f:
        content = f.readline()
        while content:
            if not os.path.isdir(content.strip()):
                print("{:60} -> path not found".format(content.strip()))
            elif content.strip() == script_path:
                print("{:60} -> current replica".format(content.strip()))
            else:
                print(content.strip())
            content = f.readline()


def add_replica(filters, script_path, new_path=None):

    utils = Utils()

    print()
    if not new_path:
        path = prompt("insert path: ")
    else:
        path = new_path

    if not os.path.isdir(path):
        print("error: {} does not exist".format(path))
    else:
        replica_list = utils.read_file_list(os.path.join(script_path, filters.FILE_REPLICAS))

        replica_list.append(path)

        for x in replica_list:
            print(x)

        utils.write_file_list(os.path.join(script_path, filters.FILE_REPLICAS), replica_list)


def diff_replica(filters, script_path):

    utils = Utils()

    replica_list = utils.read_file_list(os.path.join(script_path, filters.FILE_REPLICAS))

    available_replica_list = [replica for replica in replica_list if os.path.isdir(replica) and not replica == script_path]

    for x in available_replica_list:
        print("{}: {}".format(available_replica_list.index(x), x))
        
    val = ""
    if not val.isdigit():
        val = prompt("Select replica index to check differences or -1 to cancel: ")
        if val == "-1":
            return

    dest_path = available_replica_list[int(val)]

    # for x in os.listdir(dest_path):
    #     print(os.path.join(dest_path, x))
    #
    # print()
    #
    # for x in os.listdir(script_path):
    #     print(os.path.join(script_path, x))

    current_elems = set(os.listdir(script_path))
    replica_elems = set(os.listdir(dest_path))

    new_in_current = current_elems - replica_elems
    new_in_replica = replica_elems - current_elems

    if len(new_in_current) > 0:
        print("New in current [{}]:\n".format(script_path))
        for x in new_in_current:
            print("    {}".format(x))

    if len(new_in_replica) > 0:
        print("\nNew in replica [{}]:\n".format(dest_path))
        for x in new_in_replica:
            print("    {}".format(x))

    if sys.version_info.major > 2:
        filecmp.clear_cache()
    same_elements = current_elems & replica_elems
    for x in same_elements:
        if not filters.in_ignore_list(script_path, x):
            current_file_path = os.path.join(script_path, x)
            replica_file_path = os.path.join(dest_path, x)
            if not filecmp.cmp(current_file_path, replica_file_path):
                current_mt_timestamp = os.stat(current_file_path)[stat.ST_MTIME]
                replica_mt_timestamp = os.stat(replica_file_path)[stat.ST_MTIME]
                current_mt = datetime.datetime.fromtimestamp(current_mt_timestamp)
                replica_mt = datetime.datetime.fromtimestamp(replica_mt_timestamp)
                print("difference: {} current: {} replica: {}".format(x, current_mt, replica_mt))
                if current_mt_timestamp >= replica_mt_timestamp:
                    print("    current seems more recent")
                else:
                    print("    replica seems more recent")
        else:
            print("file {} is in ignore list, ignored.".format(x))

        
def sync_replica(filters, script_path):

    utils = Utils()
    
    replica_list = utils.read_file_list(os.path.join(script_path, filters.FILE_REPLICAS))
    
    available_replica_list = [replica for replica in replica_list if os.path.isdir(replica) and not replica == script_path]
    
    for x in available_replica_list:
        print("{}: {}".format(available_replica_list.index(x), x))
        
    val = ""
    if not val.isdigit():
        val = prompt("Select replica index to sync or -1 to cancel: ")
        if val == "-1":
            return
            
    dest_path = available_replica_list[int(val)]
    
    print("\nSyncing to: {}".format(dest_path))
    
    for x in os.listdir(dest_path):
        if not filters.in_ignore_list(script_path, x):
            current_file_path = os.path.join(script_path, x)
            replica_file_path = os.path.join(dest_path, x)
            if not filecmp.cmp(current_file_path, replica_file_path):
                os.remove(os.path.join(dest_path, x))
            else:
                print("file {} is same, ignored.".format(x))
        else:
            print("file {} is in ignore list, ignored.".format(x))
        
    for x in os.listdir(script_path):
        current_file_path = os.path.join(script_path, x)
        replica_file_path = os.path.join(dest_path, x)
        if os.path.isfile(os.path.join(script_path, x)):
            if os.path.isfile(replica_file_path):
                if not filters.in_ignore_list(script_path, x):
                    if not filecmp.cmp(current_file_path, replica_file_path):
                        shutil.copy(current_file_path, replica_file_path)
                    else:
                        print("file {} is same, ignored.".format(x))
                else:
                    print("file {} is in ignore list, ignored.".format(x))
            else:
                shutil.copy(current_file_path, replica_file_path)
                
def rem_replica(filters, script_path):

    utils = Utils()

    replica_list = utils.read_file_list(os.path.join(script_path, filters.FILE_REPLICAS))
            
    for x in replica_list:
        print("{}: {}".format(replica_list.index(x), x))
    
    val = ""
    if not val.isdigit():
        val = prompt("Select replica index to remove or -1 to cancel: ")
        if val == "-1":
            return
    
    replica_list.pop(int(val))
    
    utils.write_file_list(os.path.join(script_path, filters.FILE_REPLICAS), replica_list)


def show_links(script_path):

    filters = Filters()
    
    utils = Utils()

    title = "Contents of links"

    print("\n{}\n{}".format(title, "=" * len(title)))

    for x in utils.read_file_list(os.path.join(script_path, filters.FILE_LINKS)):
        print(x)


#
# Command management
#


def command_list_prompt(commands_list, list_prompt="Choose a command:"):

    print("\n{}\n{}\n".format(list_prompt, "=" * len(list_prompt)))
    for x in commands_list:
        print(x)


def prompt(text):
    if sys.version_info.major > 2:
        return input(text).strip()
    else:
        return raw_input(text).strip()


def command_prompt(text="> "):

    print()
    return prompt(text)


class CommandManager(object):

    def __init__(self, utils, filters, script_path):
        self.utils, self.filters, self.script_path = utils, filters, script_path
        self.replica_list_path = os.path.join(self.script_path, self.filters.FILE_REPLICAS)
        self.refresh_directory_contents()
        self.check()

    def refresh_directory_contents(self):
        self.script_directory_contents = os.listdir(self.script_path)

    def is_script_path_in_replica_list(self):
        return self.filters.check_in_replica(self.script_path, [self.script_path]).get(self.script_path)

    def is_replica_file_present(self):
        return self.filters.check_replicas_in_list(self.script_directory_contents)

    def is_links_file_present(self):
        return self.filters.check_links_in_list(self.script_directory_contents)

    def is_ignore_file_present(self):
        return self.filters.check_ignore_in_list(self.script_directory_contents)

    def verify_python_version(self):
        print("\nPython {} major version is used.".format(sys.version_info.major))

    def verify_links_presence(self):
        if not self.is_links_file_present():
            print("warning: script directory does not have links.txt file")

    def verify_replica_paths(self):
        with open(self.replica_list_path) as f:
            for replica_entry in f:
                replica_entry_normalized = replica_entry.strip()
                if not os.path.isdir(replica_entry_normalized):
                    print("warning: replica {} not present".format(replica_entry_normalized))

    def verify_script_path_registration(self):
        if not self.is_script_path_in_replica_list():
            print("warning: current script path not in replica list")

    def verify_replicas_presence(self):

        if not self.is_replica_file_present():
            print("warning: script directory does not have replicas.txt file")

        else:
            self.verify_replica_paths()
            self.verify_script_path_registration()

    def verify_ignore_presence(self):

        if not self.is_ignore_file_present():
            print("warning: script directory does not have ignore.txt file")

    def check(self):
        self.verify_python_version()
        self.verify_links_presence()
        self.verify_replicas_presence()
        self.verify_ignore_presence()

    def show_contents(self):

        title = "Contents of directory: {}".format(self.script_path)

        print("\n{}\n{}".format(title, "=" * len(title)))

        self.refresh_directory_contents()

        for x in self.script_directory_contents:
            if self.filters.check_links_file(x):
                print("{:60s} < links file".format(x))
            elif self.filters.check_script_file(x):
                print("{:60s} < control script file".format(x))
            elif self.filters.check_replicas_file(x):
                print("{:60s} < replica list file".format(x))
            elif self.filters.check_ignore_file(x):
                print("{:60s} < ignore list file".format(x))
            else:
                print(x)

    def generate_command_list(self):

        self.command_list = []

        self.command_list.append('commands: show commands')
        self.command_list.append('check: check')
        self.command_list.append('show: show directory elements')

        if self.is_links_file_present():
            self.command_list.append('links: show links')

        if not self.is_replica_file_present():
            self.command_list.append('initreplicas: create replica list file')

        if not self.is_ignore_file_present():
            self.command_list.append('initignore: create ignore list file')

        if self.is_replica_file_present():
            self.command_list.append('replicas: show replica list')
            self.command_list.append('addreplica: add new replica path to list')
            self.command_list.append('remreplica: remove replica path from list')
            self.command_list.append('diff: check differences between current replica and an available replicas')
            self.command_list.append('syncreplica: synchronize available replica with current replica')
            if not self.is_script_path_in_replica_list():
                self.command_list.append('synccurrent: set current script path to replica list')

        self.command_list.append('exit: exit script')

    def show_commands(self):
        self.generate_command_list()
        command_list_prompt(self.command_list)

    def script_main_loop(self):

        command = ""
        self.show_commands()

        while command != "exit":

            command = command_prompt()
            self.refresh_directory_contents()

            if command == "commands":
                self.show_commands()

            elif command == "check":
                self.check()

            elif command == "show":
                self.show_contents()

            elif self.is_links_file_present() and command == "links":
                show_links(self.script_path)

            elif not self.is_replica_file_present() and command == "initreplicas":
                generate_replicas_file(self.filters, self.script_path)

            elif not self.is_ignore_file_present() and command == "initignore":
                generate_ignore_file(self.filters, self.script_path)

            elif self.is_replica_file_present() and command == "replicas":
                show_replicas(self.filters, self.script_path)

            elif self.is_replica_file_present() and command == "addreplica":
                add_replica(self.filters, self.script_path)

            elif self.is_replica_file_present() and not self.is_script_path_in_replica_list() and command == "synccurrent":
                add_replica(self.filters, self.script_path, self.script_path)

            elif self.is_replica_file_present() and command == "remreplica":
                rem_replica(self.filters, self.script_path)

            elif self.is_replica_file_present() and command == "diff":
                diff_replica(self.filters, self.script_path)

            elif self.is_replica_file_present() and command == "syncreplica":
                sync_replica(self.filters, self.script_path)

            elif command == "exit":
                print("\nExiting...")

            self.refresh_directory_contents()


#
# main
#


def main():
    CommandManager(Utils(), Filters(), os.path.dirname(os.path.abspath(__main__.__file__))).script_main_loop()


if __name__ == "__main__":
    main()
