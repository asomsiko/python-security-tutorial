import hmac
import pickle
import secrets

# assume both parties agreed on some random secret key for the session
secret_random_key = secrets.token_bytes(32)

# send a pickled data along with its digest
data = b'cos\nsystem\n(S"echo hello world"\ntR.'
digest = hmac.new(secret_random_key, data, 'sha256').digest()
payload = digest + data

# verify the digest before using the data
rcv_digest = payload[:32]
rcv_data = payload[32:]
expected_digest = hmac.new(secret_random_key, rcv_data, 'sha256').digest()
if not secrets.compare_digest(rcv_digest, expected_digest):
   print('Integrity check failed')
   exit(1)
objects = pickle.loads(rcv_data)
