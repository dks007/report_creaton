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
    "2004": "User not found.",
    "2005": "Your account has been activated.",
    "2006": "Your account is not activated.",
    "2007": "Your account already activated.",
    "2008": "The OTP entered is not correct.",
    "2009": "The user provided cannot be found or the reset password token has become invalid/timed out.",
    "2010": "Invalid Link.",
    "2011": "Your profile has not been completed yet.",
    "2012": "Phone number already used",
    "2013": "Invalid token.",
    "2014": "Your old password doesn't match.",
    "2015": "Invalid old password.",
    "2016": "Invalid search.",
    "2017": "{model} object with {pk} does not exist",
    "2018": "Attached File not found",
    "2019": "Invalid Referral code",
    "2020": "Enter valid mobile number",
    "2021": "Already register",
    "2022": "Invalid Guardian code",
    "2023": "Invalid user",
    # email not verified
    "2024": "Email not verified",
    "2025": "Invalid input. Expected a list of strings.",
    # check old and new password
    "2026": "New password should not same as old password",
    "2027": "data should contain `identityToken`",
    "2028": "You are not authorized person to sign up on this platform",
    "2029": "Validity of otp verification has expired. Please request a new one.",
    "2030": "Use correct user type and token",
    # invalid password
    "2031": "Invalid password",
    "2032": "Failed to send email",
    "2033": "Missing required fields",
    "2034": "Junior is not associated",
    # image size
    "2035": "Image should not be 0 kb",
    "2036": "Choose valid user",
    # log in multiple device msg
    "2037": "You are already log in another device",
    "2038": "Choose valid action for task",
    # card length limit
    "2039": "Add at least one article card or maximum 6",
    "2040": "Add at least 5 article survey or maximum 10",
    # add article msg
    "2041": "Article with given id doesn't exist.",
    "2042": "Article Card with given id doesn't exist.",
    "2043": "Article Survey with given id doesn't exist.",
    "2044": "Task does not exist",
    "2045": "Invalid guardian",
    # past due date
    "2046": "Due date must be future date",
    # invalid junior id msg
    "2047": "Invalid Junior ID ",
    "2048": "Choose right file for image",
    # task request
    "2049": "This task is already requested ",
    "2059": "Already exist junior",
    # task status
    "2060": "Task does not exist or not in pending state",
    "2061": "Please insert image or check the image is valid or not.",
    # email not null
    "2062": "Please enter email address",
    "2063": "Unauthorized access.",
    "2064": "To change your password first request an OTP and get it verify then change your password.",
    "2065": "Passwords do not match. Please try again.",
    "2066": "Task does not exist or not in expired state",
    "2067": "Action not allowed. User type missing.",
    "2068": "No guardian associated with this junior",
    "2069": "Invalid user type",
    "2070": "You do not find as a guardian",
    "2071": "You do not find as a junior",
    "2072": "You can not approve or reject this task because junior does not exist in the system",
    "2073": "You can not approve or reject this junior because junior does not exist in the system",
    "2074": "You can not complete this task because you does not exist in the system",
    # deactivate account
    "2075": "Your account is deactivated. Please contact with admin",
    "2076": "This junior already associate with you",
    "2077": "You can not add guardian",
    "2078": "This junior is not associate with you",
    # force update
    "2079": "Please update your app version for enjoying uninterrupted services",
    "2080": "Can not add App version",
    "2081": "A junior can only be associated with a maximum of 3 guardian",
    # guardian code not exist
    "2082": "Guardian code does not exist"

}
"""Success message code"""
SUCCESS_CODE = {
    "3000": "ok",
    # Success code for password
    "3001": "Sign up successfully",
    # Success code for Thank you
    "3002": "Thank you for contacting us! Our Consumer Experience Team will reach out to you shortly.",
    # Success code for account activation
    "3003": "Log in successful",
    # Success code for password reset
    "3004": "Password reset link has been sent to your email address",
    # Success code for link verified
    "3005": "Your account is deleted successfully.",
    # Success code for password reset
    "3006": "Password reset successful. You can now log in with your new password.",
    # Success code for password update
    "3007": "Your password has been changed successfully.",
    # Success code for valid link
    "3008": "You have a valid link.",
    # Success code for logged out
    "3009": "You have successfully logged out!",
    # Success code for check all fields
    "3010": "All fields are valid",
    "3011": "Email OTP Verified successfully",
    "3012": "Phone OTP Verified successfully",
    "3013": "Valid Guardian code",
    "3014": "Password has been updated successfully.",
    "3015": "Verification code has been sent on your email.",
    "3016": "An OTP has been sent on your email.",
    "3017": "Profile image update successfully",
    "3018": "Task created successfully",
    "3019": "Support Email sent successfully",
    "3020": "Logged out successfully.",
    "3021": "Add junior successfully",
    "3022": "Remove junior successfully",
    "3023": "Junior is approved successfully",
    "3024": "Junior request is rejected successfully",
    "3025": "Task is approved successfully",
    "3026": "Task is rejected successfully",
    "3027": "Article has been created successfully.",
    "3028": "Article has been updated successfully.",
    "3029": "Article has been deleted successfully.",
    "3030": "Article Card has been removed successfully.",
    "3031": "Article Survey has been removed successfully.",
    "3032": "Task request sent successfully",
    "3033": "Valid Referral code",
    "3034": "Invite guardian successfully",
    "3035": "Task started successfully",
    "3036": "Task reassign successfully",
    "3037": "Profile has been updated successfully.",
    "3038": "Status has been changed successfully.",
    # notification read
    "3039": "Notification read successfully",
    # start article
    "3040": "Start article successfully",
    # complete article
    "3041": "Article completed successfully",
    # submit assessment successfully
    "3042": "Assessment completed successfully",
    # read article
    "3043": "Read article card successfully",
    # remove guardian code request
    "3044": "Remove guardian code request successfully",
    # create faq
    "3045": "Create FAQ data",
    "3046": "Add App version successfully"

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


