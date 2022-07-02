from . import Iterator


class SimpleIterator(Iterator):

    _index = 0

    def __init__(self, list):
        self._list = list

    def first(self):
        self._index = 0

    def last(self):
        list_length = len(self._list)
        last_index = list_length - 1
        self._index = last_index

    def next(self):
        self._index += 1

    def is_done(self):
        list_length = len(self._list)
        return self._index >= list_length

    def get_index(self):
        return self._index
