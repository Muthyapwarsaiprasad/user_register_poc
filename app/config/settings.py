import os
from dotenv import load_dotenv
load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET", "supersecretkey")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_DAYS = int(os.getenv("JWT_EXPIRATION_DAYS", 30))


MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://saiprasad:IeRjrY04NFZwXR4I@newarticles.waa3uh5.mongodb.net/")
