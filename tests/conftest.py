import os, sys
import pytest
from xprocess import ProcessStarter

@pytest.fixture(autouse=True, scope="session")
def start_server(xprocess):
    os.environ["FLASK_APP"] = "/home/caleb/Flask_REST_API/Flask_REST"
    os.environ["FLASK_ENV"] = "test"

    class Starter(ProcessStarter):
        pattern = "Running"
        args = ["flask", "run"]

    timeout = 10
    
    xprocess.ensure("Flask_API", Starter)
    yield
    xprocess.getinfo("Flask_API").terminate()
