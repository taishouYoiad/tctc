# -*- coding: UTF-8 -*-
import tornado.ioloop
import tornado.web
import json
import os

html_tmp1 = "<html><p>资金: {0}</p> <p>莱特币: {1}</p> <form action='/account' method='post'><input type='submit' value='reset'> </form></html>"

html_tmp2 = '''<html>
<form action="/order" method="post">
买入价1: {0[0]} 预设数:{1[0]} 实际买入:{2[0]}-{3[0]}  设置价:<input type="text" name="buy1" /> 个数<input type="text" name="buynum1" /><p />
买入价2: {0[1]} 预设数:{1[1]} 实际买入:{2[1]}-{3[1]} 设置价:<input type="text" name="buy2" /> 个数<input type="text" name="buynum2" /><p />
买入价3: {0[2]} 预设数:{1[2]} 实际买入:{2[2]}-{3[2]} 设置价:<input type="text" name="buy3" /> 个数<input type="text" name="buynum3" /><p />
买入价4: {0[3]} 预设数:{1[3]} 实际买入:{2[3]}-{3[3]} 设置价:<input type="text" name="buy4" /> 个数<input type="text" name="buynum4" /><p />
买入价5: {0[4]} 预设数:{1[4]} 实际买入:{2[4]}-{3[4]} 设置价:<input type="text" name="buy5" /> 个数<input type="text" name="buynum5" /><p />
买入价6: {0[5]} 预设数:{1[5]} 实际买入:{2[5]}-{3[5]} 设置价:<input type="text" name="buy6" /> 个数<input type="text" name="buynum6" /><p />
买入价7: {0[6]} 预设数:{1[6]} 实际买入:{2[6]}-{3[6]} 设置价:<input type="text" name="buy7" /> 个数<input type="text" name="buynum7" /><p />
买入价8: {0[7]} 预设数:{1[7]} 实际买入:{2[7]}-{3[7]} 设置价:<input type="text" name="buy8" /> 个数<input type="text" name="buynum8" /><p />
买入价9: {0[8]} 预设数:{1[8]} 实际买入:{2[8]}-{3[8]} 设置价:<input type="text" name="buy9" /> 个数<input type="text" name="buynum9" /><p />
买入价10: {0[9]} 预设数:{1[9]} 实际买入:{2[9]}-{3[9]} 设置价:<input type="text" name="buy10" /> 个数<input type="text" name="buynum10" /><p />
<p>------------------------------------------------</p>
卖出价1: {4[0]} 预设数:{5[0]} 实际卖出:{6[0]}-{7[0]} 设置价:<input type="text" name="sell1" /> 个数<input type="text" name="sellnum1" /><p />
卖出价2: {4[1]} 预设数:{5[1]} 实际卖出:{6[1]}-{7[1]} 设置价:<input type="text" name="sell2" /> 个数<input type="text" name="sellnum2" /><p />
卖出价3: {4[2]} 预设数:{5[2]} 实际卖出:{6[2]}-{7[2]} 设置价:<input type="text" name="sell3" /> 个数<input type="text" name="sellnum3" /><p />
卖出价3: {4[3]} 预设数:{5[3]} 实际卖出:{6[3]}-{7[3]} 设置价:<input type="text" name="sell4" /> 个数<input type="text" name="sellnum4" /><p />
卖出价3: {4[4]} 预设数:{5[4]} 实际卖出:{6[4]}-{7[4]} 设置价:<input type="text" name="sell5" /> 个数<input type="text" name="sellnum5" /><p />
卖出价3: {4[5]} 预设数:{5[5]} 实际卖出:{6[5]}-{7[5]} 设置价:<input type="text" name="sell6" /> 个数<input type="text" name="sellnum6" /><p />
卖出价3: {4[6]} 预设数:{5[6]} 实际卖出:{6[6]}-{7[6]} 设置价:<input type="text" name="sell7" /> 个数<input type="text" name="sellnum7" /><p />
卖出价3: {4[7]} 预设数:{5[7]} 实际卖出:{6[7]}-{7[7]} 设置价:<input type="text" name="sell8" /> 个数<input type="text" name="sellnum8" /><p />
卖出价3: {4[8]} 预设数:{5[8]} 实际卖出:{6[8]}-{7[8]} 设置价:<input type="text" name="sell9" /> 个数<input type="text" name="sellnum9" /><p />
卖出价3: {4[9]} 预设数:{5[9]} 实际卖出:{6[9]}-{7[9]} 设置价:<input type="text" name="sell10" /> 个数<input type="text" name="sellnum10" /><p />
</p>
<input type="submit" value="Submit">
</form>

<form action="/close" method="post">
<input type="submit" value="关闭系统">
</form>
<p></p>
<form action="/open" method="post">
<input type="submit" value="开启系统">
</form>
</html>
'''

