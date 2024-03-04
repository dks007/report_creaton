"""
This module contains all the messages used all across the project
"""

ERROR_CODE_REQUIRED = {
    # Error code for email address
    "1000": ["Required email address not found."],
    # Error code for password
    "1001": ["Required password not found."],
    # Error code for Required Post parameters
    "1002": ["Required POST parameters not found."],
    # Error code for Required Get parameters
    "1003": ["Required GET parameters not found."],
    # Error code for Required Headers
    "1004": ["Required headers were not found."],
    # Error code for Required Put parameters
    "1005": ["Required PUT parameters not found."],
    # Error code for Required query parameters
    "1006": ["Required query parameters is not valid."],
    # Error code for Required Head parameters
    "1008": ["Required HEAD parameters not found."]
}

# Error code
ERROR_CODE = {
    "2000": "Invalid email address. Please enter a registered email.",
    "2001": "This is your existing password. Please choose other one",
    "2002": "Invalid username or password.",
    "2003": "An account already exists with this email address.",
    "2004": "User not found."
}
"""Success message code"""
SUCCESS_CODE = {
    ""
    "3000": "Report saved successfully.",
    # Success code for password
    "3001": "Report created successfully.",
    "3002": "Report has already been created.",
    "30013": "Report is in progress and cannot be updated."
}
"""status code error"""
STATUS_CODE_ERROR = {
    # Status code for Invalid Input
    "4001": ["Invalid input."],
    # Status code for Authentication credentials
    "4002": ["Authentication credentials were not provided."],
    # Status code for Permission
    "4003": ["You do not have permission to perform this action."],
    # Status code for not found
    "4004": ["Not found."],
    # Status code for method not allowed
    "4005": ["Method not allowed."]
}


