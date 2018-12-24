from google.oauth2 import service_account
from google.cloud import storage
import arrow
import psycopg2


conn = psycopg2.connect(dbname="postgres", user="postgres", password="transit", host="35.230.49.21")
conn.autocommit = True
cur = conn.cursor()
credentials = service_account.Credentials.from_service_account_file(
    'ac-transit-224721-f32b66bc7da6.json')

a = arrow.utcnow()

client = storage.Client(credentials=credentials)

bucket_name = str(a.year) + str(a.month) + str(a.day)

bucket = client.create_bucket(bucket_name)
print('Bucket {} created.'.format(bucket.name))

