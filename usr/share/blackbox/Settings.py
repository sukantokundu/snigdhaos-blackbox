#!/bin/python

import os
import Functions as fn
import string
from string import Template

base_dir = os.path.dirname(os.path.realpath(__file__))

default_file = "%s/defaults/blackbox.yaml" % base_dir

class Settings(object):
    def __init__(self, display_versions, display_package_progress):
        self.display_versions = display_versions
        self.display_package_progress = display_package_progress
    
    def write_config_file(self):
        try:
            content = []
            with open(fn.config_file, "r", encoding="utf-8") as f:
                contents = f.readlines()
            if len(contents) > 0:
                self.read(contents)
                conf_settings = {}
                conf_settings[
                    "Display Package Versions"
                    ] = self.display_versions
                conf_settings[
                    "Display Package Progress"
                    ] = self.display_package_progress
                index = 0
                for line in contents:
                    if line.startswith("- name:"):
                        if (
                            line.strip("- name:")
                            .strip()
                            .strip('"')
                            .strip("\n")
                            .strip()
                            == "Display Package Versions"
                        ):
                            index = contents.index(line)
                            index += 2
                            if contents[index].startswith(" enabled: "):
                                del contents[index]
                                contents.insert(
                                    index,
                                    " enabled: %s\n"
                                    % conf_settings["Display Package Versions"],
                                )
                        if (
                            line.strip("- name:")
                            .strip()
                            .strip('"')
                            .strip("\n")
                            .strip()
                            == "Display Package Progress"
                        ):
                            index += 4
                            if contents[index].startswith(" enabled: "):
                                del contents[index]
                                contents.insert(
                                    index,
                                    " enabled: %s\n"
                                    % conf_settings["Display Package Progress"],
                                )
            
            if len(contents) > 0:
                with open(fn.config_file, "w", encoding="utf-8") as f:
                    f.writelines(contents)
                fn.permissions(fn.config_dir)
        
        except Exception as e:
            fn.Logger.error("[ERROR] Exception: %s" % e)
    
    def read_config_file(self):
        try:
            if os.path.exists(fn.config_file):
                contents = []
                with open(fn.config_file, "r", encoding="utf-8") as f:
                    contents = f.readlines()
                if len(contents) == 0:
                    fn.shutil.copy(default_file, fn.config_file)
                    fn.permissions(fn.config_dir)
                else:
                    return self.read(contents)
            else:
                # NOTE: String Replaces the Template File
                fn.shutil.copy(default_file, fn.config_file)
                fn.permissions(fn.config_dir)
                with open(fn.config_file, "r", encoding="utf-8") as f:
                    contents = f.readlines()
                return self.read(contents)
        except Exception as e:
            print("[ERROR] Exception: %s" % e)

    def read(self, contents):
        setting_name = None
        setting_value_enabled = None
        conf_settings = {}
        for line in contents:
            if line.startswith("- name:"):
                setting_name = (
                    line.strip("- name: ")
                    .strip()
                    .strip('"')
                    .strip("\n")
                    .strip()
                )
            elif line.startswith(" enabled: "):
                setting_value_enabled = (
                    line.strip("- name: ")
                    .strip()
                    .strip('"')
                    .strip("\n")
                    .strip()
                )
                if setting_value_enabled == "False":
                    conf_settings[setting_name] = False
                else:
                    conf_settings[setting_name] = True
        if len(conf_settings) > 0:
            return conf_settings
        else:
            print("[ERROR] Failed To Read Settings!")
