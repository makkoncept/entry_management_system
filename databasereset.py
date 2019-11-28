from entrymanagement import db, bcrypt
from entrymanagement.models import Host

password_hash = bcrypt.generate_password_hash("zb7h7A1ph").decode("utf-8")

db.reflect()
db.drop_all()

u = Host(
    username="mayank nader",
    email="mayank.nader11@gmail.com",
    phone_no="7906999890",
    address="dehradun, delhi",
    password_hash=password_hash,
)

db.create_all()
db.session.add(u)
db.session.commit()
