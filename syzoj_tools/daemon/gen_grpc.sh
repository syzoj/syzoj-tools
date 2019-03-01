#!/bin/sh

# Needs package: grpcio-tools
python3 -m grpc_tools.protoc -I. --python_out=. primitive.proto
python3 -m grpc_tools.protoc -I. --python_out=. tagger.proto
python3 -m grpc_tools.protoc -I. --python_out=. judge.proto
python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. judge_rpc.proto
