#!/usr/bin/env python3

import subprocess

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

def ping(ping_location):
    # provides the functionality to ping

    icmp = subprocess.call(["ping", "-c", "4", ping_location])
    if icmp == 0:
        print("\033[32mSUCCESS\033[0m")
    else:
        print("\033[31mFAIL\033[0m")

    return None

def main():

    # clear the terminal before starting
    subprocess.call("clear", shell=True)

    while(True):

        # present the user with the menu
        print("\033[33mWelcome to the Ping Test!")
        print("\t1. Display the default gateway \n\t2. Test Local Connectivity \n\t3. Test Remote Connectivity \n\t4. Test DNS Resolution")

        # try-except statement to handle non-numeric input
        try: 
            userInput = input("Select an option from the menu (1-4) or \"Q/q\" to quit:\033[0m ")

            # quit the program
            if userInput.lower() == "q":
                print("\033[35mThanks for choosing us!")
                print("Exiting the program...\033[0m")
                break

            # display the default gateway
            elif int(userInput) == 1:
                print("\033[32mDefault Gateway: ", get_default_gateway(), "\033[0m")

            # test local connectivity
            elif int(userInput) == 2:
                print("\033[32mPinging default gateway...\033[m")

                # gets the default gaetway to run the ping
                dg = get_default_gateway()
                if not dg:
                    print("\033[31mCould not find the default gateway!\033\0m")
                    continue
                
                ping(dg)

            # test remote connectivity 
            elif int(userInput) == 3:
                print("\033[32mPinging remote IP...\033[0m")

                ritdns = "129.21.3.17"
                ping(ritdns)

            # test dns resolution
            elif int(userInput) == 4:
                print("\033[32mTesting DNS Resolution...\033[0m")

                sample_domain = "www.google.com"
                ping(sample_domain)

            # indicate that the option entered was invalid
            else: 
                print("\033[31mYou entered an invalid option!\033[0m")
                continue

        # handles non-numeric input
        except ValueError:
            print("\033[31mYou entered an invalid option!\033[0m")
            continue

if __name__ == "__main__":
    main()


