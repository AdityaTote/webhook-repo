import hashlib
import hmac

from app.core.config import config
from app.error.webhook import InvalidSignatureError


def validate_webhook(payload_body, hash_sign: str):
  hash_object = hmac.new(config.github_secret.encode('utf-8'), msg=payload_body, digestmod=hashlib.sha256)
  expected_signature = "sha256=" + hash_object.hexdigest()

  if not hmac.compare_digest(expected_signature, hash_sign):
    print("not done!")
    raise InvalidSignatureError(message="invalid signature", status_code=401)
  
  print("done!")
