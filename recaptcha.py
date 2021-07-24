import os, requests

recaptcha_secret_key = os.environ.get('RECAPTCHA_SECRET_KEY', None)

def verify_recaptcha_v3(recaptcha_token):
  print('verify reCAPTCHA')
  if not recaptcha_secret_key:
    print('RECAPTCHA_SECRET_KEY is not found')
    return False
  url = f'https://www.google.com/recaptcha/api/siteverify?secret={recaptcha_secret_key}&response={recaptcha_token}'
  data = requests.post(url).json()
  success = data.get('success', False)
  print('reCAPTCHA score:', data.get('score'))
  return success
