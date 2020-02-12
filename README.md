Firewall
===
## Description
- `firewall.py`: Firewall class is defined
- `test.py`: The file for testing Firewall class using files in the `tests/`
- `tests/fw*.csv`: Firewall configuration of each test is defined
- `tests/test*.csv`: Each testcase is defined for each corresponding configuration file

## Functionality
- *Firewall* class takes a configuration csv file as an argument of constructor to construct a table
- *accept_packet(direction, protocol, port, ip_address)* function in the *Firewall* class takes a direction of transaction (inbound or outbound), transport protocol (tcp or udp), port number, and IP address as arguments and return True or False to indicate whether to accept packet or not.

## Usage
```
$ python3 test.py

```
Test all the cases in the `tests/` and show whether each case passed the test case or not. Testcases are defined in the format of `<direction>,<protocol>,<port>,<ip>,<expected result>` in the `test*.csv`. Following is the example of `test*.csv`.

```
inbound,tcp,80,192.168.10.11,True
outbound,udp,22,192.168.50.1,False
inbound,tcp,23,172.27.1.1,True
inbound,tdp,443,172.27.1.2,False

```

## Performance

The implementation takes O(log(n)) to add or delete entries. Also, it reduces the number of entries to compare with when `accept_packet` function is called. However, it still takes O(n) to query whether it accepts or not. Due to the 90 minutes time constraint, I was not able to reduce the query time to O(log(n)). Please see future optimization section for the detail of possible design.

## Observation
#### Test
Made sure a function works correctly for all the edge cases. First, since IP ranges from 0.0.0.0 to 255.255.255.255 and Port ranges from 0 to 65535, it tests the corner of each range works fine (`fw1.csv` and `test1.csv`). Second, it takes cases when duplicate IP ranges or Port ranges have different rules work fine (`fw2.csv` and `test2.csv`).

#### Design
Table consists of array of tuples consists of 4 elements; `(<IP range start>, <Port range start>, <IP range end>, <Port range end>)`. By using this format, it can binary search the index where a new entry have to be inserted or an existing entry have to be deleted. To reduce the range to query, it finds the point where it have to start query from by using Binary Search (`bisect`).

#### Future Optimization
Even though adding or deleting the entry takes always O(log(n)), judging whether to accept a packet or not takes O(n) in the worst case since it is checking each entry one by one from the index obtained by binary search. The possible optimizations are shown below.
1. Have Trie to query for the IP range it matches. Each Trie node can have a subnet/subnet mask and an array of its accepting port range. It would take O(log(n)) to query whether IP:Port pair is accepted or not. However, to make Trie to work, IP range have to be specified by subnet instead of specific start and end of the range.
2. Have array of IP ranges and dictionary of key as IP range and array of Port ranges it accept as its value. However, as the rules becomes complicated, the number of entries in the IP range array would be big and it consumes large memory space. Deleting the existing rule would be impossible.

#### Comment
Thank you for taking time to review the code. The ranking of my interested teams are as follows. Even though I listed a ranking, all of the teams look really interesting and I would be excited if I can work in any of the team.
1. platform team
2. data team
3. policy team
