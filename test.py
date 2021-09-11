import pandas as pd
data = pd.read_excel('appInfo.xlsx')
result = data.values.tolist()
res = []
for s in result:
    res.append('https://play.google.com/store/apps/details?id=' + s[2])
print(res)