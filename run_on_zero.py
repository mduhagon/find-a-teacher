from teachersapp import create_app

app = create_app()
app.app_context().push()

if __name__ == '__main__':
    # When running the app inside a Docker container,
    # and trying to bind (from Windows) the container port to the
    # host port, it would not work.
    # It does work if the python app is run on 0.0.0.0 instead of the default
    app.run(host='0.0.0.0', debug=True)