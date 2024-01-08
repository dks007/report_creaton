"""
This module contains constants used throughout the project
"""
import os

# GOOGLE_URL used for interact with google server to verify user existence.
#GOOGLE_URL = "https://www.googleapis.com/plus/v1/"

# Define Code prefix word
# for guardian code,
# junior code,
# referral code"""
ZOD = 'ZOD'
JUN = 'JUN'
GRD = 'GRD'
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
SUPER_ADMIN = "Super Admin"

# Define jwt_token_expiration time in minutes for now token will expire after 3 days
JWT_TOKEN_EXPIRATION = 3 * 24 * 60

# Define common file extention
FILE_EXTENSION = ("gif", "jpeg", "jpg", "png", "svg")

# Define file size in bytes(5MB =  5 * 1024 * 1024)
FILE_SIZE = 5 * 1024 * 1024

# String constant for configurable date for allocation lock period
ALLOCATION_LOCK_DATE = 1
# guardian code status tuple
guardian_code_tuple = ('1','3')
"""user type"""
USER_TYPE = (
    ('1', 'junior'),
    ('2', 'guardian'),
    ('3', 'superuser')
)
DEVICE_TYPE = (
    ('1', 'android'),
    ('2', 'ios')
)
USER_TYPE_FLAG = {
    "FIRST" : "1",
    "TWO" : "2",
    "THREE": "3"
}

"""gender"""
GENDERS = (
    ('1', 'Male'),
    ('2', 'Female')
)
# Task status"""
TASK_STATUS = (
    ('1', 'pending'),
    ('2', 'in-progress'),
    ('3', 'rejected'),
    ('4', 'requested'),
    ('5', 'completed'),
    ('6', 'expired')
)
# sign up method
SIGNUP_METHODS = (
    ('1', 'manual'),
    ('2', 'google'),
    ('3', 'apple')
)
# guardian code status
GUARDIAN_CODE_STATUS = (
    ('1', 'no guardian code'),
    ('2', 'exist guardian code'),
    ('3', 'request for guardian code')
)
# article status
ARTICLE_STATUS = (
    ('1', 'read'),
    ('2', 'in_progress'),
    ('3', 'completed')
)
# relationship
RELATIONSHIP = (
    ('1', 'parent'),
    ('2', 'legal_guardian')
)
"""
Define task status
in a number"""
PENDING = 1
IN_PROGRESS = 2
REJECTED = 3
REQUESTED = 4
COMPLETED = 5
EXPIRED = 6
TASK_POINTS = 5
# duplicate name used defined in constant PROJECT_NAME
PROJECT_NAME = 'Zod Bank'
# define user type constant
GUARDIAN = 'guardian'
JUNIOR = 'junior'
SUPERUSER = 'superuser'
# numbers used as a constant

# Define the byte into kb
BYTE_IMAGE_SIZE = 1024

# validate file size
MAX_FILE_SIZE = 1024 * 1024 * 5

ARTICLE_SURVEY_POINTS = 5
MAX_ARTICLE_CARD = 6

# min and max survey
MIN_ARTICLE_SURVEY = 5
MAX_ARTICLE_SURVEY = 10

# already register
Already_register_user = "duplicate key value violates unique constraint"

ARTICLE_CARD_IMAGE_FOLDER = 'article-card-images'

DATE_FORMAT = '%Y-%m-%d'
