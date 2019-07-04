from space_api.response import Response
from space_api.transport import Transport


class FileStore:
    def __init__(self, transport: Transport):
        self.transport = transport

    def create_folder(self, path: str, name: str) -> Response:
        """
        Creates a folder at the specified location

        :param path: (str) The location in which the folder is to be added
        :param name: (str) The name of the folder
        :return: (Response) The response object containing values corresponding to the request
        """
        return self.transport.create_folder(path, name)

    def delete_file(self, path: str) -> Response:
        """
        Deletes a particular file

        :param path: (str) The location of the file to be deleted
        :return: (Response) The response object containing values corresponding to the request
        """
        return self.transport.delete_file(path)

    def list_files(self, path: str) -> Response:
        """
        List the files in a particular folder

        :param path: (str) The path of the folder to be searched
        :return: (Response) The response object containing values corresponding to the request
        """
        return self.transport.list_files(path)

    def upload_file(self, path: str, name: str, location: str) -> Response:
        """
        Uploads a particular file

        :param path: (str) The location in which the file needs to be uploaded
        :param name: (str) The name of the file to be created
        :param location: (str) The location of the file to read from
        :return: (Response) The response object containing values corresponding to the request
        """
        return self.transport.upload_file(path, name, open(location, "rb"))

    def download_file(self, path: str, location: str) -> Response:
        """
        Downloads a particular file

        :param path: (str) The location of the file which needs to be downloaded
        :param location: (str) The location (including name) of the file to write to
        :return: (Response) The response object containing values corresponding to the request
        """
        return self.transport.download_file(path, open(location, "wb"))


__all__ = ["FileStore"]
