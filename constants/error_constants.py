from enum import Enum

class Errors(str, Enum):
    EPISODE_ERROR_MSG = 'Episode not found'
    CHARACTER_ERROR_MSG = 'Character not found'
    LOCATION_ERROR_MSG = 'Location not found'
    WRONG_PARAMS_MSG = 'There is nothing here'

