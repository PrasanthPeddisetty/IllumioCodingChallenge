import sys, csv, socket, struct, bisect

class Firewall:
    ''' Simplified Firewall class '''
    # The "tables" dictionary consists of 4 array for each (transaction, transport) pair.
    # An element in the array is a tuple consists of 4 values; (Start of IP range, Start of Port range, End of IP range, End of Port range).
    tables = {
                ("inbound", "tcp") : [],
                ("inbound", "udp") : [],
                ("outbound", "tcp"): [],
                ("outbound", "udp"): [],
            }

    # Constructor takes csv file as an argument, parse it, and add entry to corresponding array in the "tables".
    def __init__(self, filename):
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            for line in reader:
                if 4 != len(line):
                    print("Invalid format in input")
                    sys.exit()
                transaction = line[0]
                transport   = line[1]
                port_range  = line[2]
                ip_range    = line[3]
                self.add_entry(transaction, transport, port_range, ip_range)

    # Adds new entry into the corresponding array in the "tables".
    # Binary search to find the location to add new entry.
    def add_entry(self,  transaction, transport, port_range, ip_range):
        port_range = port_range.split('-')
        ip_range = ip_range.split('-')
        port_from = int(port_range[0])
        if len(port_range) > 1:
            port_to = int(port_range[1])
        else:
            port_to = port_from
        ip_from = self.ip2int(ip_range[0])
        if len(ip_range) > 1:
            ip_to = self.ip2int(ip_range[1])
        else:
            ip_to = ip_from

        table = self.tables[(transaction, transport)]
        entry = (ip_from, port_from, ip_to, port_to)
        idx = bisect.bisect_right(table, entry)
        if idx == 0 or table[idx - 1] != entry:
            table.insert(idx, entry)

    # Reduce the range to query using Binary Search.
    # If found, return True. If not found, return False.
    def accept_packet(self, transaction, transport, port, ip):
        table = self.tables[(transaction, transport)]
        ip = self.ip2int(ip)
        maxip = self.ip2int("255.255.255.255")
        maxport = 65535
        key = (ip, port, maxip, maxport)
        start_idx = bisect.bisect_right(table, key) - 1
        for idx in range(start_idx, -1, -1):
            if idx < len(table) and ip >= table[idx][0] and ip <= table[idx][2] and port >= table[idx][1] and port <= table[idx][3]:
                return True
        return False

    # Convert string IP to int IP, and vice versa.
    # Ref: https://stackoverflow.com/questions/5619685/
    def ip2int(self, addr):
        return struct.unpack("!I", socket.inet_aton(addr))[0]
    def int2ip(self, addr):
        return socket.inet_ntoa(struct.pack("!I", addr))


if __name__ == '__main__':
    fw = Firewall("fw.csv")
    print(fw.accept_packet("inbound", "tcp", 80, "192.168.1.2"))
    print(fw.accept_packet("inbound", "udp", 53, "192.168.2.1"))
    print(fw.accept_packet("outbound", "tcp", 10234, "192.168.10.11"))
    print(fw.accept_packet("inbound", "tcp", 81, "192.168.1.2"))
    print(fw.accept_packet("inbound", "udp", 24, "52.12.48.92"))