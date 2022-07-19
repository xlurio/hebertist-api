from games_price_digger.src.components.fake_model import FakeModel


class FakeGameModel(FakeModel):

    name = ''
    score = 0
    image = ''

    objects = None

    def __init__(self, name, score=0, image=''):
        self.name = name
        self.score = score
        self.image = image
        self._saved = False

    def save(self):
        self._saved = True

    def __str__(self):
        return (
            '{\n' +
            f'\tname: {self.name},\n' +
            f'\tscore: {self.score},\n' +
            f'\timage: {self.image}\n' +
            '}'
        )

    def __eq__(self, __o: object) -> bool:
        is_name_equal = self.name == __o.name
        is_score_equal = self.score == __o.score
        is_image_equal = self.image == __o.image

        return is_name_equal and is_score_equal and is_image_equal
