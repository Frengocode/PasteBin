from passlib.context import CryptContext



class Hash:

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @staticmethod
    def bcrypt(password: str) -> str:
        return Hash.pwd_context.hash(password)
    
    @staticmethod
    def verify(hashed_password, plain_password):
        return Hash.pwd_context.verify(plain_password, hashed_password)
    