# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import chat_pb2 as chat__pb2


class ChatServerStub(object):
    """The ChatServer service definition.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SendReplica = channel.unary_unary(
                '/chat.ChatServer/SendReplica',
                request_serializer=chat__pb2.ReplicaMessage.SerializeToString,
                response_deserializer=chat__pb2.ServerResponse.FromString,
                )
        self.ChatStream = channel.unary_stream(
                '/chat.ChatServer/ChatStream',
                request_serializer=chat__pb2.Empty.SerializeToString,
                response_deserializer=chat__pb2.Note.FromString,
                )
        self.UpdateStream = channel.unary_unary(
                '/chat.ChatServer/UpdateStream',
                request_serializer=chat__pb2.Empty.SerializeToString,
                response_deserializer=chat__pb2.SystemUpdate.FromString,
                )
        self.SendNote = channel.unary_unary(
                '/chat.ChatServer/SendNote',
                request_serializer=chat__pb2.Note.SerializeToString,
                response_deserializer=chat__pb2.ServerResponse.FromString,
                )
        self.CreateAccount = channel.unary_unary(
                '/chat.ChatServer/CreateAccount',
                request_serializer=chat__pb2.AccountInfo.SerializeToString,
                response_deserializer=chat__pb2.ServerResponse.FromString,
                )
        self.Login = channel.unary_unary(
                '/chat.ChatServer/Login',
                request_serializer=chat__pb2.AccountInfo.SerializeToString,
                response_deserializer=chat__pb2.ServerResponse.FromString,
                )
        self.Logout = channel.unary_unary(
                '/chat.ChatServer/Logout',
                request_serializer=chat__pb2.Empty.SerializeToString,
                response_deserializer=chat__pb2.ServerResponse.FromString,
                )
        self.ListAccounts = channel.unary_stream(
                '/chat.ChatServer/ListAccounts',
                request_serializer=chat__pb2.AccountInfo.SerializeToString,
                response_deserializer=chat__pb2.ServerResponse.FromString,
                )
        self.DeleteAccount = channel.unary_stream(
                '/chat.ChatServer/DeleteAccount',
                request_serializer=chat__pb2.AccountInfo.SerializeToString,
                response_deserializer=chat__pb2.ServerResponse.FromString,
                )
        self.Ping = channel.unary_unary(
                '/chat.ChatServer/Ping',
                request_serializer=chat__pb2.Empty.SerializeToString,
                response_deserializer=chat__pb2.PingMessage.FromString,
                )
        self.PingServer = channel.unary_unary(
                '/chat.ChatServer/PingServer',
                request_serializer=chat__pb2.ServerResponse.SerializeToString,
                response_deserializer=chat__pb2.ServerResponse.FromString,
                )
        self.ChatSingle = channel.unary_unary(
                '/chat.ChatServer/ChatSingle',
                request_serializer=chat__pb2.Empty.SerializeToString,
                response_deserializer=chat__pb2.Note.FromString,
                )


class ChatServerServicer(object):
    """The ChatServer service definition.
    """

    def SendReplica(self, request, context):
        """bi-directional stream for chat streaming between server and client
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ChatStream(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateStream(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SendNote(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateAccount(self, request, context):
        """account creation
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Login(self, request, context):
        """account login
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Logout(self, request, context):
        """get unread
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListAccounts(self, request, context):
        """list accounts
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteAccount(self, request, context):
        """delete account
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Ping(self, request, context):
        """ping 
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def PingServer(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ChatSingle(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ChatServerServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SendReplica': grpc.unary_unary_rpc_method_handler(
                    servicer.SendReplica,
                    request_deserializer=chat__pb2.ReplicaMessage.FromString,
                    response_serializer=chat__pb2.ServerResponse.SerializeToString,
            ),
            'ChatStream': grpc.unary_stream_rpc_method_handler(
                    servicer.ChatStream,
                    request_deserializer=chat__pb2.Empty.FromString,
                    response_serializer=chat__pb2.Note.SerializeToString,
            ),
            'UpdateStream': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateStream,
                    request_deserializer=chat__pb2.Empty.FromString,
                    response_serializer=chat__pb2.SystemUpdate.SerializeToString,
            ),
            'SendNote': grpc.unary_unary_rpc_method_handler(
                    servicer.SendNote,
                    request_deserializer=chat__pb2.Note.FromString,
                    response_serializer=chat__pb2.ServerResponse.SerializeToString,
            ),
            'CreateAccount': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateAccount,
                    request_deserializer=chat__pb2.AccountInfo.FromString,
                    response_serializer=chat__pb2.ServerResponse.SerializeToString,
            ),
            'Login': grpc.unary_unary_rpc_method_handler(
                    servicer.Login,
                    request_deserializer=chat__pb2.AccountInfo.FromString,
                    response_serializer=chat__pb2.ServerResponse.SerializeToString,
            ),
            'Logout': grpc.unary_unary_rpc_method_handler(
                    servicer.Logout,
                    request_deserializer=chat__pb2.Empty.FromString,
                    response_serializer=chat__pb2.ServerResponse.SerializeToString,
            ),
            'ListAccounts': grpc.unary_stream_rpc_method_handler(
                    servicer.ListAccounts,
                    request_deserializer=chat__pb2.AccountInfo.FromString,
                    response_serializer=chat__pb2.ServerResponse.SerializeToString,
            ),
            'DeleteAccount': grpc.unary_stream_rpc_method_handler(
                    servicer.DeleteAccount,
                    request_deserializer=chat__pb2.AccountInfo.FromString,
                    response_serializer=chat__pb2.ServerResponse.SerializeToString,
            ),
            'Ping': grpc.unary_unary_rpc_method_handler(
                    servicer.Ping,
                    request_deserializer=chat__pb2.Empty.FromString,
                    response_serializer=chat__pb2.PingMessage.SerializeToString,
            ),
            'PingServer': grpc.unary_unary_rpc_method_handler(
                    servicer.PingServer,
                    request_deserializer=chat__pb2.ServerResponse.FromString,
                    response_serializer=chat__pb2.ServerResponse.SerializeToString,
            ),
            'ChatSingle': grpc.unary_unary_rpc_method_handler(
                    servicer.ChatSingle,
                    request_deserializer=chat__pb2.Empty.FromString,
                    response_serializer=chat__pb2.Note.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'chat.ChatServer', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ChatServer(object):
    """The ChatServer service definition.
    """

    @staticmethod
    def SendReplica(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/chat.ChatServer/SendReplica',
            chat__pb2.ReplicaMessage.SerializeToString,
            chat__pb2.ServerResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ChatStream(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/chat.ChatServer/ChatStream',
            chat__pb2.Empty.SerializeToString,
            chat__pb2.Note.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdateStream(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/chat.ChatServer/UpdateStream',
            chat__pb2.Empty.SerializeToString,
            chat__pb2.SystemUpdate.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SendNote(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/chat.ChatServer/SendNote',
            chat__pb2.Note.SerializeToString,
            chat__pb2.ServerResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CreateAccount(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/chat.ChatServer/CreateAccount',
            chat__pb2.AccountInfo.SerializeToString,
            chat__pb2.ServerResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Login(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/chat.ChatServer/Login',
            chat__pb2.AccountInfo.SerializeToString,
            chat__pb2.ServerResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Logout(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/chat.ChatServer/Logout',
            chat__pb2.Empty.SerializeToString,
            chat__pb2.ServerResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ListAccounts(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/chat.ChatServer/ListAccounts',
            chat__pb2.AccountInfo.SerializeToString,
            chat__pb2.ServerResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteAccount(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/chat.ChatServer/DeleteAccount',
            chat__pb2.AccountInfo.SerializeToString,
            chat__pb2.ServerResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Ping(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/chat.ChatServer/Ping',
            chat__pb2.Empty.SerializeToString,
            chat__pb2.PingMessage.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def PingServer(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/chat.ChatServer/PingServer',
            chat__pb2.ServerResponse.SerializeToString,
            chat__pb2.ServerResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ChatSingle(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/chat.ChatServer/ChatSingle',
            chat__pb2.Empty.SerializeToString,
            chat__pb2.Note.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
