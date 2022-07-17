from . import FakeModel


class FakeStoreModel(FakeModel):
    name = ''

    objects = None

    def __init__(self, name):
        self.name = name
        self._saved = False

    def save(self):
        self._saved = True

    def __str__(self):
        return (
            '{\n' +
            f'\tname: {self.name},\n' +
            '}'
        )
