#define configuration parameters for Authorizer Layer
class Config:
    def __init__():
        self.config = {
            "server": "localhost",
            "db": "auth",
            "user": "postgres",
            "password": "admin",
            "default_alg": "HS256",
            "password_secret": "SOME BYTE ARRAY",
            "token_lifetime": 8640000000
        }