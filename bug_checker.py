#!/usr/bin/env python3

import csv
import logging
import argparse
import sys
from bugs.bug_class_mapper import BugClassMapper
from devices import DeviceClassMapper
from helpers import ThreadingHelper, DeviceHelper

_logger = logging.getLogger("BugChecker")


def check_bug(device, bug_list):
    """
    Method to check a bug against.
    :param device: device to connect to
    :type device: BaseBug
    :param bug_list: list of bugs to be checked
    :type bug_list: list
    :return:
    """


    for bug in bug_list:
        _logger.info(f"{device.ipaddr} - Starting {bug.bug_id} bug check")

        if bug.enable_mode_required:
            _logger.debug(f"{device.ipaddr} - Enable mode required for {bug.bug_id}")
            device.enter_enable_mode()

        device.check_bug(bug)
        _logger.info(f"{device.ipaddr} - Completed {bug.bug_id} bug check")

    _logger.debug(f"{device.ipaddr} - Disconnecting from device")
    device.disconnect()
    return device


def main(devices, bug_list, worker_threads=4):
    """
    Main run method.
    :param devices: list of device objects to check
    :type devices: list
    :param bug_list: list of bugs to check on the object
    :type bug_list: list
    :param worker_threads: Number of worker threads to use. Default is 4
    :type worker_threads: int
    :return: List of devices containing the results of the bug checks
    """

    _logger.info(f"Starting Bug Checker")
    _logger.info(f"-Bug List: {bug_list}")
    _logger.info(f"-Worker Threads: {worker_threads}")
    _logger.info(f"-Number of Devices: {len(devices)}")

    # if bug_ids is not a list, convert it to list
    if not isinstance(bug_list, list):
        bug_list = [bug_list]

    bugs = []

    for bug in bug_list:
        # get bug class and instantiate the class
        bugs.append(BugClassMapper.get_bug_class(str(bug))())

    args = {"bug_list": bugs}

    _logger.debug(f"Starting worker threads")
    th = ThreadingHelper(worker_func=check_bug, worker_func_args=args, num_of_workers=worker_threads)
    devices = th.run(devices)
    _logger.debug(f"Worker threads completed")
    return devices


def read_csv(input_file, credentials):
    """
    Read a CSV to create a list of devices to check.

    CSV File must contain a column titled "IP Address"
    :param input_file:  CSV file location
    :type input_file: str
    :param credentials: credentails to be used to connect to the devices.
    :type credentials: list
    :return: List of Devices
    """

    devices = []

    # Read CSV file and write each row to a Device Obect
    with open(input_file) as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:

            # Get device class, If no column exists then use autodetect type of device
            try:
                device_type = row["Device Type"]
                device = DeviceClassMapper.get_device_class(device_type)
            except IndexError:
                device = DeviceClassMapper.get_device_class("AutoDetect")

            device = device(credentials=credentials, ipaddr=row["IP Address"])
            devices.append(device)

    return devices


def write_csv(output_file, bug_list, devices):
    """
    Writes the checked devices results to a CSV file
    :param output_file: location of CSV file to be saved
    :type output_file: str
    :param bug_list: List of bugs been checked. Used to create coulmns for the results
    :type bug_list: list
    :param devices: list of devices to write to the CSV file
    :type devices: list
    :return:
    """

    # if bug_ids is not a list, convert it to list
    if not isinstance(bug_list, list):
        bug_list = [bug_list]

    rows = ["Hostname", "IP Address", "OS Version"]

    for b in bug_list:
        rows.append(f"{b} Impacted")
        rows.append(f"{b} Output")

        with open(output_file, "w") as csvfile:
            wr = csv.writer(csvfile, dialect="excel")

            wr.writerow(rows)

            for device in devices:
                row = [device.hostname, device.ipaddr, device.version]
                for bug in bug_list:
                    row.append(device.bugs[bug].impacted)
                    row.append(device.bugs[bug].output)

                wr.writerow(row)


if __name__ == "__main__":

    parse = argparse.ArgumentParser()
    parse.add_argument("-b", "--bugid", nargs="+", required=True,
                       help="<Required> Bug ID to test against devices. Place space between each Bug ID")
    parse.add_argument("-i", "--inputcsv", type=str, required=True,
                       help="<Required> Location of source CSV file")
    parse.add_argument("-o", "--outputcsv", type=str, required=True,
                       help="<Required> Location where output CSV should be writen")
    parse.add_argument("-w", "--workerthreads", type=int, default=4,
                       help="Number of worker threads to use. Default is 4")
    parse.add_argument("-lv", "--logginglevel", type=str,
                       choices=["critical", "error", "warning", "info", "debug", "notset"],
                       default="info",
                       help="Logging level, Default is info")
    parse.add_argument("-lf", "--loggingtofile", action="store_true",
                       help="Set if logging should be saved to the file")

    parse_args = parse.parse_args()

    creds = DeviceHelper.get_credentials()

    # Setting up logging

    logging_mapper = {
        "critical": logging.CRITICAL,
        "error": logging.ERROR,
        "warning": logging.WARNING,
        "info": logging.INFO,
        "debug": logging.DEBUG,
        "notset": logging.NOTSET
    }

    _logger.setLevel(logging_mapper[parse_args.logginglevel])

    formatter = logging.Formatter("%(asctime)s - %(threadName)s -  %(name)s - %(levelname)s - %(message)s")

    if parse_args.loggingtofile:
        fh = logging.FileHandler("BugChecker.log")
        fh.setFormatter(formatter)
        _logger.addHandler(fh)

    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(formatter)
    _logger.addHandler(sh)

    # get list of devices
    device_list = read_csv("devices.csv", creds)

    # check each device
    checked_devices = main(device_list, parse_args.bugid, parse_args.workerthreads)

    # write results to csv file
    write_csv(parse_args.outputcsv, parse_args.bugid, checked_devices)
