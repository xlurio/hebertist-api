class FakeModel:

    name = ''
    score = 0
    image = ''

    objects = None

    def __init__(self, name, score, image):
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
