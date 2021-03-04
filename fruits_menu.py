import unicodedata
import datetime
import os

### 引数textの全角文字数カウント
def get_zen_count(text):
	count=0
	for c in text:
		if unicodedata.east_asian_width(c) in "FWA":
			count +=1
	return count


### 商品クラス
class Item:
	def __init__(self,item_code,item_name,price,cnt=0):
		self.item_code=item_code
		self.item_name=item_name
		self.price=price
		self.item_cnt=cnt
	
	def get_price(self):
		return self.price * self.item_cnt


### 注文クラス
class Order:
	def __init__(self,item_master):
		self.item_order_list=[]
		self.item_master=item_master
		self.order_cnt = 0
		self.order_price = 0
	
	def code_to(self,code):                # 商品コードを渡すと,商品名と値段を返す
		for C_key_item in self.item_master:
			if C_key_item.item_code == code:
				price = str(C_key_item.price)
				return C_key_item.item_name + " " + price + "円"
		print("該当する商品がありません")
		return False

	def add_item_order(self,item_code,item_cnt):
		for C_key_item in self.item_master:
			if C_key_item.item_code == item_code:
				self.item_order_list.append(item_code)
				C_key_item.item_cnt += item_cnt
				return
		print("該当する商品がありません")
	
	def view_item_master(self):
		self.order_cnt=0
		self.order_price=0
		for item in self.item_master:                         #注文の合計を表示
			name_width = 9-get_zen_count(item.item_name)
			print(f"［{item.item_code}:{item.item_name:{name_width}}{item.price}円 x{item.item_cnt:3}点 ={item.get_price():5}円］")
			self.order_cnt += item.item_cnt
			self.order_price += item.get_price()
		# 合計点数、合計金額の表示
		print(" ――――――――――――――――――――――――――――――――――――")
		print(f"　合計金額　　　　　　{self.order_cnt:3}点　{self.order_price:5}円")
		

	def view_item_list(self):                                 #注文リストを表示
		for item in self.item_order_list:
			print(f"商品コード:{item}",end="")

			#商品コードitemに該当する商品の値段をself.item_master[]から取得
			for C_key_item in self.item_master:
				if C_key_item.item_code == item:
					name_width = 10-get_zen_count(C_key_item.item_name)
					print(f" {C_key_item.item_name:{name_width}} {C_key_item.get_price()}円")

	def receipt_txt(self):                                    #レシートを出力
		# ファイル名「現在日時.txt」を作成
		order_time = datetime.datetime.now()
		file_name = order_time.strftime("order_%Y-%m-%d_%H%M")
		
		# ファイルを開く
		if not os.path.isfile(file_name):
			with open( file_name+".txt", encoding="UTF-8", mode="w") as f:
				# ファイルに書き込む
				self.order_cnt=0
				self.order_price=0
				f.write("\n" + file_name+"\n")
				f.write(" ―――――――――――――――――――――――――――――――――――\n")
				for item in self.item_master:                         #注文の合計を表示
					name_width = 9-get_zen_count(item.item_name)
					f.write(f"［{item.item_code}:{item.item_name:{name_width}}{item.price}円 x{item.item_cnt:3}点 ={item.get_price():5}円］\n")
					# print(f"［{item.item_code}:{item.item_name:{name_width}}{item.price}円 x{item.item_cnt:3}点 ={item.get_price():5}円］")
					self.order_cnt += item.item_cnt
					self.order_price += item.get_price()
				# 合計点数、合計金額の表示
				f.write(" ―――――――――――――――――――――――――――――――――――\n")
				f.write(f"　合計金額　　　　　　 {self.order_cnt:3}点　{self.order_price:5}円\n")
				f.write(f"　お預かり　　　　　　　　　　{self.order_cash:5}円\n")
				f.write(f"　お釣り　　　　　　　　　　　{self.order_cash-self.order_price:5}円\n")
				f.write(" ―――――――――――――――――――――――――――――――――――\n")
				f.write("\n「お買い上げありがとうございました。」\n")
				
			return file_name
		else:
			return "Error"
			


