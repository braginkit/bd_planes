import os

class Config(object):
    DEBUG = True
    CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'UYVBDUAOhawbdaudUYABDbadb891ahjsdb'
    CSRF_SESSION_KEY = 'HFBAibfwibfiqhwbfihq90234sknqd'
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
