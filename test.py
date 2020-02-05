from firewall import Firewall
import os, csv,sys

if __name__ == '__main__':
    # Iteratively check a pair of nat*.csv and test*.csv exist in the tests
    # Construct nat with nat*.csv, and test cases in test*.csv file
    cur = 1
    while os.path.isfile("tests/fw" + str(cur) + ".csv") and os.path.isfile("tests/test" + str(cur) + ".csv"):
        print("TEST: " + str(cur))

        # Construct Firewall Class
        fw = Firewall("tests/fw" + str(cur) + ".csv")

        # Parse each line of test csv file
        with open("tests/test" + str(cur) + ".csv", 'r') as f:
            reader = csv.reader(f)
            for line in reader:
                if 5 != len(line):
                    print("Invalid format in input")
                    print(line)
                    sys.exit()
                transaction = line[0]
                transport   = line[1]
                port        = int(line[2])
                ip          = line[3]
                expected    = line[4]
                if expected == "True":
                    expected = True
                else:
                    expected = False

                # Check if expected value matches with actual response of firewall
                if expected == fw.accept_packet(transaction, transport, port, ip):
                    print("  PASS: " + transaction + " " + transport + " Port:" + str(port) + " IP:" + ip + " Expected:" + str(expected))
                else:
                    print("  FAIL: " + transaction + " " + transport + " Port:" + str(port) + " IP:" + ip + " Expected:" + str(expected))
        cur += 1