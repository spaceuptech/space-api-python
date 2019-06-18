import json


class Response:
    """
    The Response class
    Contains: status, error, result

    :param response: (space_api.proto.server_pb2.Response) gRPC Response
    """

    def __init__(self, response):
        self.status = response.status
        self.error = response.error if len(response.error) > 0 else None
        self.result = json.loads(response.result) if len(response.result) > 0 else None

    def __str__(self) -> str:
        return f'Response(status={self.status}, error={self.error}, result={self.result})'


__all__ = ["Response"]
