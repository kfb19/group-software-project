import requests
from decouple import config
import json

params = {
  'workflow': 'wfl_brNwJk9abjFRDu54kAc6y',
  'api_user': config('image_analysis_api_user'),
  'api_secret': config('image_analysis_api_key')
}

files = {'media': open('', 'rb')}
r = requests.post('https://api.sightengine.com/1.0/check-workflow.json', files=files, data=params)

output = json.loads(r.text)

if output['status'] == 'failure':
  # handle failure
  print(output['error'])

print(output['summary']['action'])
print(output['summary']['reject_prob'])
print(output['summary']['reject_reason'])


if output['summary']['action'] == 'reject':
  # handle image rejection
  # the rejection probability is provided in output['summary']['reject_prob']
  # and user readable reasons for the rejection are in the array output['summary']['reject_reason']
  pass