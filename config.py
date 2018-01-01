# -*- coding: utf-8 -*-

import os
import yaml
import shutil
from errno import ENOENT


class config:
    def __init__(self, fn_yml):
        self.fp_yml = os.path.realpath(os.path.expanduser(fn_yml))
        if not os.path.exists(self.fp_yml) and not os.path.isfile(self.fp_yml):
            raise IOError(ENOENT, "No such file", self.fp_yml)

        # load config.yml
        with open(self.fp_yml, "r") as fin:
            self.yml = yaml.load(fin)
        print("config file: {0}".format(self.fp_yml))

        self.rtmpdump = shutil.which(self.yml["rtmpdump"])
        if self.rtmpdump is None:
            raise IOError(ENOENT, "No such executable", self.yml["rtmpdump"])
        print("    rtmpdump: {0}".format(self.rtmpdump))

        self.ffmpeg = shutil.which(self.yml["ffmpeg"])
        if self.ffmpeg is None:
            raise IOError(ENOENT, "No such executable", self.yml["ffmpeg"])
        print("    ffmpeg: {0}".format(self.ffmpeg))

        self.fp_schedule = os.path.join(os.path.dirname(self.fp_yml), self.yml["schedule"])
        self.fp_schedule = os.path.realpath(os.path.expanduser(self.fp_schedule))
        print("    schedule: {0}".format(self.fp_schedule))

        # load schedule file
        with open(self.fp_schedule, "r") as fin:
            self.schedule = yaml.load(fin)
