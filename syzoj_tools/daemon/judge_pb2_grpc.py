# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from . import judge_pb2 as judge__pb2


class JudgeStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.FetchTask = channel.unary_unary(
        '/Judge/FetchTask',
        request_serializer=judge__pb2.JudgeRequest.SerializeToString,
        response_deserializer=judge__pb2.FetchTaskResult.FromString,
        )
    self.SetTaskProgress = channel.stream_unary(
        '/Judge/SetTaskProgress',
        request_serializer=judge__pb2.TaskProgress.SerializeToString,
        response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
        )
    self.SetTaskResult = channel.unary_unary(
        '/Judge/SetTaskResult',
        request_serializer=judge__pb2.SetTaskResultMessage.SerializeToString,
        response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
        )


class JudgeServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def FetchTask(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def SetTaskProgress(self, request_iterator, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def SetTaskResult(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_JudgeServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'FetchTask': grpc.unary_unary_rpc_method_handler(
          servicer.FetchTask,
          request_deserializer=judge__pb2.JudgeRequest.FromString,
          response_serializer=judge__pb2.FetchTaskResult.SerializeToString,
      ),
      'SetTaskProgress': grpc.stream_unary_rpc_method_handler(
          servicer.SetTaskProgress,
          request_deserializer=judge__pb2.TaskProgress.FromString,
          response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
      ),
      'SetTaskResult': grpc.unary_unary_rpc_method_handler(
          servicer.SetTaskResult,
          request_deserializer=judge__pb2.SetTaskResultMessage.FromString,
          response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'Judge', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
