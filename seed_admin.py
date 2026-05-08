import models, auth, database
from sqlalchemy.orm import Session

def create_admin():
    db = database.SessionLocal()
    admin_email = "admin@cardioai.com"
    db_user = db.query(models.User).filter(models.User.email == admin_email).first()
    
    if not db_user:
        hashed_password = auth.get_password_hash("admin123")
        admin = models.User(
            full_name="Administrator",
            email=admin_email,
            hashed_password=hashed_password,
            role="admin"
        )
        db.add(admin)
        db.commit()
        print(f"Admin user created: {admin_email} / admin123")
    else:
        print("Admin user already exists.")
    db.close()

if __name__ == "__main__":
    create_admin()
