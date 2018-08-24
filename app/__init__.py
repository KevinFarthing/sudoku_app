from flask import Flask, Request
# from config import Config
from flask_bootstrap import Bootstrap
app = Flask(__name__)
bootstrap = Bootstrap(app)

from app import routesgit