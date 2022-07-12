from . import Game


class MetaGame(Game):

    def __init__(self, name: str, score: int, image: str):
        self._name = self._validate_name(name)
        self._score = score
        self._image = image

    def _validate_name(self, name: str) -> str:
        name = name.replace('\n', '')
        return self._clean_whitespaces(name)

    def _clean_whitespaces(self, text: str) -> str:
        cleaned_text = ''
        last_character_index = len(text) - 1

        for index in range(0, last_character_index):
            next_index = index + 1
            current_character = text[index]
            next_character = text[next_index]

            cleaned_text += self._check_for_chain_of_whitespace(
                current_character, next_character
            )

        return cleaned_text + text[-1]

    def _check_for_chain_of_whitespace(self,
                                       current_character: str,
                                       next_character: str) -> str:
        has_chain_of_whitespaces = (
            current_character == ' ' and next_character == ' '
        )

        if not has_chain_of_whitespaces:
            return current_character

        return ''

    def get_name(self):
        return self._name

    def get_score(self):
        return self._score

    def get_image(self):
        return self._image

    def get_data(self):
        return {
            'name': self._name,
            'score': self._score,
            'image': self._image,
        }

    def __str__(self) -> str:
        return (
            '{\n' +
            f'\tname: "{self._name}",\n' +
            f'\tscore: "{self._score}",\n' +
            f'\timage: "{self._image}",\n' +
            '}'
        )
