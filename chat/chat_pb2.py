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




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nchat.proto\x12\x04\x63hat\"\x07\n\x05\x45mpty\"b\n\x04Note\x12\x0f\n\x07version\x18\x01 \x01(\x05\x12\x16\n\x0eoperation_code\x18\x02 \x01(\x05\x12\x0e\n\x06sender\x18\x03 \x01(\t\x12\x10\n\x08receiver\x18\x04 \x01(\t\x12\x0f\n\x07message\x18\x05 \x01(\t\"2\n\x0eServerResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\"1\n\x0b\x41\x63\x63ountInfo\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\"*\n\x0eReplicaMessage\x12\n\n\x02ip\x18\x01 \x01(\t\x12\x0c\n\x04port\x18\x02 \x01(\x05\x32\xae\x03\n\nChatServer\x12\x39\n\x0bSendReplica\x12\x14.chat.ReplicaMessage\x1a\x14.chat.ServerResponse\x12\'\n\nChatStream\x12\x0b.chat.Empty\x1a\n.chat.Note0\x01\x12,\n\x08SendNote\x12\n.chat.Note\x1a\x14.chat.ServerResponse\x12\x38\n\rCreateAccount\x12\x11.chat.AccountInfo\x1a\x14.chat.ServerResponse\x12\x30\n\x05Login\x12\x11.chat.AccountInfo\x1a\x14.chat.ServerResponse\x12+\n\x06Logout\x12\x0b.chat.Empty\x1a\x14.chat.ServerResponse\x12\x39\n\x0cListAccounts\x12\x11.chat.AccountInfo\x1a\x14.chat.ServerResponse0\x01\x12:\n\rDeleteAccount\x12\x11.chat.AccountInfo\x1a\x14.chat.ServerResponse0\x01\x62\x06proto3')

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
  _ACCOUNTINFO._serialized_end=230
  _REPLICAMESSAGE._serialized_start=232
  _REPLICAMESSAGE._serialized_end=274
  _CHATSERVER._serialized_start=277
  _CHATSERVER._serialized_end=707
# @@protoc_insertion_point(module_scope)
