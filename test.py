import pandas as pd
# data = pd.read_csv('pageage_name_PH.csv')
# data1 = pd.read_csv('pageage_name_VN.csv')
# result = data1.values.tolist()
# urls = []
# for s in result:
#      urls.append('https://play.google.com/store/apps/details?id=' + s[0])

df1 = pd.read_csv('test.csv')
df2 = pd.read_csv('test1.csv')
# print(df1)
# print(df2)
result = pd.merge(df1, df2, on='Package', how='inner')
print(result)
# result.to_csv('test2.csv')