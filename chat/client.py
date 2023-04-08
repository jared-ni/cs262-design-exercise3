import threading
import grpc
import chat_pb2 as chat
import chat_pb2_grpc as rpc
import time 
from hashlib import blake2b
import sys
import errno
import signal
import socket

# Generate grpc server code by running 
# 'python3 -m grpc_tools.protoc -I protos --python_out=. --grpc_python_out=. protos/chat.proto'

# client-side hashing key of account password. Passwords cannot be unhashed. 
CLIENT_KEY = b'cs262IsFunAndWaldoIsCool'
FORMAT = "utf-8"

# client class for all client-side functionalities
class Client:
    def __init__(self):
        # the frame to put ui components on
        self.username = ""
        self.address = socket.gethostbyname(socket.gethostname())
        # self.port = None
        # dictionary of (ip, ports) of all replicas
        self.ip_ports = {
            "R1": None,
            "R2": None,
            "R3": None,
        }
        # self.ip_ports ==
        self.primary = "R1"

        # stub for gRPC channel
        self.channel = None
        self.stub = None



        # configure server address, if on Jared's Mac, try 10.250.151.166
        try:
            self.handle_connect("1")
            self.handle_connect("2")
            self.handle_connect("3")
        except KeyboardInterrupt:
            print("\n[DISCONNECTED]")
            exit(0)

        print(self.ip_ports)

        try:
            # connect to primary replica
            self.leader_election()
            # create a gRPC channel + stub
            print(f"[LEADER] Connecting to {self.primary}...")
            addr = str(self.ip_ports[self.primary][0]) + ":" + str(self.ip_ports[self.primary][1])
            self.channel = grpc.insecure_channel(addr)
            self.stub = rpc.ChatServerStub(self.channel)

        except:
            print("Could not connect to primary server. Check ip and port addresses.")
            exit(0)


    def handle_connect(self, rn):
        while True:
            local = input(f"Are you running replica {rn} locally? (yes/no) ")
            if local.lower() == 'no':
                response = input(f"Server replica {rn} <IP address> <port>: ")
                self.ip_ports[f"R{rn}"] = response.split()
                break
            elif local.lower() == 'yes':
                response = input(f"Server replica {rn} <port>: ")
                self.ip_ports[f"R{rn}"] = [self.address, response]
                break
            else:
                continue
    
    # find the primary replica among current replicas, by choosing the least uuid
    # TODO: only perform leader election when the primary fails
    def leader_election(self):
        print("[Leader election] electing leader...")
        print(self.ip_ports)
        leader_uuid = ""
        original = self.primary
        for r in self.ip_ports:
            if self.ip_ports[r] is not None:
                uuid = str(self.ip_ports[r][0]) + "." + str(self.ip_ports[r][1])
                if leader_uuid == "":
                    leader_uuid = uuid
                    self.primary = r
                elif uuid < leader_uuid:
                    leader_uuid = uuid
                    self.primary = r

        if leader_uuid == "":
            print("No replicas available. Exiting...")
            exit(0)
        # elif original != self.primary:
        #     # replace the stub
        #     addr = str(self.ip_ports[self.primary][0]) + ":" + str(self.ip_ports[self.primary][1])
        #     channel = grpc.insecure_channel(addr)
        #     self.stub = rpc.ChatServerStub(channel)
        #     print(f"[Leader election] stub changed: {self.primary}")


    # call to start everything: listening thread and the input thread
    def start(self):
        # create new listening thread for when new message streams come in
        threading.Thread(target=self.__listen_for_messages, daemon=True).start()
        # threading.Thread(target=self.__listen_for_updates, daemon=True).start()
        threading.Thread(target=self.ping, daemon=True).start()
        self.communicate_with_server()


    # listening thread for incoming messages from other users
    def __listen_for_messages(self):
        # TODO: check the type of message. If new replica, store it
        for note in self.stub.ChatStream(chat.Empty()):
            print(">[{}] {}".format(note.sender, note.message))


    # TODO: make the current replica None, then switch to another replica
    def switch_replica(self, new_server=False):
        print("[switch replica] switching replica from " + self.primary)

        if not new_server:
            self.ip_ports[self.primary] = None
            self.primary = None

        self.leader_election()
        
        try:
            addr = str(self.ip_ports[self.primary][0]) + ":" + str(self.ip_ports[self.primary][1])
            self.stub = None
            self.channel.close()
            self.channel = grpc.insecure_channel(addr)
            self.stub = rpc.ChatServerStub(self.channel)

            print("[switch replica] stub changed! ")
        except:
            # try another replica
            print("[switch replica] can't connect to replica; trying another replica...")
            self.switch_replica()


    # Pings primary replica to check if it is alive
    # Everytime ping: listen for possible updates
    def ping(self):
        while True:
            # print("[Ping] Pinging primary replica...")
            time.sleep(3)

            try:
                print("[Ping] Pinging primary replica " + self.primary)
                # print(self.stub)
                response, status = self.stub.Ping.with_call(chat.Empty(), timeout=3)

                # check if there's replica update: if so, update ip_ports
                if response.change:
                    if response.new_server:
                        exist = False
                        for r in self.ip_ports:
                            if self.ip_ports[r] and str(response.port) == self.ip_ports[r][1]:
                                exist = True
                        if not exist:
                            for r in self.ip_ports:
                                if self.ip_ports[r] is None:
                                    self.ip_ports[r] = [response.ip, str(response.port)]
                                    print(f"[Ping] {r} added to ip_ports")
                                    print(self.ip_ports)   
                            self.switch_replica(new_server=True)
                    # secondary failed
                    else:
                        for r in self.ip_ports:
                            if (self.ip_ports[r] and 
                                self.ip_ports[r][0] == response.ip and 
                                self.ip_ports[r][1] == str(response.port)):
                                self.ip_ports[r] = None
                                print(f"[Ping] {r} removed from ip_ports")
                                print(self.ip_ports)
                print("End of Ping")

            except grpc.RpcError as e:
                print("[Ping] Primary replica failed. Trying another replica...")
                print("Error:")
                print(e)
                self.switch_replica()
                print("End of Ping")


    # send message to server then to receiver
    def send_message(self, user, message):
        n = chat.Note()
        n.version = 1
        n.operation_code = 0
        n.sender = self.username
        n.receiver = user
        n.message = message

        print(self.ip_ports)
        # get server response and print error message if unsuccessful
        # TODO: get ACK, if not, server has failed, so choose another replica
        # response = self.stub.SendNote(n)
        try:
            print("[primary: " + self.primary + "]")
            response, status = self.stub.SendNote.with_call(n, timeout=5)
            if not response.success:
                print(response.message)
                return False
            return True
        except grpc.RpcError as e:
            print("Server failed, trying another replica...")
            # if no server is available, exit. Else, resend message
            self.switch_replica()
            self.send_message(user, message)

    
    # register user
    def register_user(self):
        while True:
            register = input("Would you like to register for a new account? (yes/no) ")
            if register.lower() == 'yes':
                # register the user
                username = input("Username: ")
                if not username:
                    print("Username cannot be empty.")
                    continue
                # check that username doesn't contain ':'
                if ":" in username:
                    print("Username cannot contain ':'")
                    continue
                password = input("Password: ")

                re_password = input("Re-enter password: ")
                if password != re_password:
                    print("Passwords do not match.")
                    continue
                
                # send gRPC message for registering user
                n = chat.AccountInfo()
                n.username = username
                n.password = self.get_hashed_password(password)
                response = self.stub.CreateAccount(n)
                print(response.message)
                if response.success:
                    return True
                return False
            elif register.lower() == 'no':
                return False
    
    
    # login user provided by argument
    def login_user(self):
        while True:
            login = input("Would you like to log in? (yes/no) ")
            if login.lower() == 'yes':
                # log in the user
                username = input("Username: ")
                if not username:
                    print("Username cannot be empty.")
                    continue
                password = input("Password: ")
                n = chat.AccountInfo()
                n.username = username
                n.password = self.get_hashed_password(password)
                response = self.stub.Login(n)

                print(response.message)
                self.print_commands()
                if response.success:
                    self.username = username
                    return True
                else:
                    return False
            elif login.lower() == 'no':
                return False
    

    # logout user
    def logout(self):
        n = chat.Empty()
        response = self.stub.Logout(n)
        print(response.message)
        if response.success:
            self.username = ""


    # list all server accounts currently registered
    def list_accounts(self, magic_word):
        n = chat.AccountInfo()
        n.username = magic_word.strip()

        print("Current accounts:")
        for account in self.stub.ListAccounts(n):
            if not account.success:
                print("Account Listing Error")
                break
            print(account.message)
        print()
       

    # deletes an account, either provided by argument or current user
    def delete_account(self, account):
        n = chat.AccountInfo()
        if account:
            n.username = account
        else:
            n.username = self.username
        n.password = input(f"Password for account {n.username}: ")
        n.password = self.get_hashed_password(n.password)

        # get server response and print error message if unsuccessful, else print success message
        for response in self.stub.DeleteAccount(n):
            print(response.message)
            if not response.success:
                print("Account deletion failed.")
                return False
            elif response.success and n.username == self.username:
                self.username = ""
                print("Account deleted. You have been logged out.")
            elif response.success:
                print(f"Account {n.username} has been deleted.")
        return True
    

    # prints out the help menu
    def print_help(self):
        print("Commands:")
        print("\t./list <user>: list all users if <user> is empty, else list all users that contain <user>,")
        print("\t./register: register a new account,")
        print("\t./login: log in to an existing account,")
        print("\t./delete <user>: delete account <user> (<user> = current user by default),")
        print("\t./logout: disconnect from the server,")
        print("\t<user>: <message>: send a message to <user>.")


    # prints directional commands
    def print_commands(self):
        print("Commands: <user>: <message>, ./list, ./register, ./login, ./delete, ./logout. Type ./help for more info.")


    # disconnect from server
    def disconnect(self):
        self.logout()
        print("\nDisconnected from server.")
        exit(0)


    # get double-hashed password from an already hashed password
    def get_hashed_password(self, password):
        h = blake2b(key=CLIENT_KEY, digest_size=16)
        h.update(password.encode(FORMAT))
        return h.hexdigest()


    # communicate with server loop
    def communicate_with_server(self):
        # handle ctrl-z and ctrl-c
        signal.signal(signal.SIGTSTP, lambda x, y: self.disconnect())
        signal.signal(signal.SIGINT, lambda x, y: self.disconnect())

        # register user
        self.register_user()
        # login user
        logged_in = self.login_user()
        # unread is automatically loaded when user logs in
        
        while True:
            try: 
                message = input()
                if not message:
                    continue
                elif message[:8].lower() == "./delete":
                    self.delete_account(message[8:].strip().lower())
                elif message.lower() == "./help":
                    self.print_help()
                    pass
                elif message[:6].lower() == "./list":
                    # TODO: MAGIC WORD
                    self.list_accounts(message[7:].strip().lower())
                elif message.lower() == "./register":
                    successful = self.register_user()
                    time.sleep(0.5)
                    if not successful:
                        self.register_user()
                    # if not logged in and registered, login
                    elif not self.username and successful:
                        self.login_user()
                elif message.lower() == "./login":
                    self.login_user()
                elif message.lower() == "./logout":
                    self.logout()
                else:
                    firstColon = message.find(':')
                    if firstColon == -1:
                        print("Use: <user>: <message>")
                        continue
                    user = message[:firstColon]
                    message = message[firstColon + 1:]
                    self.send_message(user, message)
            except IOError as e:
                # ignore recoverable EAGAIN and EWOULDBLOCK error
                if e.errno == errno.EAGAIN and e.errno == errno.EWOULDBLOCK:
                    continue
                print('Reading error', str(e))
                self.disconnect()
            except Exception as e:
                print(e)
                self.disconnect()
    

if __name__ == '__main__':
    client = Client()  # this starts a client and thus a thread which keeps connection to server open
    client.start()