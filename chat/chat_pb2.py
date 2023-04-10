# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chat.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nchat.proto\x12\x04\x63hat\"\x07\n\x05\x45mpty\"b\n\x04Note\x12\x0f\n\x07version\x18\x01 \x01(\x05\x12\x16\n\x0eoperation_code\x18\x02 \x01(\x05\x12\x0e\n\x06sender\x18\x03 \x01(\t\x12\x10\n\x08receiver\x18\x04 \x01(\t\x12\x0f\n\x07message\x18\x05 \x01(\t\"2\n\x0eServerResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\"F\n\x0b\x41\x63\x63ountInfo\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\x12\x13\n\x0b\x63lient_addr\x18\x03 \x01(\t\"*\n\x0eReplicaMessage\x12\n\n\x02ip\x18\x01 \x01(\t\x12\x0c\n\x04port\x18\x02 \x01(\x05\"8\n\x0cSystemUpdate\x12\x0e\n\x06is_new\x18\x01 \x01(\x08\x12\n\n\x02ip\x18\x02 \x01(\t\x12\x0c\n\x04port\x18\x03 \x01(\x05\"b\n\x0bPingMessage\x12\x0e\n\x06\x63hange\x18\x01 \x01(\x08\x12\x12\n\nnew_server\x18\x02 \x01(\x08\x12\x15\n\rfailed_server\x18\x03 \x01(\x08\x12\n\n\x02ip\x18\x04 \x01(\t\x12\x0c\n\x04port\x18\x05 \x01(\x05\"\x1c\n\x0b\x44\x61taRequest\x12\r\n\x05query\x18\x01 \x01(\t\"\x1c\n\x0c\x44\x61taResponse\x12\x0c\n\x04rows\x18\x01 \x03(\t\"0\n\x0b\x46ileRequest\x12\x10\n\x08\x66ilename\x18\x01 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x02 \x01(\x0c\x32\x93\x06\n\nChatServer\x12\x39\n\x0bSendReplica\x12\x14.chat.ReplicaMessage\x1a\x14.chat.ServerResponse\x12\'\n\nChatStream\x12\x0b.chat.Empty\x1a\n.chat.Note0\x01\x12/\n\x0cUpdateStream\x12\x0b.chat.Empty\x1a\x12.chat.SystemUpdate\x12,\n\x08SendNote\x12\n.chat.Note\x1a\x14.chat.ServerResponse\x12\x38\n\rCreateAccount\x12\x11.chat.AccountInfo\x1a\x14.chat.ServerResponse\x12\x30\n\x05Login\x12\x11.chat.AccountInfo\x1a\x14.chat.ServerResponse\x12\x31\n\x06Logout\x12\x11.chat.AccountInfo\x1a\x14.chat.ServerResponse\x12\x39\n\x0cListAccounts\x12\x11.chat.AccountInfo\x1a\x14.chat.ServerResponse0\x01\x12:\n\rDeleteAccount\x12\x11.chat.AccountInfo\x1a\x14.chat.ServerResponse0\x01\x12,\n\x04Ping\x12\x11.chat.AccountInfo\x1a\x11.chat.PingMessage\x12\x38\n\nPingServer\x12\x14.chat.ServerResponse\x1a\x14.chat.ServerResponse\x12%\n\nChatSingle\x12\x0b.chat.Empty\x1a\n.chat.Note\x12\x32\n\x07GetData\x12\x11.chat.DataRequest\x1a\x12.chat.DataResponse\"\x00\x12\x37\n\x08SendFile\x12\x11.chat.FileRequest\x1a\x14.chat.ServerResponse\"\x00\x30\x01\x12\x30\n\x0b\x43hatHistory\x12\x11.chat.AccountInfo\x1a\n.chat.Note\"\x00\x30\x01\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'chat_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _EMPTY._serialized_start=20
  _EMPTY._serialized_end=27
  _NOTE._serialized_start=29
  _NOTE._serialized_end=127
  _SERVERRESPONSE._serialized_start=129
  _SERVERRESPONSE._serialized_end=179
  _ACCOUNTINFO._serialized_start=181
  _ACCOUNTINFO._serialized_end=251
  _REPLICAMESSAGE._serialized_start=253
  _REPLICAMESSAGE._serialized_end=295
  _SYSTEMUPDATE._serialized_start=297
  _SYSTEMUPDATE._serialized_end=353
  _PINGMESSAGE._serialized_start=355
  _PINGMESSAGE._serialized_end=453
  _DATAREQUEST._serialized_start=455
  _DATAREQUEST._serialized_end=483
  _DATARESPONSE._serialized_start=485
  _DATARESPONSE._serialized_end=513
  _FILEREQUEST._serialized_start=515
  _FILEREQUEST._serialized_end=563
  _CHATSERVER._serialized_start=566
  _CHATSERVER._serialized_end=1353
# @@protoc_insertion_point(module_scope)
