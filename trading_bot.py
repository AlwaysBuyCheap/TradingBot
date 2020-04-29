import time
import requests
import json

API_ID = "YOUR_ALPACA_ID"
API_SECRET_KEY = "YOUR_SECRET_API_KEY"



BASE_URL = "https://paper-api.alpaca.markets"
ORDERS_URL = "{}/v2/orders".format(BASE_URL)
headers={'APCA-API-KEY-ID':API_ID,'APCA-API-SECRET-KEY':API_SECRET_KEY}

def get_order(symbol,qty,side,typ,time_in_force):
	data = {
	"symbol":symbol,
	"qty":qty,
	"side":side,
	"type":typ,
	"time_in_force":time_in_force
	}

	r = requests.post(ORDERS_URL, json = data, headers = {'APCA-API-KEY-ID':API_ID,'APCA-API-SECRET-KEY':API_SECRET_KEY})

	return json.loads(r.content)

turnaround = False
compra = False
#get_order("FB",400,"buy","market","gtc")

total = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=FB&interval=1min&apikey=TZXBXLAS01S8CW10").json()
date = total['Meta Data']['3. Last Refreshed']
total = float(total['Time Series (1min)'][date]['4. close'])
beneficio = 0
print(f"Actual Price: {total}")

while True:
	sec = time.localtime()[5]
	minute = time.localtime()[4]
	hour = time.localtime()[3]
	timenow = str(time.localtime()[3]) + "-" + str(time.localtime()[4]) + "-" + str(time.localtime()[5])
	if sec == 10:
		SMA = requests.get("https://www.alphavantage.co/query?function=SMA&symbol=FB&interval=1min&time_period=7&series_type=open&apikey=TZXBXLAS01S8CW10").json()
		date = SMA['Meta Data']['3: Last Refreshed']
		SMA7 = SMA['Technical Analysis: SMA'][date[:-3]]['SMA']
		SMA29 = requests.get("https://www.alphavantage.co/query?function=SMA&symbol=FB&interval=1min&time_period=29&series_type=open&apikey=TZXBXLAS01S8CW10").json()
		SMA29 = SMA29['Technical Analysis: SMA'][date[:-3]]['SMA']
		PRICE = float(requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=FB&interval=1min&apikey=TZXBXLAS01S8CW10").json()['Time Series (1min)'][date]['4. close'])

		percent = (PRICE - total)/total

		if compra == True:
			if percent > 0.01:
				compra = False
				turnaround = False
				beneficio = beneficio + PRICE - total
				get_order("FB",400,"sell","market","gtc")
				print("sell")
			
			else:
				if SMA7>SMA29:
					pass
					print("nothing happens SMA7>SMA29")
				else:
				
					compra = False
					beneficio = beneficio + PRICE - total
					get_order("FB",400,"sell","market","gtc")
					print("sell")
					
		else:
			if SMA7>SMA29:
				
				if turnaround == True:			
					compra = True
					total = PRICE
					print("buy")
					get_order("FB",400,"buy","market","gtc")
				else:
					pass
					print("nothing happens SMA7>SMA29 and turn == False")
			else:
				turnaround = True
				print("nothing happens SMA7<SMA29")
		

		print(f"Actual price: {PRICE}	SMA7: {SMA7}	SMA29: {SMA29}		{timenow}")
		print(f"Buy price: {total}     Benefit: {beneficio}")	

	elif hour == 21 and minute == 29 and sec == 10:
		if compra == True:
			compra = False
			beneficio = beneficio + PRICE - total
			get_order("FB",400,"sell","market","gtc")
			print("sell")
			print(f"Actual price: {PRICE}	SMA7: {SMA7}	SMA29: {SMA29}		{timenow}")
			print(f"Buy price: {total}     Benefit: {beneficio}")
			break;
	else:	
		pass
