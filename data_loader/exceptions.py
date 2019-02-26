"""
Classes for the Exceptions used in the repo
"""

class DataLoaderBaseException(Exception):
    """
    Base class for other exceptions
    """

class InvalidInputException(DataLoaderBaseException):
    """
    Exception for when the input read in does not match the assumptions for the input
    """
