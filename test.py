import requests
import pandas as pd

data = {
  'f.req': '[[["xdSrCf","[[null,[\\"com.sc.scorecreator\\",7],[]]]",null,"1"]]]',
}
url = 'https://play.google.com/_/PlayStoreUi/data/batchexecute?rpcids=xdSrCf&f.sid=-3751894382704443719&bl=boq_playuiserver_20210908.03_p0&hl=en-US&authuser&soc-app=121&soc-platform=1&soc-device=1&_reqid=164510&rt=c'
response = requests.post(url, headers={"content-type": "application/x-www-form-urlencoded"},data=data)

allowed_domains = []
url = []
data = pd.read_excel('appInfo.xlsx')
result = data.values.tolist()
for s in result:
    url.append('[[["xdSrCf","[[null,[\""' + s[2] + '\",7],[]]]",null,"1"]]]')
    # [[["xdSrCf","[[null,[\"com.google.android.youtube\",7],[]]]",null,"1"]]]
# print(url)

print('[[["xdSrCf","[[null,[\\"com.google.android.youtube\\",7],[]]]",null,"1"]]]')