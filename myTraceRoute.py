import socket
import time

# Initial values for future use
dName = "www.google.ca" # the address of destination
dAdd = socket.gethostbyname(dName)
countHop = 1
numPort = 33434
sAdd = (dAdd, numPort)
markTF = True

# Print the information about the destination
print("traceroute to {} ({})".format(dName, dAdd))

# Start searching for the destination
while markTF == True:
    # The time for hop
    print("#" + str(countHop), end="  ")
    tries = 3
    # Start sending request
    sendTime = time.time()
    # Make sending end with UDP
    sendPeople = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sendPeople.setsockopt(socket.SOL_IP, socket.IP_TTL, countHop)
    sendPeople.sendto(b"", sAdd)
    # Make receiving end with ICMP
    receivePeople = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    receivePeople.settimeout(4)
    receivePeople.bind(("", numPort))

    # Try first time of connecting
    try:
        data, address = receivePeople.recvfrom(512)
        receiveTime = time.time()
        rtt = str(round((receiveTime-sendTime)*1000,3))
    except socket.error:
        rtt = "*"
        address = None
    finally:
        sendPeople.close()
        receivePeople.close()

    # If the first time is successful, start the second time and the third time, and print rtt
    if address is not None:
        # Provide address and name for second time and third time
        curAdd = str(address[0])

        try:
            name, alias, addresslist = socket.gethostbyaddr(curAdd)
            name = name
        except:
            name = curAdd

        # Print rtt for the first time
        print(rtt, end="  ")

        # Start the second time and the third time
        for _ in range(tries - 1):
            sendTime = time.time()
            # Make sending end
            sendPeople = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            sendPeople.setsockopt(socket.SOL_IP, socket.IP_TTL, countHop)
            sendPeople.sendto(b"", sAdd)
            # Make receiving end
            receivePeople = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            receivePeople.settimeout(4)
            receivePeople.bind(("", numPort))

            # Try connecting
            try:
                data, address = receivePeople.recvfrom(512)
                receiveTime = time.time()
                rtt = str(round((receiveTime - sendTime) * 1000, 3))
            except socket.error:
                rtt = "*"
                address = None
            finally:
                sendPeople.close()
                receivePeople.close()

            # Print rtt for the second time and the third time
            print(rtt, end="  ")
    else:
        for _ in range(tries):
            # Print rtt for the second time and the third time
            print(rtt, end="  ")

    # Print information about route
    if address is not None:
        print("{}({})".format(name, curAdd), end="  ")
        print()
    else:
        print()

    # Count the times of hop
    countHop = countHop + 1

    # Limit hop times not greater than 30
    if countHop > 30:
        print('Process done')
        markTF = False

    # Test whether arrive at destination. If yes, stop process
    if address == dAdd:
        print('Arrived at destination. Process done')
        markTF = False


