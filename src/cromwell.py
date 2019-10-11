from bravado.client import SwaggerClient

from bravado.requests_client import RequestsClient
from bravado.client import SwaggerClient

http_client = RequestsClient()
http_client.set_basic_auth(
    '34.74.157.142',
    'user1', '123'
)

client = SwaggerClient.from_url(
    'http://34.74.157.142/swagger/cromwell.yaml',
    http_client=http_client,
)
