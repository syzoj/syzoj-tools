# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: judge_rpc.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from . import primitive_pb2 as primitive__pb2
from . import judge_pb2 as judge__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='judge_rpc.proto',
  package='syzoj.judge.rpc',
  syntax='proto2',
  serialized_options=_b('Z,github.com/syzoj/syzoj-ng-go/app/core/protos'),
  serialized_pb=_b('\n\x0fjudge_rpc.proto\x12\x0fsyzoj.judge.rpc\x1a\x1bgoogle/protobuf/empty.proto\x1a\x0fprimitive.proto\x1a\x0bjudge.proto\"R\n\x0cJudgeRequest\x12,\n\tjudger_id\x18\x03 \x01(\x0b\x32\x19.syzoj.primitive.ObjectID\x12\x14\n\x0cjudger_token\x18\x02 \x01(\t\"G\n\x0f\x46\x65tchTaskResult\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12#\n\x04task\x18\x02 \x01(\x0b\x32\x15.syzoj.judge.rpc.Task\"x\n\x04Task\x12\x10\n\x08task_tag\x18\x01 \x01(\x03\x12-\n\nproblem_id\x18\x05 \x01(\x0b\x32\x19.syzoj.primitive.ObjectID\x12/\n\x07\x63ontent\x18\x06 \x01(\x0b\x32\x1e.syzoj.judge.SubmissionContent\"\x0e\n\x0cTaskProgress\"\x9b\x01\n\x14SetTaskResultMessage\x12,\n\tjudger_id\x18\x05 \x01(\x0b\x32\x19.syzoj.primitive.ObjectID\x12\x14\n\x0cjudger_token\x18\x02 \x01(\t\x12\x10\n\x08task_tag\x18\x03 \x01(\x03\x12-\n\x06result\x18\x06 \x01(\x0b\x32\x1d.syzoj.judge.SubmissionResult2\xf7\x01\n\x05Judge\x12N\n\tFetchTask\x12\x1d.syzoj.judge.rpc.JudgeRequest\x1a .syzoj.judge.rpc.FetchTaskResult\"\x00\x12L\n\x0fSetTaskProgress\x12\x1d.syzoj.judge.rpc.TaskProgress\x1a\x16.google.protobuf.Empty\"\x00(\x01\x12P\n\rSetTaskResult\x12%.syzoj.judge.rpc.SetTaskResultMessage\x1a\x16.google.protobuf.Empty\"\x00\x42.Z,github.com/syzoj/syzoj-ng-go/app/core/protos')
  ,
  dependencies=[google_dot_protobuf_dot_empty__pb2.DESCRIPTOR,primitive__pb2.DESCRIPTOR,judge__pb2.DESCRIPTOR,])




_JUDGEREQUEST = _descriptor.Descriptor(
  name='JudgeRequest',
  full_name='syzoj.judge.rpc.JudgeRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='judger_id', full_name='syzoj.judge.rpc.JudgeRequest.judger_id', index=0,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='judger_token', full_name='syzoj.judge.rpc.JudgeRequest.judger_token', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=95,
  serialized_end=177,
)


_FETCHTASKRESULT = _descriptor.Descriptor(
  name='FetchTaskResult',
  full_name='syzoj.judge.rpc.FetchTaskResult',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='success', full_name='syzoj.judge.rpc.FetchTaskResult.success', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='task', full_name='syzoj.judge.rpc.FetchTaskResult.task', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=179,
  serialized_end=250,
)


_TASK = _descriptor.Descriptor(
  name='Task',
  full_name='syzoj.judge.rpc.Task',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='task_tag', full_name='syzoj.judge.rpc.Task.task_tag', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='problem_id', full_name='syzoj.judge.rpc.Task.problem_id', index=1,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='content', full_name='syzoj.judge.rpc.Task.content', index=2,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=252,
  serialized_end=372,
)


_TASKPROGRESS = _descriptor.Descriptor(
  name='TaskProgress',
  full_name='syzoj.judge.rpc.TaskProgress',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=374,
  serialized_end=388,
)


_SETTASKRESULTMESSAGE = _descriptor.Descriptor(
  name='SetTaskResultMessage',
  full_name='syzoj.judge.rpc.SetTaskResultMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='judger_id', full_name='syzoj.judge.rpc.SetTaskResultMessage.judger_id', index=0,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='judger_token', full_name='syzoj.judge.rpc.SetTaskResultMessage.judger_token', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='task_tag', full_name='syzoj.judge.rpc.SetTaskResultMessage.task_tag', index=2,
      number=3, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='result', full_name='syzoj.judge.rpc.SetTaskResultMessage.result', index=3,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=391,
  serialized_end=546,
)