html_tmp3_1 = '''<html>
<head>
<script type="text/javascript" src="/static/js/jquery-1.2.6.min.js"></script>
<script type="text/javascript" src="/static/js/jquery.flot.js"></script>
<script type="text/javascript" src="/static/js/jquery.graphTable-0.2.js"></script>
</head>
<body>
<table class="tablebox" id="table1" width="500" style="display:none">
	<thead>
		<caption>trend</caption>
		<tr>
			<th>&nbsp;</th>
			<th>cny</th>
		</tr>
	</thead>
	<tbody>
'''
html_tmp3_2 = '''
	</tbody>
</table>
<script type="text/javascript">
	$('#table1').graphTable({series: 'columns'});
	console.log("asdasdas")
</script>
</body>
</html>
'''

def getFileContent(filename):
	fp = open(filename, 'r')
	data = fp.read()
	fp.close()
	try:
		data = json.loads(data)
	except:
		data = data
	return data


class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("<html><a href='/account'>账户查询</a> <a href='/order'>下单设置</a> <a href='/list'>成交记录</a> <a href='/trend'>资金曲线</a></html>")

class CloseHandler(tornado.web.RequestHandler):
	def post(self):
		os.system("kill -9 `ps -ef| grep fishltc| awk '{print $2}'`")
		self.write('close system')

class OpenHandler(tornado.web.RequestHandler):
	def post(self):
		os.system("kill -9 `ps -ef| grep fishltc| awk '{print $2}'`")
		os.system('nohup python fishltc.py > a.log 2>&1 &')
		self.write('open system')
	

class AccountHandler(tornado.web.RequestHandler): 
	def get(self):
		data = getFileContent('account.json')
		self.write(html_tmp1.format(data['cny'], data['ltc']))
	def post(self):
		s = json.dumps({'cny' : 10000, 'ltc' : 0})
		fp = open('account.json', 'w+')
		fp.write(s)
		fp.close()
		fp = open('trend.log', 'w+')
		fp.write(json.dumps({'date' : 0, 'cny' : 10000}) + '\r\n')
		fp.close()
		self.write('-ok')
		

class PlanHandler(tornado.web.RequestHandler):
	def get(self):
		data = getFileContent('plan.json')
		buy = data['buy']
		sell = data['sell']
		#h = html_tmp2.format(buy[0][0], buy[1][0], buy[2][0], sell[0][0], sell[1][0], sell[2][0], buy[0][1], buy[1][1], buy[2][1], sell[0][1], sell[1][1], sell[2][1], buy[0][2], buy[1][2], buy[2][2], sell[0][2], sell[1][2], sell[2][2], buy[0][3], buy[1][3], buy[2][3], sell[0][3], sell[1][3], sell[2][3])
		buyPrice = []
		setBuyNum = []
		actBuyPrice = []
		actBuyNum = []
		for i in buy:
			buyPrice.append(i[0])
			setBuyNum.append(i[1])
			actBuyPrice.append(i[2])
			actBuyNum.append(i[3])
		sellPrice = []
		setSellNum = []
		actSellPrice = []
		actSellNum = []
		for i in sell:
			sellPrice.append(i[0])
			setSellNum.append(i[1])
			actSellPrice.append(i[2])
			actSellNum.append(i[3])
		h = html_tmp2.format(buyPrice, setBuyNum, actBuyPrice, actBuyNum, sellPrice, setSellNum, actSellPrice, actSellNum)
		self.write(h)
	def post(self):
		buys = []
		buynums = []
		sells = []
		sellnums = []
		for i in range(1, 11):
			buys.append(self.get_argument('buy' + str(i)))
			buynums.append(self.get_argument('buynum' + str(i)))
			sells.append(self.get_argument('sell' + str(i)))
			sellnums.append(self.get_argument('sellnum' + str(i)))
		data = getFileContent('plan.json')
		for i in range(0, 10):
			if buys[i]:
				data['buy'][i][0] = buys[i]
			if buynums[i]:
				data['buy'][i][1] = buynums[i]
			if sells[i]:
				data['sell'][i][0] = sells[i]
			if sellnums[i]:
				data['sell'][i][1] = sellnums[i]
		fp = open('plan.json', 'w+')
		fp.write(json.dumps(data))
		fp.close()
		self.write('ook')

class ListHandler(tornado.web.RequestHandler):
	def get(self):
		data =getFileContent('ltc.log')
		self.write(data)

class TrendHandler(tornado.web.RequestHandler):
	def get(self):
		fina_html = html_tmp3_1
		fp = open('trend.log', 'r')
		index = 0
		for line in open('trend.log'):
			data = fp.readline()
			data = json.loads(data)
			fina_html = fina_html + '<tr><th>{0}</th><td>{1}</td></tr>'
			fina_html = fina_html.format(index, data.get('cny'))
			index = index + 1
		fina_html = fina_html + html_tmp3_2
		self.write(fina_html)


settings = {
	"static_path": os.path.join(os.path.dirname(__file__), "static") 
} 
application = tornado.web.Application([  
    (r"/",MainHandler),
    (r"/account",AccountHandler),
    (r"/order",PlanHandler),
	(r"/list",ListHandler),
	(r"/close",CloseHandler),
	(r"/open",OpenHandler),
	(r"/trend", TrendHandler),
], **settings)  
  
if __name__=="__main__":  
    application.listen(9090)  
    tornado.ioloop.IOLoop.instance().start() 
