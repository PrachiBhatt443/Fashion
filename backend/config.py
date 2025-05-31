class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'  # SQLite DB for local dev
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'Fashionista@mazing'  # Change this to a strong secret key
