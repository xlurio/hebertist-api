import uuid
from . import NamingStrategy


class UUD4Naming(NamingStrategy):

    def get_filename(self, extension) -> str:
        filename = f'{uuid.uuid4()}.{extension}'
        return filename
