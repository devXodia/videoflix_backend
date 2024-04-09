import hashlib
import random
import string
from django.conf import settings

def generate_verification_token(user):
    # Combine user's email and a secret key to create a unique token
    token_data = user.email + settings.SECRET_KEY + str(random.random())
    
    # Hash the token data using a secure hashing algorithm (e.g., SHA-256)
    token_hash = hashlib.sha256(token_data.encode()).hexdigest()
    
    # Encode the user's primary key (pk) and append it to the token
    token = f"{user.pk}:{token_hash}"
    
    return token