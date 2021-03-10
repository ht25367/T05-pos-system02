import eel
import desktop
import fruits_menu
import os
import json

app_name="html"
end_point="index.html"
size=(850,600)

### JSONファイルの設定用
def default_method(item):
	if isinstance(item, object) and hasattr(item, '__dict__'):
		return item.__dict__
	else:
		raise TypeError

@ eel.expose
def order_init():
	order_master = fruits_menu.Order()
	with open ("order_master.json","w") as f:
		json.dump( order_master,f, default=default_method,indent=2)

@ eel.expose
def set_item_master_csv(file_name):
	fruits_menu.set_item_master_csv(file_name)

@ eel.expose
def add_order_list(code, name, price, cnt):
	
	# json ファイルを読み込み>インスタンスに代入
	order_data = fruits_menu.Order()
	with open ("order_master.json","r") as f:
		data = json.load(f)
	for item in data["order_list"]:
		order_data.order_list.append(fruits_menu.Item(item["item_code"],item["item_name"],item["item_price"],item["item_cnt"]))
	order_data.order_cnt = data["order_cnt"]
	order_data.order_price = data["order_price"]

	# order の注文追加メソッド
	order_data.add_order_list(code,name,price,cnt)
	with open ("order_master.json","w") as f:
		json.dump( order_data,f, default=default_method,indent=2)

@ eel.expose
def order_payment(cash):
	# json ファイルを読み込み>インスタンスに代入
	order_data = fruits_menu.Order()
	with open ("order_master.json","r") as f:
		data = json.load(f)
	for item in data["order_list"]:
		order_data.order_list.append(fruits_menu.Item(item["item_code"],item["item_name"],item["item_price"],item["item_cnt"]))
	order_data.order_cnt = data["order_cnt"]
	order_data.order_price = data["order_price"]

	# order の清算メソッド
	order_data.order_payment(cash)
	

desktop.start(app_name,end_point,size)
#desktop.start(size=size,appName=app_name,endPoint=end_point)
