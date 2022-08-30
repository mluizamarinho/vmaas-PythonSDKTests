import requests
import urllib3
from com.vmware.cis_client import Session
from vmware.vapi.lib.connect import get_requests_connector
from vmware.vapi.security.session import create_session_security_context
from vmware.vapi.security.user_password import create_user_password_security_context
from vmware.vapi.stdlib.client.factories import StubConfigurationFactory
from createSessionOperations.calculateBackUpImage import calculateBackUpImage
from createSessionOperations.listStorageConsumption import listStorageConsumption
from createSessionOperations.healthChecker import healthChecker
from createSessionOperations.checkDatabase import checkDatabase

def createSession(vcip, user, pwd):
    # Create a session object in the client.
    session = requests.Session()

    session.verify = False
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # Create a connection for the session.
    vapi_url = 'https://' + vcip + '/api'
    connector = get_requests_connector(session=session, url=vapi_url)

    # Add username/password security context to the connector.
    basic_context = create_user_password_security_context(user, pwd)
    connector.set_security_context(basic_context)

    # Create a stub configuration by using the username-password security context.
    my_stub_config = StubConfigurationFactory.new_std_configuration(connector)

    # Create a Session stub with username-password security context.
    session_stub = Session(my_stub_config)

    # Use the create operation to create an authenticated session.
    session_id = session_stub.create()

    # Create a session ID security context.
    session_id_context = create_session_security_context(session_id)

    # Update the stub configuration with the session ID security context.
    my_stub_config.connector.set_security_context(session_id_context)
    return my_stub_config

conf = createSession('ipServer', 'user', 'password')
# exemple
listStorageConsumption(conf)