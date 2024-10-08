# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import url_shortener_pb2 as url__shortener__pb2

GRPC_GENERATED_VERSION = '1.66.2'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in url_shortener_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class URLShortenerStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Shorten = channel.unary_unary(
                '/urlshortener.URLShortener/Shorten',
                request_serializer=url__shortener__pb2.ShortenRequest.SerializeToString,
                response_deserializer=url__shortener__pb2.ShortenResponse.FromString,
                _registered_method=True)
        self.Resolve = channel.unary_unary(
                '/urlshortener.URLShortener/Resolve',
                request_serializer=url__shortener__pb2.ResolveRequest.SerializeToString,
                response_deserializer=url__shortener__pb2.ResolveResponse.FromString,
                _registered_method=True)


class URLShortenerServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Shorten(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Resolve(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_URLShortenerServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Shorten': grpc.unary_unary_rpc_method_handler(
                    servicer.Shorten,
                    request_deserializer=url__shortener__pb2.ShortenRequest.FromString,
                    response_serializer=url__shortener__pb2.ShortenResponse.SerializeToString,
            ),
            'Resolve': grpc.unary_unary_rpc_method_handler(
                    servicer.Resolve,
                    request_deserializer=url__shortener__pb2.ResolveRequest.FromString,
                    response_serializer=url__shortener__pb2.ResolveResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'urlshortener.URLShortener', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('urlshortener.URLShortener', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class URLShortener(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Shorten(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/urlshortener.URLShortener/Shorten',
            url__shortener__pb2.ShortenRequest.SerializeToString,
            url__shortener__pb2.ShortenResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def Resolve(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/urlshortener.URLShortener/Resolve',
            url__shortener__pb2.ResolveRequest.SerializeToString,
            url__shortener__pb2.ResolveResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
