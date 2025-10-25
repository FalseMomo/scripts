#!/usr/bin/env python3

import subprocess
import datetime
import socket
import sys
import os

def get_default_gateway():
    # returns the default gateway

    try:
        output = subprocess.check_output(["ip", "route", "show", "default"], text=True).strip()
        if output:
            token = output.split()
            if "via" in token:
                return token[token.index("via")+1]

    except Exception:
        return None

    return None

def get_ip_address():
    # returns the ip address

    try:
        output = subprocess.check_output(["ifconfig"], text=True)
        for line in output.splitlines():
            line  = line.strip()
            if "inet" in line:
                token = line.split()
                return token[token.index("inet")+1]

    except Exception:
        return None

    return None


def get_subnet_mask():
    # returns the subnet mask

    try:
        output = subprocess.check_output(["ifconfig"], text=True)
        for line in output.splitlines():
            line  = line.strip()
            if "netmask" in line:
                token = line.split()
                return token[token.index("netmask")+1]

    except Exception:
        return None

    return None

def get_kernel_version():
    # returns kernel version

    try: 
        output = subprocess.check_output(["uname", "-r"], text=True)
        return output

    except Exception:
        return None

    return None

def get_drive_total():
    # returns total drive space

    output = subprocess.check_output(["df", "-h", "/"], text=True)
    line = output.strip().splitlines()
    
    return line[1].split()[1]

def get_drive_used():
    # returns used drive space

    output = subprocess.check_output(["df", "-h", "/"], text=True)
    line = output.strip().splitlines()

    return line[1].split()[2]

def get_drive_free():
    # returns free drive space

    output = subprocess.check_output(["df", "-h", "/"], text=True)
    line = output.strip().splitlines()

    return line[1].split()[3]

def get_ram_total():
    # returns total ram space

    output = subprocess.check_output(["free", "-h"], text=True)
    line = output.strip().splitlines()

    return line[1].split()[1]

def get_ram_available():
    # returns available ram space

    output = subprocess.check_output(["free", "-h"], text=True)
    line = output.strip().splitlines()

    return line[1].split()[6]

def main():

    # clear the terminal before starting
    # subprocess.call("clear", shell=True)

    # print header
    today = datetime.datetime.today()
    current = today.strftime("%B %d, %Y")
    text = "\033[31mSystem Report - \033[0m" + current
    print(text.center(80), "\n")

    # print device information
    print("\033[32mDevice Information:          \033[0m")
    
    fqdn = socket.getfqdn()
    fqdn_split = fqdn.split(".")

    hostname = fqdn_split[0]
    domain = fqdn_split[1] + "." + fqdn_split[2]
    
    print("Hostname:                     ", hostname)

    print("Domain:                       ", domain, "\n")

    # print network information
    print("\033[32mNetwork Information:          \033[0m")

    print("IP Address:                   ", get_ip_address())
    
    print("Gateway:                      ", get_default_gateway())

    print("Network Mask:                 ", get_subnet_mask())

    dns = []
    with open("/etc/resolv.conf") as dns_file:
        for line in dns_file:
            line = line.strip()
            if line.startswith("nameserver"):
                dns.append(line.split()[1])

    print("DNS1:                         ", dns[0])

    print("DNS2:                         ", dns[1], "\n")

    # print operating system information
    print("\033[32mOperating System Information:\033[0m")

    with open("/etc/os-release") as os_file:
        for line in os_file:
            line = line.strip()
            if line.startswith("NAME="):
                os_name1 = line.split("\"")[1]
            if line.startswith("VERSION="):
                os_name2 = line.split("\"")[1]
            if line.startswith("VERSION_ID="):
                os_version = line.split("\"")[1]

        os = os_name1 + " " + os_name2

    print("Operating System:             ", os)

    print("OS Version:                   ", os_version)  

    print("Kernel Version:               ", get_kernel_version())

    # print storage information
    print("\033[32mStorage Information:          \033[0m")
    
    print("System Drive Total:           ", get_drive_total())

    print("System Drive Used:            ", get_drive_used())

    print("System Drive Free:            ", get_drive_free(), "\n")

    # print processor information
    print("\033[32mProcessor Information:        \033[0m")

    processors = 0
    with open("/proc/cpuinfo") as cpu_file:
        for line in cpu_file:
            line = line.strip()
            if line.startswith("model name"):
                model = line.split(":")[1].strip()
            if line.startswith("physical id"):
                processors += 1
            if line.startswith("cpu cores"):
                cores = line.split(":")[1].strip()

    if processors == 0:
        processors = 1
            
    print("CPU Model:                    ", model)

    print("Number of processors:         ", processors)

    print("Number of cores:              ", cores, "\n")

    # print memory information
    print("\033[32mMemory Information:           \033[0m")

    print("Total RAM:                    ", get_ram_total())

    print("Available RAM:                ", get_ram_available(), "\n")

if __name__ == "__main__":
    
    # clear the terminal before running
    subprocess.call(["clear"], shell=True)

    # call main()
    main()

    # create the log file
    hostname = socket.gethostname().split(".")[0]
    log = os.path.expanduser("~/" + hostname.strip() + "_system_report.log")
    with open(log, "w") as logfile:
        output = sys.stdout
        sys.stdout = logfile
        main()
        sys.stdout = output
    

