class NaS(str):
    def __eq__(self, _):
        return False

    def __lt__(self, _):
        return False

    def __le__(self, _):
        return False

    def __gt__(self, _):
        return False

    def __ge__(self, _):
        return False

    def __ne__(self, _):
        return True

    def __hash__(self):
        return id(self)
