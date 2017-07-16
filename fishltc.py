import gzip
import StringIO
import json
from ws4py.client.threadedclient import WebSocketClient
import logging
import time

def decodeDepthData(data):
	if not data:
		return
	if type(data) != type({}):
		return
	if not data.has_key('tick'):
		return
	tick = data.get('tick')
	if not tick.has_key('bids'):
		return
	bids = tick.get('bids')
	if not tick.has_key('asks'):
		return
	asks = tick.get('asks')
	return bids[0], asks[0]


def fishing(buyPrice, sellPrice):
	fp = open('plan.json', 'r')
	data = fp.read()
	fp.close()
	data = json.loads(data)
	buy  = data.get('buy')
	sell = data.get('sell')
	fp = open('account.json', 'r')
	acc = fp.read()
	acc = json.loads(acc)
	sumLtc = float(acc.get('ltc'))
	for i in buy:
		if float(sellPrice[0]) <= float(i[0]) and float(i[1]) > float(i[3]):
			buyNum = int(i[1]) - int(i[3])
			sumLtc = sumLtc + int(i[3])
			i[3] = i[1]
			i[2] = sellPrice[0]
			buyLtc(sellPrice[0], buyNum)
	for i in range(0, 10):
		xSell = (float(buy[i][2]) + float(sell[i][0]))* (1 + 0.004)
		if float(buy[i][2]) > 0 and float(buyPrice[0]) >= xSell  and sumLtc >0 and float(buy[i][3]) > 0:
			sellNum = int(sell[i][1])
			sell[i][3] = float(sell[i][3]) + float(sellNum)
			sell[i][2] = buyPrice[0]
			buy[i][3] = float(buy[i][3]) - float(sellNum)
			sellLtc(buyPrice[0], sellNum, buy[i][2])
	fp = open('plan.json', 'w+')
	data = json.dumps(data)
	fp.write(data)
	fp.close()
	
def buyLtc(price, num):
	accounting('buy', price, num, 0)

def sellLtc(price, num, bprice):
	accounting('sell', price, num, bprice)

def accounting(direction, price, num, bprice):
	fp = open('account.json', 'r+')
	data = fp.read()
	fp.close()
	data = json.loads(data)
	cost = price * num
	if direction == "buy":
		if cost > data.get('cny'):
			logging.debug('NOT ENOUGH CNY')
		else:
			data['cny'] = data['cny'] - (cost * 1.002)
			data['ltc'] = data['ltc'] + num
			logging.info(str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))) + ' BUY ' + str(num) + ' LTC, price ' + str(price) + "<p />")
	else:
		if num > data.get('ltc'):
			logging.debug('NOT ENOUGH LTC')
		else:
			data['ltc'] = data['ltc'] - num
			data['cny'] = data['cny'] + (cost * 0.998)
			wcny = float(num) * (float(price) * 0.998 - float(bprice) * 1.002)
			logging.info(str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))) + ' Sell ' + str(num) + ' LTC, price ' + str(price) + " gain cny:" + str(wcny) + "<p />")
	fp = open('account.json', 'w+')
	fp.write(json.dumps(data))		
	fp.close()
	
	trend = {'date' : time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())), 'cny' : data['cny']}
	fp = open('trend.log', 'a+')
	fp.write(json.dumps(trend) + '\r\n')
	fp.close()

class DummyClient(WebSocketClient):
	def opened(self):
		self.subscribe()
	def closed(self, code, reason=None):
		logging.warning(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + 'Closed Down <p />')
		if reason:
			logging.warning(reason)
	def received_message(self, m):
		compressedData = m
		compressedStream = StringIO.StringIO(compressedData)
		gzipper = gzip.GzipFile(fileobj = compressedStream)
		data = gzipper.read()
		decode_json = json.loads(data)
#		logging.info('Receive : ' + data)
		if decode_json.has_key('ping'):
			ping = decode_json.get('ping')
			pong = {'pong' : ping}
			pong_str = json.dumps(pong)
			self.send(pong_str)
		else:
			bidAndask = decodeDepthData(decode_json)
			if bidAndask and bidAndask[0] and bidAndask[1]:
				fishing(bidAndask[0], bidAndask[1])

	def subscribe(self):
		sub_data = {'sub' : 'market.ltccny.depth.step0', 'id' : 'id1'}
		sub_str = json.dumps(sub_data)
		self.send(sub_str)
#		logging.info('Send : ' + sub_str)


if __name__ == '__main__':
	logging.basicConfig(level = logging.INFO, filename = 'ltc.log')
	logging.basicConfig(level = logging.WARNING, filename = 'trade.log')
	try:
		ws = DummyClient('wss://api.huobi.com/ws', protocols = ['chat'])
		ws.connect()
		ws.run_forever()
	except KeyboardInterrupt:
		ws.close()
