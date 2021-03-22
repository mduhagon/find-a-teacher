# find-a-teacher
Project for Frauenloop class: website for language teachers to offer classes, and for students to find a teacher.

# Starting the app locally

1. Activate virtual env:

```
. venv/bin/activate
```

2. Set env variables that the app requires:

```
export FINDATEACHER_SECRET_KEY=SOME_VALUE
export FINDATEACHER_SQLALCHEMY_DATABASE_URI=SOME_VALUE
exportFINDATEACHER_GOOGLE_MAPS_API_KEY=SOME_VALUE
```

3. Initialize the Database:

```
export FLASK_APP=teachersapp
flask db upgrade
```

4. Run the Flask app:

```
python run.py
```
.
