from copy import copy


class ListPaginatorByOne:
    def __init__(self, list_: list):
        self.pages = len(list_)
        self.object = copy(list_)
        self.current = -1

    def next(self):
        self.current += 1
        try:
            return self.object[self.current]
        except IndexError as ex:
            self.current = 0
            return self.object[self.current]

    def prev(self):
        self.current -= 1
        try:
            return self.object[self.current]
        except IndexError as ex:
            self.current = 0
            return self.object[self.current]

    def position(self):
        return f'{self.current + 1}/{self.pages}'

    def value(self):
        return self.object[self.current]
