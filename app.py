from teachersapp import create_app

app = create_app()
app.app_context().push()