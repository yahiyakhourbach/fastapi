from passlib.context import CryptContext


hash_context = CryptContext(schemes='bcrypt', deprecated="auto")


def hash_password(password):
    return hash_context.hash(password)

def validate_password(password, hashed_password):
     return hash_context.verify(password, hashed_password)