import jwt
from datetime import datetime, timedelta

# This is a secret key used for encoding and decoding JWT tokens.
# It should be kept secret and not hard-coded in production.
SECRET_KEY = 'vassdel'

def generate_token(user):
    # Define the token expiration time (e.g., 60 minutes from now)
    expiration_time = datetime.utcnow() + timedelta(minutes=60)

    # Create the token payload
    payload = {
        'user_id': user.id,  # Include user ID in the payload
        'exp': expiration_time,  # Expiration time
        'iat': datetime.utcnow(),  # Issued at time
        # You can include more information about the user here if needed
    }

    # Encode the payload to create the JWT token
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

    return token
