import requests

files = {'file': open('timeseries.csv','rb')}
upload_url = 'http://localhost:5001/api/v1/upload'
r = requests.post(upload_url, files=files)
print("Uploading time series file status: {}".format(r.status_code))

predict_url = 'http://localhost:5001/api/v1/predict'
payload = {'filename': 'timeseries.csv', 'days': 3}
r = requests.get(predict_url, params=payload)
print("Makeing prediction status: {}".format(r.status_code))