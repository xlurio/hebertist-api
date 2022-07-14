import os


class FileDeleter:

    def delete(self, file_path):
        os.remove(file_path)
