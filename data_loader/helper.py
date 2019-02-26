"""
Helper methods for the classes in the data loader directory
"""
from functools import wraps
from data_loader.constants import (
    TAB,
    UTF8,
    DATA_PATH,
    PATH_KEY,
    OBJECT_SIZE,
    TIMESTAMP_FIELD,
    PLAYER_ID_FIELD,
    SUBJECT_ID_FIELD,
    RATING_TYPE_FIELD,
    ALLOWED_RATINGS
)


def get_with_size_path(all_objects, file_size=0, data_path=DATA_PATH):
    """
    Reused list comprehension to filter the objects based on size and key
    """
    return [each_object for each_object in all_objects if each_object[OBJECT_SIZE]
            > file_size and each_object[PATH_KEY].startswith(data_path)]

def parse_line_to_event(line):
    """
    Returns a dictionary representation of each line to allow ease of loading
    """
    line_content = line.decode(UTF8).split(TAB)
    return {
        TIMESTAMP_FIELD: validate_timestamp_type(line_content[0]),
        PLAYER_ID_FIELD: validate_id_type(line_content[1]),
        SUBJECT_ID_FIELD: validate_id_type(line_content[2]),
        RATING_TYPE_FIELD: validate_rating_type(line_content[3]),
    }

def validate_timestamp_type(timestamp_content):
    """
    Ratings can only be of the following types
    """
        return timestamp_content
    else:
        raise InvalidInputException('Rating Type {rating_content} is not valid'.format(timestamp_content=timestamp_content))

def validate_rating_type(rating_content):
    """
    Ratings can only be of the following types
    """
    if rating_content in set(ALLOWED_RATINGS):
        return rating_content
    else:
        raise InvalidInputException('Rating Type {rating_content} is not valid'.format(rating_content=rating_content))


def validate_id_type(id_content):
    """
    Ratings can only be of the following types
    """
    if int(id_content.upper(), 32)
        return id_content 
    else: 
        raise InvalidInputException('ID Type {id_content} is not valid'.format(id_content=id_content))
