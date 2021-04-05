from flask import Flask

app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY='dev',
)
app.jinja_env.auto_reload = True


import fortune.main
