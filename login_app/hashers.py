import bcrypt
from django.contrib.auth.hashers import BasePasswordHasher

class BcryptPasswordHasher(BasePasswordHasher):
    algorithm = "bcrypt"

    def salt(self):
        return None

    def encode(self, password, salt):
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        return f"{self.algorithm}${hashed}"

    def verify(self, password, encoded):
        algorithm, hashed = encoded.split('$', 1)
        return bcrypt.checkpw(password.encode(), hashed.encode())

    def safe_summary(self, encoded):
        return {'algorithm': self.algorithm}