# AGQR-Recorder

Python script to record AGQR streaming as your schedule

## Requirements

- Python 3.4 or later
    - with `PyYAML` module
- `rtmpdump`
- `ffmpeg`

## How to Use

1. Install dependences
    - Install `rtmpdump`, `ffmpeg` and python modules.

```bash
$ sudo apt install -y rtmpdump ffmpeg
$ sudo apt install -y python3-pip
$ pip3 install pyyaml
```

2. Configure config.yml
    - Configure config.yml according to your environment. **DO NOT** use tilde (`~`) when using crontab.

```bash
$ cat config.yml
# path of schedule file
schedule: ./schedule.yml

# path of a log file
log: ./log.txt

# path to save media files
flv: ./AGQR/flv
mp4: ./AGQR/mp4
m4a: ./AGQR/m4a

# rtmpdump executable
rtmpdump: rtmpdump
# ffmpeg executable
ffmpeg: ffmpeg

# AGQR streaming URL
stream: rtmp://fms-base1.mitene.ad.jp/agqr/aandg22
```

3. Schedule
    - Input schedule of programs to schedule.yml.

```bash
$ cat schedule.yml
- title: Yoru_Night_Thu
  wday: 4
  time: "0:00"
  length: 60
  movie: 1

- title: Hondo_Joriku_Sakusen
  wday: 1
  time: "2:00"
  length: 30
  movie: 1
```

The definition of wday is as below.

| wday | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|------|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|      |Mon|Tue|Wed|Thu|Fri|Sat|Sun|

4. Configure crontab
    - Append schedule to crontab.

```bash
$ crontab -e
```

```crontab
# AGQR Recorder
29,59 * * * * /usr/bin/python3 /full/path/to/AGQR-Recorder/agqr.py /full/path/to/AGQR-Recorder/config.yml > /dev/null
```
