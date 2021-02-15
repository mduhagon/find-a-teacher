import random, string
from teachersapp import db, bcrypt
from teachersapp.models import Language, User, UserTypes, TeachingProfile

def load_file_as_list(filename):
    result = []
    with open(filename, "r") as a_file:
        for line in a_file:
            result.append(line.strip())
    return result

def random_suffix():
    letters = string.digits
    return ''.join(random.choice(letters) for i in range(5))  

db.drop_all()

# This attempts to fix this error:
# AddGeometryColumn() error: unexpected metadata layout
# DiscardGeometryColumn: "no such table: geometry_columns"
db.engine.execute("SELECT InitSpatialMetaData();")

db.create_all()



# Insert the list of languages that can be offered in the site
langs = []
with open("teachersapp/resources/initial-language-list.txt", "r") as a_file:
  for line in a_file:
    stripped_line = line.strip()
    lang = Language(name=stripped_line)
    langs.append(lang)
    db.session.add(lang) 
print("Added Languages", len(langs))

# Insert my own user as Admin
hashed_password = bcrypt.generate_password_hash('password').decode('utf-8')
admin = User(name='Maria', email='mduhagon@gmail.com', password=hashed_password, user_type=UserTypes.Admin)
db.session.add(admin)
print(f"Added admin user: email=mduhagon@gmail.com pass=password")

# Insert some fake teachers 
dummy_service_titles = load_file_as_list("teachersapp/resources/dummy-service-titles.txt")
dummy_service_descriptions = load_file_as_list("teachersapp/resources/dummy-service-descriptions.txt")

count_users = 0
usernames = []
emails = []
with open("teachersapp/resources/dummy-users.txt", "r") as a_file:
  for line in a_file:
    givenName,streetAddress,city,email,username,latitude,longitude = line.strip().split(",")
    teacher_num_langs = random.choice([1,2])
    teacher_langs = random.sample(langs, teacher_num_langs)
    serviceTitle = random.choice(dummy_service_titles).replace('#name', givenName).replace('#lang', teacher_langs[0].name)
    serviceDescription = random.choice(dummy_service_descriptions).replace('#name', givenName).replace('#lang', teacher_langs[0].name)

    # the dummy file contains duplicate usernames and emails, so I need to catch them 
    # and make them different
    if username in usernames:
        username += random_suffix()
    if email in emails:
        email = random_suffix() + email    

    usernames.append(username)
    emails.append(email)
    user = User(name=username, email=email, password='')
    teachingProfile = TeachingProfile(
        title=serviceTitle, 
        service_description=serviceDescription, 
        service_address=streetAddress,
        service_location='POINT(' + str(longitude) + ' ' + str(latitude) + ')',
        user=user)

    for l in teacher_langs:    
        teachingProfile.offered_languages.append(l)    

    db.session.add(user)
    db.session.add(teachingProfile)
    count_users += 1

print(f"Added fake users: {count_users}")
        
db.session.commit()
