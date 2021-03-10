import os
import csv
import unicodedata
import datetime
import eel


### 引数textの全角文字数カウント
def get_zen_count(text):
	count=0
	for c in text:
		if unicodedata.east_asian_width(c) in "FWA":
			count +=1
	return count


### 商品クラス
class Item:
	def __init__(self,code,name,price,cnt):
		self.item_code=code
		self.item_name=name
		self.item_price=price
		self.item_cnt=cnt

### 注文クラス
class Order:
	def __init__(self):
		self.order_list=[]
		self.order_cnt = 0
		self.order_price = 0
	
	def item_data_to_text(self,co,na,pr,n):
		na_width = 10-get_zen_count(na)
		pr_total = str( int(pr)*int(n) ).rjust(5)
		return co.ljust(4) + na.ljust(na_width) + str(pr).rjust(4)+"円" + str(n).rjust(3)+"個   = " + pr_total+"円\n"

	def add_order_list(self,code,name,price,cnt):
		add_flg = 0
		for item in self.order_list:
			if item.item_code == code:
				item.item_code = code
				item.item_name = name
				item.item_price = price
				item.item_cnt = str(int(item.item_cnt) + int(cnt))
				self.order_cnt += int(cnt)
				self.order_price += int(price)*int(cnt)
				add_flg = 1
			# JS に書き出し
			eel.order_list_add_write_js(self.item_data_to_text(item.item_code,item.item_name,item.item_price,item.item_cnt))
		
		if add_flg == 0:
			self.order_cnt += int(cnt)
			self.order_price += int(price)*int(cnt)
			self.order_list.append(Item(code,name,price,cnt))
			# JS に書き出し
			eel.order_list_add_write_js(self.item_data_to_text(code,name,price,cnt))

		eel.order_list_add_write_js("-------------------------------------\n")
		eel.order_list_add_write_js("合計                "+str(self.order_cnt).rjust(3)+"個     "+str(self.order_price).rjust(5)+"円\n")


	def order_payment(self,cash):
		# print(type(cash))   str
		# print(type(self.order_cnt))   int
		# print(type(self.order_price))   int
		cash = int(cash)
		if cash < self.order_price:
			eel.payment_result_js(cash-self.order_price)
		else:
			# おつり計算と表示
			eel.order_list_add_write_js(f"お預かり                      {str(cash).rjust(5)}円\n")
			if cash == self.order_price:
				eel.alert_js(f"{cash}円丁度、お預かりします。")
			else:
				eel.order_list_add_write_js(f"おつり                        {str(int(cash) -self.order_price).rjust(5)}円\n")
				eel.alert_js(f"{cash}円お預かりし、{cash-self.order_price}円のおつりになります。")
			self.receipt_txt(cash)
			eel.payment_result_js(0)
	

	#レシートをファイルに出力
	def receipt_txt(self,cash):
		order_time = datetime.datetime.now()
		file_name = order_time.strftime("order_%Y-%m-%d_%H%M")
		if not os.path.isfile(file_name):
			with open( file_name+".txt", encoding="UTF-8", mode="w") as f:
				# ファイルに書き込む
				# self.order_cnt=0
				# self.order_price=0
				f.write("\n" + file_name+"\n")
				f.write("-------------------------------------\n")
				for item in self.order_list:                         #注文の合計を表示
					f.write(self.item_data_to_text(item.item_code,item.item_name,item.item_price,item.item_cnt))
					# name_width = 9-get_zen_count(item.item_name)
					# f.write(f"［{item.item_code}:{item.item_name:{name_width}}{item.price}円 x{item.item_cnt:3}点 ={item.get_price():5}円］\n")

				# 合計点数、合計金額の表示
				f.write("-------------------------------------\n")
				f.write(f"合計                "+str(self.order_cnt).rjust(3)+"個     "+str(self.order_price).rjust(5)+"円\n")
				f.write(f"お預かり                      {str(cash).rjust(5)}円\n")
				f.write(f"おつり                        {str(int(cash) -self.order_price).rjust(5)}円\n")
				f.write("-------------------------------------\n")
				f.write("\n「お買い上げありがとうございました。」\n")
				return file_name
		else:
			return "Error"


### csvファイルの読み込み
def set_item_master_csv(csv_file):
	with open(csv_file,encoding="utf_8",newline="") as items_csv:
		item_master = csv.reader(items_csv)
		next(item_master)

		# 商品リストを読み込む前にテキストエリアを空にする
		eel.item_list_add_item_js()
		for item in item_master:
			eel.item_list_add_item_js(item[0],item[1],item[2])
	