from UDPclient import UDPclient

client1 = UDPclient(13000) # assign port 13000 to the application on client 1
client2 = UDPclient(12000) # assign port 12000 to the application on client 2
x = 'a'
while x != 0:  # while the input is not 0, keep prompting the user which client he would like to choose
    if x == 1:  # client 1
        client1.send('Chris', 'message.txt')  # client1 will send to 'Chris' the file 'message.txt'
        client2.receive()  # client2 will receive the file from 'Chris' from port 16000
    elif x == 2:  # the opposite for client 2
        client2.send('Chris', 'message.txt')
        client1.receive()
    x = int(input('Choose which user is the sender (0 to exit): '))



