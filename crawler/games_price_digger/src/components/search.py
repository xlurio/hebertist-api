class Search:
    def __init__(self, game: str, store: str) -> None:
        self._game = game
        self._store = store

    def get_game(self):
        return self._game

    def get_store(self):
        return self._store

    def is_the_searched_game(self, game_found: str) -> bool:
        game_searched_letters = self._extract_letters_only(self._game)
        game_found_letters = self._extract_letters_only(game_found)
        return game_searched_letters == game_found_letters

    def _extract_letters_only(self, string_to_extract: str) -> str:
        new_string = ''.join([
            self._validate_character(character)
            for character in string_to_extract
        ])
        return new_string

    def _validate_character(self, character: str) -> str:
        invalid_characters = r'[@_!#$%^&*()<>?/\|}{~:]-™® '
        if character not in invalid_characters:
            return character.lower()
        return ''

    def __str__(self) -> str:
        return (
            '{\n'
            f'\tgame: {self._game},\n'
            f'\tstore: {self._store},\n'
            '}'
        )
