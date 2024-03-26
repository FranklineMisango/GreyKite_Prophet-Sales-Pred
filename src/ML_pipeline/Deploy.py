# Importing required packages
from flask import Flask
from flask_restful import Resource, Api
from . import Utils


class LoanPred(Resource):
    def __init__(self, model):
        self.model = model

    def get(self):
        return{'ans': 'success'}

# Function to deploy the model on falsk
def init(load_path):
    app = Flask(__name__)
    api = Api(app)

    uploaded_model = Utils.load_model(load_path)

    api.add_resource(LoanPred, '/', resource_class_kwargs={'model': uploaded_model})
    app.run(port=12345)
