"""
This module contains constants used throughout the project
"""
import os

# GOOGLE_URL used for interact with google server to verify user existence.
#GOOGLE_URL = "https://www.googleapis.com/plus/v1/"

# Define number variable
# from zero to
# twenty and
# some standard
# number"""
NUMBER = {
    'point_zero': 0.0, 'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7,
    'eight': 8, 'nine': 9, 'ten': 10, 'eleven': 11, 'twelve': 12, 'thirteen': 13, 'fourteen': 14, 'fifteen': 15,
    'sixteen': 16, 'seventeen': 17, 'eighteen': 18, 'nineteen': 19, 'twenty': 20,
    'twenty_one': 21, 'twenty_two': 22,'twenty_three': 23, 'twenty_four': 24, 'twenty_five': 25,
    'thirty': 30, 'forty': 40, 'fifty': 50, 'sixty': 60, 'seventy': 70, 'eighty': 80, 'ninty': 90,
    'ninety_nine': 99, 'hundred': 100, 'thirty_six_hundred': 3600
}

none = "none"

# Super Admin string constant for 'role'
SUPER_ADMIN = "Admin"

# Define jwt_token_expiration time in minutes for now token will expire after 3 days
JWT_TOKEN_EXPIRATION = 3 * 24 * 60

# Define common file extention
FILE_EXTENSION = ("jpeg", "jpg", "png")

# Define file size in bytes(5MB =  5 * 1024 * 1024)
FILE_SIZE = 5 * 1024 * 1024

# String constant for configurable date for allocation lock period
ALLOCATION_LOCK_DATE = 1

# Task status"""
REPORT_STATUS = (
    ('0', 'Not Started'),
    ('1', 'In Progress'),
    ('2', 'Created'),
    ('3', 'Create Error'),
    ('4', 'Unknown')
)

# constant PROJECT_NAME
PROJECT_NAME = 'Success Tool'

# Define the byte into kb
BYTE_IMAGE_SIZE = 1024

# validate file size
MAX_FILE_SIZE = 1024 * 1024 * 5

DATE_FORMAT = '%Y-%m-%d'
