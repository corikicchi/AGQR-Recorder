# -*- coding: utf-8 -*-

import os
import sys
import time
import datetime
import subprocess
from errno import ENOENT

import config


def check(config):
    dt_now = datetime.datetime.now()
    print("current time: {0}".format(dt_now))

    program_to_rec = None
    for program in config.schedule:
        # check if wday of the program matches to current datetime
        # if program starts "00:00", wday is seems to be set to the one of the next day
        h_program, m_program = [int(s) for s in program["time"].split(":")]
        if h_program == 0 and m_program == 0:
            wday = (dt_now.weekday() + 1) % 7
        else:
            wday = dt_now.weekday()
        if wday != program["wday"]:
            continue

        # check hours and minutes
        if m_program == 00:
            if (h_program - 1) % 24 == dt_now.hour and dt_now.minute == 59:
                print("{} is scheduled".format(program["title"]))
                program_to_rec = program
                break
        elif m_program == 30:
            if h_program == dt_now.hour and dt_now.minute == 29:
                print("{} is scheduled".format(program["title"]))
                program_to_rec = program
                break
    else:
        print("No recording is scheduled")

    return program_to_rec


def record(config, program):
    # base file name
    dt_now = datetime.datetime.now()
    h_program, m_program = [int(s) for s in program["time"].split(":")]
    if h_program == 0 and m_program == 0:
        dt_now = dt_now + datetime.timedelta(days=1)
    fn = "{0:04d}".format(dt_now.year) \
         + "{0:02d}".format(dt_now.month) \
         + "{0:02d}".format(dt_now.day)

    # flv file name
    fp_flv = os.path.join(config.dn_flv, program["title"] + "_" + fn + ".flv")

    # create rtmpdump command
    rec_length = int(program["length"]) * 60 + 30
    rtmpdump_command = [config.rtmpdump, "-r", config.stream, "--live", "-B", rec_length, "-o", fp_flv]
    rtmpdump_command = [str(s) for s in rtmpdump_command]

    # sleep 30sec
    time.sleep(30)

    # record
    if not os.path.exists(config.dn_flv) or not os.path.isdir(config.dn_flv):
        os.makedirs(config.dn_flv)
    if not os.path.exists(os.path.dirname(config.fp_log)):
        os.makedirs(os.path.dirname(config.fp_log))
    with open(config.fp_log, "a") as fout:
        fout.write("[{}] start recording: {}\n".format(datetime.datetime.now(), os.path.basename(fp_flv)))
    subprocess.call(rtmpdump_command)
    with open(config.fp_log, "a") as fout:
        fout.write("[{}] finish recording: {}\n".format(datetime.datetime.now(), os.path.basename(fp_flv)))

    if program["movie"] == 1:
        fp_mp4 = os.path.join(config.dn_mp4, program["title"] + "_" + fn + ".mp4")
        if not os.path.exists(config.dn_mp4) or not os.path.isdir(config.dn_mp4):
            os.makedirs(config.dn_mp4)
        ffmpeg_command = [config.ffmpeg, "-y", "-i", fp_flv, "-vcodec", "copy", "-acodec", "copy", fp_mp4]
        ffmpeg_command = [str(s) for s in ffmpeg_command]

        # convert
        with open(config.fp_log, "a") as fout:
            fout.write("[{}] start converting: {} -> {}\n".format(datetime.datetime.now(),
                                                                  os.path.basename(fp_flv), os.path.basename(fp_mp4)))
        subprocess.call(ffmpeg_command)
        with open(config.fp_log, "a") as fout:
            fout.write("[{}] finish converting: {} -> {}\n".format(datetime.datetime.now(),
                                                                   os.path.basename(fp_flv), os.path.basename(fp_mp4)))
    elif program["movie"] == 0:
        fp_m4a = os.path.join(config.dn_m4a, program["title"] + "_" + fn + ".m4a")
        if not os.path.exists(config.dn_m4a) or not os.path.isdir(config.dn_m4a):
            os.makedirs(config.dn_m4a)
        ffmpeg_command = [config.ffmpeg, "-y", "-i", fp_flv, "-vn", "-acodec", "copy", fp_m4a]
        ffmpeg_command = [str(s) for s in ffmpeg_command]

        # convert
        with open(config.fp_log, "a") as fout:
            fout.write("[{}] start converting: {} -> {}\n".format(datetime.datetime.now(),
                                                                  os.path.basename(fp_flv), os.path.basename(fp_m4a)))
        subprocess.call(ffmpeg_command)
        with open(config.fp_log, "a") as fout:
            fout.write("[{}] finish converting: {} -> {}\n".format(datetime.datetime.now(),
                                                                   os.path.basename(fp_flv), os.path.basename(fp_m4a)))
    else:
        raise IndexError(ENOENT, "Invalid index", program["movie"])


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Usage:")
        print("\t{} /path/to/config.yml".format(os.path.basename(sys.argv[0])))
        exit(1)
    fp_config = os.path.realpath(os.path.expanduser(sys.argv[1]))
    if not os.path.exists(fp_config) or not os.path.isfile(fp_config):
        raise FileNotFoundError(ENOENT, "No such file", fp_config)
    config = config.config(fp_config)

    program = check(config)
    if program is not None:
        record(config, program)
