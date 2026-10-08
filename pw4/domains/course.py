from domains.entity import Entity

class Course(Entity):
    def __init__(self, c_id="", name="", credits=0):
        self.__id = c_id
        self.__name = name
        self.__credits = credits

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_credits(self):
        return self.__credits