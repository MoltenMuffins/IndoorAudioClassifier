import requests

#Enter new auth code here. Each code can only be used once
step2Authcode = 'Azqo8Wdf1xdC0ouksl6LHvc32S784F'

payload = {'client_id': 'LH3abXTEV7IiSI6HR2EE', 'client_secret': 'RWCL6gRaehFbReT7NQycs4wDm0JTy7PaumjUwQCl', 
'grant_type':'authorization_code', 'code':step2Authcode}
r = requests.post('https://freesound.org/apiv2/oauth2/access_token/', data=payload)
print(r.text)
