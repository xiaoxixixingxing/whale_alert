import time
import json
import requests

while(True):
    time_start = str(int(time.time()-600))
    url = 'https://api.whale-alert.io/v1/transactions?api_key=7phBF3Cy2biiiQdMqArlvh7m3FQHM9Hi&start={}&min_value=500000&'.format(time_start)
    url_state='https://api.whale-alert.io/v1/status?api_key=your-api-key-here'

    response = json.loads(requests.get(url=url).text)
    #print(response)
    for transaction in response['transactions']:
        out_line = ' '.join([time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(transaction['timestamp'])),str(transaction['amount']),transaction['symbol'],'('+str(transaction["amount_usd"])+' USD'+')',transaction['transaction_type'],'from',transaction['from']['owner'],'to',transaction['to']['owner']])
        print(out_line)
    time.sleep(15)
