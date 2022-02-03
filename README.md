# CSV-to-IB
This will take in a CSV file specified in the UI and use Interactive Broker's API to place orders on a local paper account.

***How to setup API on any PC***

1. Download and install TWS (https://www.interactivebrokers.com/en/index.php?f=14099) or IB Gateway (https://www.interactivebrokers.ca/en/index.php?f=16457)

2. Download and install API at https://interactivebrokers.github.io/#

3. Run CMD as admin and navigate to C:\TWS API\source\pythonclient and run "$ python setup.py install"

4. Download python libraries: pandas ("$ pip install pandas")

5. Open TWS and navigate to File->Global Configuration->API->Settings and make sure Enable ActiveX and Socket Clients is checked

6. Open TWS and navigate to File->Global Configuration->API->Settings and make sure Allow connections from local host only is checked 
or 
open IBG and navigate to Configure->API->Settings and make sure Allow connections from local host only is checked

OR

uncheck and add "127.0.0.1" (local host) and any other trusted IP's needed

7. Port numbers should match the following for whichever services will be used (can be changed in same settings as above): 
TWS paper = 7497
TWS live = 7496
IBG paper = 4002
IBG live = 4001