_JUDGEREQUEST.fields_by_name['judger_id'].message_type = primitive__pb2._OBJECTID
_FETCHTASKRESULT.fields_by_name['task'].message_type = _TASK
_TASK.fields_by_name['problem_id'].message_type = primitive__pb2._OBJECTID
_TASK.fields_by_name['content'].message_type = judge__pb2._SUBMISSIONCONTENT
_SETTASKRESULTMESSAGE.fields_by_name['judger_id'].message_type = primitive__pb2._OBJECTID
_SETTASKRESULTMESSAGE.fields_by_name['result'].message_type = judge__pb2._SUBMISSIONRESULT
DESCRIPTOR.message_types_by_name['JudgeRequest'] = _JUDGEREQUEST
DESCRIPTOR.message_types_by_name['FetchTaskResult'] = _FETCHTASKRESULT
DESCRIPTOR.message_types_by_name['Task'] = _TASK
DESCRIPTOR.message_types_by_name['TaskProgress'] = _TASKPROGRESS
DESCRIPTOR.message_types_by_name['SetTaskResultMessage'] = _SETTASKRESULTMESSAGE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

JudgeRequest = _reflection.GeneratedProtocolMessageType('JudgeRequest', (_message.Message,), dict(
  DESCRIPTOR = _JUDGEREQUEST,
  __module__ = 'judge_rpc_pb2'
  # @@protoc_insertion_point(class_scope:syzoj.judge.rpc.JudgeRequest)
  ))
_sym_db.RegisterMessage(JudgeRequest)

FetchTaskResult = _reflection.GeneratedProtocolMessageType('FetchTaskResult', (_message.Message,), dict(
  DESCRIPTOR = _FETCHTASKRESULT,
  __module__ = 'judge_rpc_pb2'
  # @@protoc_insertion_point(class_scope:syzoj.judge.rpc.FetchTaskResult)
  ))
_sym_db.RegisterMessage(FetchTaskResult)

Task = _reflection.GeneratedProtocolMessageType('Task', (_message.Message,), dict(
  DESCRIPTOR = _TASK,
  __module__ = 'judge_rpc_pb2'
  # @@protoc_insertion_point(class_scope:syzoj.judge.rpc.Task)
  ))
_sym_db.RegisterMessage(Task)

TaskProgress = _reflection.GeneratedProtocolMessageType('TaskProgress', (_message.Message,), dict(
  DESCRIPTOR = _TASKPROGRESS,
  __module__ = 'judge_rpc_pb2'
  # @@protoc_insertion_point(class_scope:syzoj.judge.rpc.TaskProgress)
  ))
_sym_db.RegisterMessage(TaskProgress)

SetTaskResultMessage = _reflection.GeneratedProtocolMessageType('SetTaskResultMessage', (_message.Message,), dict(
  DESCRIPTOR = _SETTASKRESULTMESSAGE,
  __module__ = 'judge_rpc_pb2'
  # @@protoc_insertion_point(class_scope:syzoj.judge.rpc.SetTaskResultMessage)
  ))
_sym_db.RegisterMessage(SetTaskResultMessage)


DESCRIPTOR._options = None

_JUDGE = _descriptor.ServiceDescriptor(
  name='Judge',
  full_name='syzoj.judge.rpc.Judge',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=549,
  serialized_end=796,
  methods=[
  _descriptor.MethodDescriptor(
    name='FetchTask',
    full_name='syzoj.judge.rpc.Judge.FetchTask',
    index=0,
    containing_service=None,
    input_type=_JUDGEREQUEST,
    output_type=_FETCHTASKRESULT,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='SetTaskProgress',
    full_name='syzoj.judge.rpc.Judge.SetTaskProgress',
    index=1,
    containing_service=None,
    input_type=_TASKPROGRESS,
    output_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='SetTaskResult',
    full_name='syzoj.judge.rpc.Judge.SetTaskResult',
    index=2,
    containing_service=None,
    input_type=_SETTASKRESULTMESSAGE,
    output_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_JUDGE)

DESCRIPTOR.services_by_name['Judge'] = _JUDGE

# @@protoc_insertion_point(module_scope)
