from teachersapp import db
from teachersapp.models import Language

with open("teachersapp/resources/initial-language-list.txt", "r") as a_file:
  for line in a_file:
    stripped_line = line.strip()
    lang = Language(name=stripped_line)
    db.session.add(lang) 
    print('Adding: '+ stripped_line)

db.session.commit()

Language.query.all()