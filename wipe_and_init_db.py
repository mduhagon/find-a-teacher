from teachersapp import db, bcrypt
from teachersapp.models import Language, User, UserTypes

db.drop_all()
db.create_all()

# Insert the list of languages that can be offered in the site
count_langs = 0
with open("teachersapp/resources/initial-language-list.txt", "r") as a_file:
  for line in a_file:
    stripped_line = line.strip()
    lang = Language(name=stripped_line)
    db.session.add(lang) 
    count_langs += 1
print(f"Added {count_langs} Languages")

# Insert my own user as Admin
hashed_password = bcrypt.generate_password_hash('password').decode('utf-8')
admin = User(name='Maria', email='mduhagon@gmail.com', password=hashed_password, user_type=UserTypes.Admin)
db.session.add(admin)
print(f"Added admin user: email=mduhagon@gmail.com pass=password")

# Insert some fake teachers 
# TODO

db.session.commit()