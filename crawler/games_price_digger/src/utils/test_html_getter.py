import os


class TestHTMLGetter:

    def __init__(self):
        file_directory = os.path.dirname(__file__)
        file_directory_path = os.path.abspath(file_directory)
        html_files_directory = os.path.join(
            file_directory_path,
            '../../static/tests/html'
        )
        self._html_files_directory = os.path.abspath(html_files_directory)

    def get_html_file_by_name(self, html_file_name: str) -> str:
        html_file_path = os.path.join(
            self._html_files_directory, html_file_name
        )
        does_file_exists = os.path.isfile(html_file_path)
        if not does_file_exists:
            raise FileNotFoundError(
                f'"{html_file_path}" was not found'
            )
        return html_file_path
