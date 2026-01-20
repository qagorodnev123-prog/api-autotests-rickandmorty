from enum import Enum

class Genders(str, Enum):
    FEMALE = 'female'
    MALE = 'male'
    GENDERLESS = 'genderless'
    UNKNOWN = 'unknown'

class Status(str, Enum):
    ALIVE = 'alive'
    DEAD = 'dead'
    UNKNOWN = 'unknown'