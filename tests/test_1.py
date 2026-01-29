import pytest
import requests

# Requesting the 'openml_docker_stack' fixture forces it to run!
def test_can_connect_to_local_docker(openml_docker_stack):
    
    # Try to talk to the V2 API we just built
    response = requests.get("http://localhost:9001/docs")
    
    # If we get a 200 OK or 404 (Not Found), the server is alive.
    # If it fails, this line will crash the test.
    assert response.status_code in [200]
