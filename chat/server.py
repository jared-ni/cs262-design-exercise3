from concurrent import futures
import grpc
import time
import chat_pb2 as chat
import chat_pb2_grpc as rpc
from collections import deque
import threading
import bcrypt
import socket
import errno
import sys
import sqlite3


class MyContextWrapper:
    def __init__(self, context):
        self.context = context

    def peer(self):
        # Return the original peer address
        return self.context.peer()


# Chat Server class for handling gRPC connected clients and their requests
class ChatServer(rpc.ChatServerServicer):

    def __init__(self, port):
        # List with all the chat history
        self.users = {}
        # maps context.peer() to username
        self.clients = {}
        # thread locks for preventing race conditions in users and clients
        self.users_lock = threading.Lock()
        self.clients_lock = threading.Lock()

        # system updates
        self.system_updates = deque()
        
        # TODO: connect to other servers
        self.address = socket.gethostbyname(socket.gethostname())
        self.port = port
        self.ip_ports = {
            "self": (self.address, port),
            "R1": None,
            "R2": None,
        }
        self.replica_stubs = {
            "R1": None,
            "R2": None,
        }
        self.primary = "self"

        self.sync_lock = threading.Lock()
        self.synced = False

        # TODO: add server replicas
        prior_replicas = 0
        while True:
            prior_replicas  = int(input("How many replicas are currently running besides this one? (0, 1, or 2): "))
            if 0 <= prior_replicas <= 2:
                break
            else:
                print("Invalid number of prior replicas (must be 0, 1, or 2)")
        

        # connect prior replicas
        def handle_connect(rn):
            while True:
                local = input(f"Are you running replica {rn} locally? (yes/no) ")
                if local.lower() == 'no':
                    response = input(f"Server replica {rn} <IP address> <port>: ")
                    ip, port = response.split()
                    self.ip_ports[f"R{rn}"] = (ip, int(port))
                    break
                elif local.lower() == 'yes':
                    response = input(f"Server replica {rn} <port>: ")
                    self.ip_ports[f"R{rn}"] = (self.address, response)
                    break
                else:
                    continue
        
        try: 

            print("Server address:", self.address)
            print("Server port:", self.port)
            print(self.ip_ports)

            # TODO: add database

            # add commit log 
            with open(f"commit_{self.address}_{self.port}.txt", "a") as f:
                f.write("")
            
            self.db = sqlite3.connect(f"chat_{self.port}.db", check_same_thread=False)
            self.cursor = self.db.cursor()
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS users(username text, password text)''')
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS chat_history (sender text, receiver text, message text)''')
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS unread (sender text, receiver text, message text)''')
            # make counter_name unique
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS commit_count (count integer, counter_name text UNIQUE)''')
            # add a row named "counter" to commit_count table if it doesn't exist
            self.cursor.execute('''INSERT OR IGNORE INTO commit_count (count, counter_name) VALUES (0, "counter")''')
            self.db.commit()


            for i in range(1, prior_replicas + 1):
                handle_connect(i)
                # connect to replica
                addr = str(self.ip_ports[f"R{i}"][0]) + ":" + str(self.ip_ports[f"R{i}"][1])
                channel = grpc.insecure_channel(addr)
                self.replica_stubs[f"R{i}"] = rpc.ChatServerStub(channel)
                print("Connected to prior replica", i)

            # send current ip and port to prior replicas
            print("checkpoint: got to replica_message")
            self.replica_message()
        except:
            print("Could not connect to server. Check ip and port addresses.")
            exit(0)

        # start thread to detect failures
        threading.Thread(target=self.detect_failure, daemon=True).start()


        # sync commit logs with replicas
        self.sync_commits()


    def sync_commits(self):
        for rep in self.ip_ports:
            if self.ip_ports[rep] is not None and rep != "self":
                addr, port = self.ip_ports[rep]
                stub = self.replica_stubs[rep]
                self.receive_file(stub, f"commit_{addr}_{port}.txt")
     
        
    def receive_file(self, stub, filename):
        # try:
        print("Receiving file", filename)
        request = chat.FileRequest(filename=filename)
        response_iterator = stub.SendFile(request)

        print(response_iterator)

        # get last commit number
        self.cursor.execute("SELECT count FROM commit_count WHERE counter_name = 'counter'")
        counter = int(self.cursor.fetchone()[0])

        for res in response_iterator:
            commit_num, commit = res.message.split("~")
            commit = str(commit)

            print("commit_num:", commit_num)
            print("commit:", commit)

            if int(commit_num) > counter:
                with open(f"commit_{self.address}_{self.port}.txt", "a") as f:
                    f.write(f"{commit_num}~{commit}")

                self.cursor.execute(f'''{commit}''')
                self.db.commit()
                counter = int(commit_num)
                self.cursor.execute("UPDATE commit_count SET count = count + 1 WHERE counter_name = 'counter'")
                self.db.commit()
    

    def SendFile(self, request, context):
        with open(request.filename, 'r') as f:
            for line in f:
                response = chat.ServerResponse(success=True, message=line)
                yield response
        

    # periodically check if replicas are still alive
    def detect_failure(self):
        print("[Detect failure] Started thread to detect failures")
        while True:
            time.sleep(1)
            for rep in self.replica_stubs:
                if self.replica_stubs[rep] is not None:
                    try:
                        response, status = self.replica_stubs[rep].PingServer.with_call(chat.ServerResponse(message=str(self.port)), timeout=1)
                    except grpc.RpcError as e:
                        print(f"[Detect failure] Could not connect to replica {rep}")
                        print(e)
                        # TODO: inform client replica failed
                        failed_replica = self.ip_ports[rep]
                        self.ip_ports[rep] = None
                        self.replica_stubs[rep] = None

                        # leader election only if the failed replica was the primary
                        if rep == self.primary:
                            self.primary = "self"
                            self.leader_election()

                        # inform clients of failed replica if current replica is primary
                        if self.primary == "self":
                            self.inform_client_new_replica(failed_replica, is_new=False)


    # only if new update, primary update the client
    def Ping(self, request: chat.AccountInfo(), context):
        # print("[Ping] Received ping")
        print("ping: " + request.username)
        if request.username in self.users and context.peer() not in self.clients:
            current_user = request.username
            # change client address
            with self.clients_lock:
                for client in self.clients:
                    if self.clients[client] == current_user:
                        del self.clients[client]
                        break
                self.clients[context.peer()] = current_user
            # change user address
            with self.users_lock:
                self.users[current_user]['address'] = context.peer()


        if len(self.system_updates) > 0:
            update = self.system_updates.popleft()
            return chat.PingMessage(change=True, new_server=update.is_new, ip=update.ip, port=update.port)

        return chat.PingMessage(change=False, new_server=False)
    

    def PingServer(self, request: chat.ServerResponse(), context):
        # print(f"[Server Ping] Received ping from {request.message}")

        # if not synced, sync
        if not self.synced:
            self.sync_commits()
            with self.sync_lock:
                self.synced = True

        return chat.ServerResponse(success=True, message="Pong")


    # find the primary replica among current replicas, by choosing the least uuid
    def leader_election(self):
        print("[Leader election] Starting leader election: " + self.primary)
        # must start with self; don't know if primary failed or not
        leader_uuid = str(self.ip_ports["self"][0]) + "." + str(self.ip_ports["self"][1])
        for r in self.ip_ports:
            if self.ip_ports[r] is not None:
                uuid = str(self.ip_ports[r][0]) + "." + str(self.ip_ports[r][1])
                if uuid < leader_uuid:
                    leader_uuid = uuid
                    self.primary = r
        print("[Leader election] New primary replica: " + self.primary)
        

    def replica_message(self):
        print("[Replica message] Sending replica message")
        n = chat.ReplicaMessage(ip=self.address, port=self.port)
        for rep in self.replica_stubs:
            if self.replica_stubs[rep] is not None:
                response = self.replica_stubs[rep].SendReplica(n)
                print("[Replica message] Sent replica message to", rep)
        self.leader_election()


    # TODO: add message function bewteen replicas
    def SendReplica(self, request: chat.ReplicaMessage, context):
        # fill in a None replica
        for rep in self.ip_ports:
            if self.ip_ports[rep] is None:
                self.ip_ports[rep] = (request.ip, request.port)
                # connect to replica
                addr = str(self.ip_ports[rep][0]) + ":" + str(self.ip_ports[rep][1])
                channel = grpc.insecure_channel(addr)
                self.replica_stubs[rep] = rpc.ChatServerStub(channel)
                print("[SendReplica] Connected to replica")
                print(self.ip_ports)

                if self.primary == "self":
                    self.inform_client_new_replica(self.ip_ports[rep], is_new=True)

                break
        
        print("[SendReplica] leader election")
        self.leader_election()

        with self.sync_lock:
            self.synced = False

        return chat.ServerResponse(success=True, message="Replica added")


    # hash password again for storage
    def hash_password(self, password):
        # return bcrypt.hashpw(password.encode(FORMAT), bcrypt.gensalt())
        return password


    # return true if password matches hashed password
    def check_password(self, password, hashed_password):
        # print(hashed_password)
        # return bcrypt.checkpw(password.encode(FORMAT), hashed_password)
        return password == hashed_password


    def inform_client_new_replica(self, replica, is_new=True):
        update = chat.SystemUpdate()
        update.ip = replica[0]
        update.port = int(replica[1])
        update.is_new = is_new
        self.system_updates.append(update)
        print("[Inform client] Informing clients of new replica")


    def ChatSingle(self, request, context):
        user = None
        if context.peer() in self.clients:
            user = self.clients[context.peer()]
        # if not user:
        #     return chat.ServerResponse(success=False, message="[SERVER] Error sending message")
        
        
        # Check if there are any new messages if logged in
        if user in self.users and len(self.users[user]['unread']) > 0:
            message = self.users[user]['unread'].popleft()
            return message
        else:
            return chat.Note(operation_code=10)


        # except IOError as e:
        #     # ignore recoverable EAGAIN and EWOULDBLOCK error
        #     if e.errno == errno.EAGAIN and e.errno == errno.EWOULDBLOCK:
        #         continue
        # except Exception as e:
        #     print(e)
        #     yield chat.ServerResponse(success=False, message="[SERVER] Error sending message")
                

    # TODO: must save login info to database
    # Send a message to the server then to the receiver
    def SendNote(self, request: chat.Note, context):
        # try: 
        print("[SendNote] Received message: ", request.message)
        # check version
        if request.version != 1:
            return chat.ServerResponse(success=False, message="[SERVER] Version mismatch")
        if request.sender == "":
            return chat.ServerResponse(success=False, message="[SERVER] You are not logged in")
        
        # check if the user is logged in
        current_user = None
        if context.peer() in self.clients:
            current_user = self.clients[context.peer()]
        
        # check if the username is in the current usernames
        elif request.sender in self.users:

            current_user = request.sender
            # change client address
            with self.clients_lock:
                for client in self.clients:
                    if self.clients[client] == current_user:
                        del self.clients[client]
                        break
                self.clients[context.peer()] = current_user
            # change user address
            with self.users_lock:
                self.users[current_user]['address'] = context.peer()
            
        if current_user is None or not current_user:
            return chat.ServerResponse(success=False, message="[SERVER] You are not logged in")

        # Check if the receiver exists in the database
        self.cursor.execute("SELECT * FROM users WHERE username = ?", (request.receiver,))
        receiver = self.cursor.fetchone()
        if receiver is None:
            return chat.ServerResponse(success=False, message="[SERVER] User does not exist")
        

        # send the same message to other replica
        print("primary: " + self.primary)

        if self.primary == "self":
            for rep in self.replica_stubs:
                if self.replica_stubs[rep] is not None:
                    self.replica_stubs[rep].SendNote(request)

        # commit to database
        self.cursor.execute("INSERT INTO chat_history (sender, receiver, message) VALUES (?, ?, ?)", 
                            (request.sender, request.receiver, request.message))
        # increment counter in database
        self.cursor.execute("UPDATE commit_count SET count = count + 1 WHERE counter_name = 'counter'")
        self.db.commit()

        # get counter
        self.cursor.execute("SELECT count FROM commit_count WHERE counter_name = 'counter'")
        counter = self.cursor.fetchone()[0]

        # log into the commit log
        with open(f"commit_{self.address}_{self.port}.txt", "a") as f:
            f.write(f"{counter}~INSERT INTO chat_history (sender, receiver, message) VALUES ('{request.sender}', '{request.receiver}', '{request.message}')\n")
        

        # append to unread
        if self.primary == "self":
            if request.receiver in self.users:
                with self.users_lock:
                    self.users[request.receiver]['unread'].append(request)
            else:
                # push to unread database if user is not logged in
                self.cursor.execute("INSERT INTO unread (sender, receiver, message) VALUES (?, ?, ?)", 
                                    (current_user, request.receiver, request.message))
                self.db.commit()


        return chat.ServerResponse(success=True, message="")
        
        # except Exception as e:
        #     print(e)
        #     return chat.ServerResponse(success=False, message="[SERVER] Error sending message")
    
    
    # Acount Creaton
    def CreateAccount(self, request: chat.AccountInfo, context):
        # try: 
        # Check if the username is already taken in db
        self.cursor.execute('''SELECT * FROM users WHERE username = ?''', (request.username,))
        user = self.cursor.fetchone()
        if user or request.username in self.users:
            return chat.ServerResponse(success=False, message="[SERVER] Username already taken")

        # Create the account
        with self.users_lock:
            self.users[request.username] = {
                "password": self.hash_password(request.password), 
                "client": None,
                "logged_in": False,
                "unread": deque()
            }

        # insert into database
        self.cursor.execute('''INSERT INTO users (username, password) VALUES (?, ?)''', 
                            (request.username, self.hash_password(request.password)))

        # increment counter in database
        self.cursor.execute("UPDATE commit_count SET count = count + 1 WHERE counter_name = 'counter'")
        self.db.commit()

        # get counter
        self.cursor.execute("SELECT count FROM commit_count WHERE counter_name = 'counter'")
        counter = self.cursor.fetchone()[0]

        # log into the commit log
        with open(f"commit_{self.address}_{self.port}.txt", "a") as f:
            f.write(f"{counter}~INSERT INTO users (username, password) VALUES ('{request.username}', '{self.hash_password(request.password)}')\n")
        

        # send to other replica
        if self.primary == "self":
            for rep in self.replica_stubs:
                if self.replica_stubs[rep] is not None:
                    self.replica_stubs[rep].CreateAccount(request)


        return chat.ServerResponse(success=True, message=f"[SERVER] Account {request.username} created")
        
        # except Exception as e:
        #     print(e)
        #     return chat.ServerResponse(success=False, message="[SERVER] Error creating account")
    

    # Account Login: a client must be logged in on one device at a time, else they are logged out of previous device
    def Login(self, request: chat.AccountInfo(), context):
        # try: 
        # Check if the username exists
        # check if username exists in database
        self.cursor.execute("SELECT * FROM users WHERE username = ?", (request.username,))
        user = self.cursor.fetchone()

        if user is None:
            return chat.ServerResponse(success=False, message="[SERVER] Username does not exist")

        # Check if the password is correct in database
        if not self.check_password(request.password, user[1]):
            return chat.ServerResponse(success=False, message="[SERVER] Incorrect password")
        
        # warn previous client of the user account if logged in on new client

        client_addr = context.peer() if self.primary == "self" else request.client_addr

        if request.username in self.users and self.users[request.username]["client"] is not None:
            detection = chat.Note(message = f"Logged out: detected {request.username} login on another client.")
            self.users[request.username]["unread"].append(detection)
            # wait for previous client to get message
            time.sleep(1)
            prev_client = self.users[request.username]["client"]
            with self.clients_lock:
                self.clients[prev_client] = None
            
        # # Logout previous user
        if client_addr in self.clients and self.clients[client_addr] is not None:
            prev_user = self.clients[client_addr]
            with self.users_lock:
                self.users[prev_user]["logged_in"] = False
                self.users[prev_user]["client"] = None

        with self.clients_lock:
            self.clients[client_addr] = request.username
        with self.users_lock:
            if request.username in self.users:
                self.users[request.username]['client'] = client_addr
                self.users[request.username]['logged_in'] = True
            else:
                self.users[request.username] = {
                    "client": client_addr,
                    "logged_in": True,
                    "unread": deque()
                }
                # push unread messages to user
                self.cursor.execute("SELECT * FROM unread WHERE receiver = ?", (request.username,))
                unread = self.cursor.fetchall()
                for msg in unread:
                    self.users[request.username]['unread'].append(chat.Note(
                        sender=msg[0], receiver=msg[1], message=msg[2]
                    ))
                    # delete unread messages from database
                    self.cursor.execute("DELETE FROM unread WHERE sender = ? AND receiver = ? AND message = ?", 
                                        (msg[0], msg[1], msg[2]))
                    self.db.commit()


        # successfully logged in
        # login on replicas 
        new_request = chat.AccountInfo(username=request.username, 
                                       password=request.password, 
                                       client_addr=client_addr)

        if self.primary == "self":
            for rep in self.replica_stubs:
                if self.replica_stubs[rep] is not None:
                    replica_response = self.replica_stubs[rep].Login(new_request)
                    print("replica response: ")
                    print(replica_response)

        # commit log
        # if self.primary == "self":
        #     with open (f"commits_{self.address}_{self.port}.txt", "a") as commit_file:
        #         commit_file.write(f"login~{context.peer()}~{request.username}~{request.password}\n")


        return chat.ServerResponse(success=True, message=f"[SERVER] Logged in as {request.username}")
        
        # except Exception as e:
        #     print(e)
        #     return chat.ServerResponse(success=False, message="[SERVER] Error logging in")


    # Account Logout of the current client
    def Logout(self, request: chat.Empty, context):
        
        # Check if the username exists
        current_user = None
        if context.peer() in self.clients:
            current_user = self.clients[context.peer()]

        # check if the username is in the current usernames
        elif request.username in self.users:
            current_user = request.sender
            # change client address
            with self.clients_lock:
                for client in self.clients:
                    if self.clients[client] == current_user:
                        del self.clients[client]
                        break
                self.clients[context.peer()] = current_user
            # change user address
            with self.users_lock:
                self.users[current_user]['address'] = context.peer()
            
        if current_user is None or not current_user:
            return chat.ServerResponse(success=False, message="[SERVER] You are not logged in")

        
        # Logout the user: change both users and clients dicts
        username = self.clients[context.peer()]
        with self.users_lock:
            self.users[username]['logged_in'] = False
            self.users[username]['client'] = None
        with self.clients_lock:
            self.clients[context.peer()] = None

        # logout on replicas
        if self.primary == "self":
            for rep in self.replica_stubs:
                if self.replica_stubs[rep] is not None:
                    self.replica_stubs[rep].Logout(request)

        # commit log
        # if self.primary == "self":
        #     with open (f"commits_{self.address}_{self.port}.txt", "a") as commit_file:
        #         commit_file.write(f"logout~{context.peer()}\n")


        return chat.ServerResponse(success=True, message=f"[SERVER] Logged out of user {username}")


    # Account list
    def ListAccounts(self, request: chat.AccountInfo, context):
        # list all accounts in data
        self.cursor.execute("SELECT username FROM users")
        for user in self.cursor.fetchall():
            if request.username == "*" or not request.username or request.username in user:
                yield chat.ServerResponse(success=True, message=f"{user[0]}")


    # Account delete
    def DeleteAccount(self, request: chat.AccountInfo, context):
        # try: 
        # Check if the username exists: return if not
        # get all users from database
        self.cursor.execute("SELECT * FROM users WHERE username = ?", (request.username,))
        user = self.cursor.fetchone()
        print()
        if not user:
            yield chat.ServerResponse(success=False, message="[SERVER] Username does not exist")
            return
        
        # # Check if the password is correct: return if incorrect
        if not self.check_password(request.password, user[1]):
            yield chat.ServerResponse(success=False, message=f"[SERVER] Incorrect password for account {request.username}")
            return
        

        # delete on replicas
        if self.primary == "self":
            for rep in self.replica_stubs:
                if self.replica_stubs[rep] is not None:
                    self.replica_stubs[rep].DeleteAccount(request)

        # Yield success message before actual deletion so user can be logout
        yield chat.ServerResponse(success=True, message="")  
        # warn the currently logged in client on the deleted account
        print(self.users)
        
        # no need to warn a person that's logged out on a new replica
        prev_client = self.users[request.username]["client"]
        if prev_client is not None:
            detection = chat.Note(message = f"Logged out: account {request.username} has been deleted.")
            with self.users_lock:
                self.users[request.username]["unread"].append(detection)
            with self.clients_lock:
                self.clients[prev_client] = None
        with self.users_lock:
            del self.users[request.username]
        

        # delete from database
        self.cursor.execute("DELETE FROM users WHERE username = ?", (request.username,))

        # increment counter in database
        self.cursor.execute("UPDATE commit_count SET count = count + 1 WHERE counter_name = 'counter'")
        self.db.commit()

        # get counter
        self.cursor.execute("SELECT count FROM commit_count WHERE counter_name = 'counter'")
        counter = self.cursor.fetchone()[0]

        # log into the commit log
        with open(f"commit_{self.address}_{self.port}.txt", "a") as f:
            f.write(f"{counter}~DELETE FROM users WHERE username = '{request.username}'\n")
        
        
        yield chat.ServerResponse(success=True, message=f"[SERVER] Account {request.username} deleted")
        return
        
        # except KeyError or ValueError:
        #     return chat.ServerResponse(success=False, message="[SERVER] Failed: make sure information is entered correctly")
        # except Exception as e:
        #     return chat.ServerResponse(success=False, message=f"[SERVER] Failed: {e}")


# main thread for handling clients
if __name__ == '__main__':
    FORMAT = "utf-8"

    # server port number must be specified as a command line argument
    if len(sys.argv) < 2:
        print('[SERVER ERROR] Usage: python server.py <port>')
        sys.exit(1)
    port = int(sys.argv[1])
                
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10)) 

    # create server object
    serverObject = ChatServer(port)

    rpc.add_ChatServerServicer_to_server(serverObject, server)
    print('[SERVER STARTING] Listening on port ' + str(port) + '...')

    addr_host = socket.gethostbyname(socket.gethostname())

    server.add_insecure_port(f'{addr_host}:{port}')
    server.start()


    server.wait_for_termination()