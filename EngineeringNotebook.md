# Engineering Notebook

## 03/06
We made the decision to use the gRPC implementation design problem 1 instead of our own defined protocol implementation using sockets because we feel that the abstraction and transparency of the sending and deciphering messages between server and client was efficient as it was not the focus on this design problem. We also thought that it would be easier to implement this abstraction meant that the code for the gRPC version could be easily kept more cleaner as we implemented replication with several servers and multiple clients. Overall, we went along with the gRPC version to implement replication because of the level of abstraction that hides away the details of message sending and receiving, which would ultimately make having to implement replication of this chat app easier, both as a coder and as a code reviewer.

## 03/07
We first went about trying to implement the system being 2-fault tolerant in the face of crash/failstop failures. We first initialized 3 servers/replicas, which knew each others port numbers such that they could communicate among one another. As per the advice of Varun during section, we decided to use the Master-Slave/Primaray-Secondary model for inter-server communication

We implemented a "ping" function that would send a messsage to other servers, checking if 