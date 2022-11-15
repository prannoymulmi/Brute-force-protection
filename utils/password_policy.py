from password_strength import PasswordPolicy
"""
A configuration for the password policy strength. 
The strict password is chosen because these are staff accounts and breach may cause lose of Health Personally Identifiable Information (PII). 
"""
policy = PasswordPolicy.from_names(
    length=16,  # min length: 16
    uppercase=2,  # need min. 2 uppercase letters
    numbers=2,  # need min. 2 digits
    special=2,  # need min. 2 special characters
    nonletters=2,  # need min. 2 non-letter characters (digits, specials, anything)
)
