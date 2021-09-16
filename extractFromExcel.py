import pandas as pd
import requests
import threading

package = []
data = pd.read_csv('pageage_name_PH.csv')
result = data.values.tolist()

def process():
    for s in result:
        url = 'https://play.google.com/store/apps/details?id=' + s[0]
        response = requests.get(url)
        print(response.status_code)
    # package.append('https://play.google.com/store/apps/details?id=' + s[0])
def main():
    thread = []
    for i in range(100):
        t = threading.Thread(target=process())
        t.start()
        thread.append(t)
    for t in thread:
        t.join()

if __name__ == '__main__':
    main()