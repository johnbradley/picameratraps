#!/usr/bin/env python3
import argparse
import sys
import subprocess
import os

CAMERA_TRAP_LIST_PATH = "cameratraps.txt"


def get_trap_hosts():
    with open(CAMERA_TRAP_LIST_PATH, "rt") as infile:
        lines = infile.readlines()
        return [line.strip() for line in lines]


def run_cmd(cmd_str):
    print(f"Running {cmd_str}")
    subprocess.run(f"bash -c '{cmd_str}'", shell=True)


def print_host_header(host):
    print("----------------------")
    print(host)
    print("----------------------")


def run_cmd_on_traps(cmd, msg=None, sync_remote_files_first=False):
    if msg:
        print(msg)
    for host in get_trap_hosts():
        print_host_header(host)
        if sync_remote_files_first:
            run_cmd(f"rsync --recursive --perms remote-files/* pi@{host}:.")
        run_cmd(f"ssh -o ConnectTimeout=4 pi@{host} {cmd}")


def init(args):
    run_cmd_on_traps(
        cmd="./scripts/init.sh",
        msg="Perform one-time setup on camera traps",
        sync_remote_files_first=True,
    )


def setup_alarms(args):
    run_cmd_on_traps(
        cmd="./scripts/setup.sh",
        msg="Setup camera trap alarms",
        sync_remote_files_first=True,
    )
    print("Run the 'shutdown' command to begin recording on the next alarm")

def sync_rtc(args):
    run_cmd_on_traps(
        cmd="sudo hwclock -w --verbose",
        msg="Synchronizing RTC clock with Pi system clock",
    )

def status(args):
    run_cmd_on_traps(cmd="./scripts/status.sh", msg="Checking camera trap status")


def set_wifi(args):
    print("Set WiFi on camera traps - to enable downloading data from Phone HotSpot in the field")
    ssid = input("SSID: ")
    password = input("Password: ")
    cmd = f"sudo raspi-config nonint do_wifi_ssid_passphrase {ssid} {password}"
    run_cmd_on_traps(cmd=cmd, msg="Applying WiFi settings")


def stream(args):
    hostname = args.hostname
    print(f"Video streaming for {hostname}")
    print("Open another terminal and run:")
    print(f"vlc tcp/h264://{hostname}:8888/")
    print("Press Ctrl-C to terminate streaming")
    run_cmd(f"ssh -o ConnectTimeout=4 pi@{hostname} ./scripts/streamvid.sh")


def fetch(args):
    base_cmd = "rsync -v --stats --progress --recursive --times"
    for host in get_trap_hosts():
        print_host_header(host)
        dest = f"results/{host}"
        os.makedirs(dest, exist_ok=True)
        run_cmd(f"{base_cmd} pi@{host}:images {dest}")
        run_cmd(f"{base_cmd} pi@{host}:videos {dest}")
        run_cmd(f"{base_cmd} pi@{host}:logs {dest}")


def convert(args):
    print("Converting videos from .h264 to .mkv format")
    run_cmd("./convertvideos.sh")


def purge(args):
    run_cmd_on_traps(
        cmd="./scripts/purge.sh",
        msg="Deleting images from camera traps older than 24 hours",
    )


def shutdown(args):
    run_cmd_on_traps(
        cmd="./scripts/shutdown.sh",
        msg="Shutting down Raspberry Pis - so alarms will fire and begin recording",
    )


def create_command_parser():
    parser = argparse.ArgumentParser(description="Raspberry Pi Camera Trap Manager")
    subparsers = parser.add_subparsers()

    subparser = subparsers.add_parser(
        "init", description="Perform one-time setup on camera traps"
    )
    subparser.set_defaults(func=init)

    subparser = subparsers.add_parser("setup", description="Setup for recording")
    subparser.set_defaults(func=setup_alarms)

    subparser = subparsers.add_parser(
        "sync-rtc", description="Synchronize Real Time Clock with system time"
    )
    subparser.set_defaults(func=sync_rtc)

    subparser = subparsers.add_parser(
        "status", description="Check status for all camera traps"
    )
    subparser.set_defaults(func=status)

    subparser = subparsers.add_parser(
        "set-wifi", description="Set WiFi - Phone HotSpot for fetching images/video"
    )
    subparser.set_defaults(func=set_wifi)

    subparser = subparsers.add_parser(
        "stream", description="Stream video from one camera trap"
    )
    subparser.add_argument(
        "hostname", help="Hostname of camera trap from cameratraps.txt"
    )
    subparser.set_defaults(func=stream)

    subparser = subparsers.add_parser(
        "shutdown", description="Shutdown all Raspberry Pis (so recording can begin)"
    )
    subparser.set_defaults(func=shutdown)

    subparser = subparsers.add_parser(
        "fetch", description="Fetch images from camera traps"
    )
    subparser.set_defaults(func=fetch)

    subparser = subparsers.add_parser(
        "convert", description="Convert videos into  images from camera traps"
    )
    subparser.set_defaults(func=convert)

    subparser = subparsers.add_parser(
        "purge",
        description="Delete images/videos from camera traps older than 24 hours",
    )
    subparser.set_defaults(func=purge)

    return parser


parser = create_command_parser()
args = parser.parse_args()
if hasattr(args, "func"):
    args.func(args)
else:
    parser.print_help()
    sys.exit(1)
