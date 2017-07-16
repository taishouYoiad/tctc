import json
fp = open('trend.log', 'r')
for i in open('trend.log'):
	x = fp.readline()
	data = json.loads(x)
	print(data.get('date'), data.get('cny'))
	print('----------')
fp.close()
