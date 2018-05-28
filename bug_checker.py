#!/usr/bin/env python3

import csv
import logging
import argparse
import sys
from bugs.bug_class_mapper import BugClassMapper
from devices import DeviceClassMapper, ConnectionException
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

    try:
        for bug in bug_list:
            _logger.info(f"{device.ipaddr} - Starting {bug.bug_id} bug check")

            if bug.enable_mode_required:
                _logger.debug(f"{device.ipaddr} - Enable mode required for {bug.bug_id}")
                device.enter_enable_mode()

            device.check_bug(bug)
            _logger.info(f"{device.ipaddr} - Completed {bug.bug_id} bug check")

        _logger.debug(f"{device.ipaddr} - Disconnecting from device")
        device.disconnect()

    except ConnectionException as e:
        device.connection_error = e

    finally:
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

    bugs = BugClassMapper.get_bug_class(bug_list)

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

    rows = ["Hostname", "IP Address", "OS Version", "Connection Error"]

    for b in bug_list:
        rows.append(f"{b} Impacted")
        rows.append(f"{b} Output")

    with open(output_file, "w") as csvfile:
        wr = csv.writer(csvfile, dialect="excel")
        wr.writerow(rows)

        for device in devices:

            # if connection error, write blank results
            if device.connection_error:
                row = ["", device.ipaddr, "", device.connection_error]
            else:

                row = [device.hostname, device.ipaddr, device.version, device.connection_error]

                for bug in bug_list:
                    row.append(device.bugs[bug].impacted)
                    row.append(device.bugs[bug].output)

            wr.writerow(row)

def print_bug_detail(bug_list):
    """
    Print out bug details
    :param bug_list: list of bugs to print details for.
    :return:
    """

    # if bug_ids is not a list, convert it to list
    if not isinstance(bug_list, list):
        bug_list = [bug_list]

    for b in BugClassMapper.get_bug_class(bug_list):

        print(f"Bug ID: {b.manufacture_bug_id()}")
        print(f"Bug Manufacture: {b.manufacture()}")
        print(f"CVE ID: {b.cve_id()}")
        print(f"Bug Reference: {b.bug_reference()}")
        print(f"Bug Severity: {b.bug_severity()}")
        print(f"Bug Description: \n{b.bug_description()}")
        print(f"Remediate Implimented: {b.remediate_implimented()}")
        print(f"Affected Devices: {b.affected_devices()}")
        print(f"Enable Mode required: {b.enable_mode_required()}")



def print_bug_summary():

    print("-" * 115)
    print(f"| {'Manufacture':^13} | {'Bug ID':^13} | {'CVE ID':^15} | {'Severity':^10} | {'Affected':^15} | {'Enable Mode':^13} | {'Remediate':^14} |")
    print(f"| {'':^13} | {'':^13} | {'':^15} | {'':^10} | {'Devices':^15} | {'Required':^13} | {'Implimented':^14} |")
    print("-" * 115)

    for b in BugClassMapper.get_bug_class():
        affected_devices = b.affected_devices()
        print(f"| {b.manufacture():^13} | {b.manufacture_bug_id():^13} | {b.cve_id():^15} | {b.bug_severity():^10} | {affected_devices[0]:^15} | {b.enable_mode_required():^13} | {b.remediate_implimented():^14} |")

        for a in affected_devices[1:len(affected_devices)]:
            print(
                f"| {'':^13} | {'':^13} | {'':^15} | {'':^10} | {a:^15} | {'':^13} | {'':^14} |")

        print("-" * 115)

if __name__ == "__main__":

    parse = argparse.ArgumentParser()
    parse.add_argument("-c", "--checkdevice", action="store_true",
                       help="Specifies if a bug is to be checked on a device")
    parse.add_argument("-l", "--listbugdetails", action="store_true",
                       help="Specifies if a bug details are to be listed")

    parse.add_argument("-b", "--bugid", nargs="+",
                       help="Bug ID to check against devices if -c is set, or Bug ID to list details. Place space "
                            "between each Bug ID")

    parse.add_argument("-i", "--inputcsv", type=str,
                       help="Location of source CSV file")
    parse.add_argument("-o", "--outputcsv", type=str,
                       help="Location where output CSV should be writen")

    parse.add_argument("-s","--bugsummary", action="store_true",
                       help="Prints a summary of all bugs")

    parse.add_argument("--workerthreads", type=int, default=4,
                       help="Number of worker threads to use. Default is 4")
    parse.add_argument("--logginglevel", type=str,
                       choices=["critical", "error", "warning", "info", "debug", "notset"],
                       default="info",
                       help="Logging level, Default is info")
    parse.add_argument("--loggingtofile", action="store_true",
                       help="Set if logging should be saved to the file")

    parse_args = parse.parse_args()

    if not parse_args.checkdevice and not parse_args.listbugdetails:
        print("Bug Checker requires either -c or -l to be set")
    else:
        if parse_args.listbugdetails:
           if not (parse_args.bugid or parse_args.bugsummary):
               print("If -l is spesified, --bugid or --bugsummary are required")
           else:
               if parse_args.bugid:
                   print_bug_detail(parse_args.bugid)
               elif parse_args.bugsummary:
                   print_bug_summary()

        elif parse_args.checkdevice:
            if parse_args.checkdevice and not parse_args.bugid and not parse_args.inputcsv and not parse_args.outputcsv:
                print("If -b is specified, the following are required --bug, --inputcsv as --outputcsv")
            else:
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

                formatter = logging.Formatter(
                    "%(asctime)s - %(threadName)s -  %(name)s - %(levelname)s - %(message)s")

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
