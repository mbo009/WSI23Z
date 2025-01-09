class NotEnoughColumns(Exception):
    def __init__(self):
        super().__init__("Not enough columns passed as an argument")
