import eel
import fruits_menu
import csv

### csvファイルの読み込み
def set_item_master_csv(csv_file):
	with open(csv_file,encoding="utf_8",newline="") as items_csv:
		item_master = csv.reader(items_csv)
		next(item_master)
		# for文で、アイテム数分リストに.append
		L_items = []
		for item in item_master:
			L_items.append(fruits_menu.Item(item[0],item[1],int(item[2])))

	# 商品クラスの入ったリストを返す
	return L_items


### メイン処理
def order_input():
	# マスタ登録
	item_master = set_item_master_csv("item_master.csv")
	

	# オーダー登録
	order=fruits_menu.Order(item_master)
	order.add_item_order("001",1)
	order.add_item_order("002",1)
	order.add_item_order("003",1)
	
	# オーダー入力
	while True:
		print("\n---現在の注文状況---")
		order.view_item_master()

		while True:
			f_order=input("注文を追加しますか？(y/n)")
			if f_order == "n":
				break
			elif f_order == "y":
				#注文できる商品を表示
				input_code = input("注文する商品のコードを入力して下さい:")
				input_code = input_code.zfill(3)
				order_item = order.code_to(input_code)
				if order_item != False:
					try:
						print(order_item,end=" の")
						input_cnt = int(input("注文数を入力して下さい:"))
						if 0 < input_cnt < 100:
							order.add_item_order(input_code,input_cnt)
							break
						elif input_cnt> 99 :
							print("一度に100個以上注文する事はできません。")
					except ValueError:
						pass
					print("注文可能な数を入力して下さい。")
				
			else:
				print("y か n を入力して下さい：")
				continue
		if f_order == "n":
			print("・\n・\n・")
			order.view_item_master()
			f_order = input("ご注文は以上で宜しいですか？(y/n):")
			if f_order == "y":
				break
	
	# 支払い処理
	print(f"\n合計 {order.order_price}円になります。")
	while True:
		try:
			cash = int(input("お支払い金額を入力して下さい："))
			order.order_cash = cash
			if order.order_price == cash:
				print(f"{cash}円丁度、お預かりします。")
			elif order.order_price < cash:
				print(f"{cash}円、お預かりします。")
				print(f"お釣り {cash-order.order_price}円のお返しになります。")
			else:
				print("金額が足りません。")
				continue

			# レシート.txtを作成
			f_order = order.receipt_txt()
			if f_order != "Error":
				print("レシートのお渡しになります。" + f_order)
				print("ご注文、ありがとうございました！")
			else:
				print("注文が重複しています。")
			break
		except ValueError:
			print("入力された金額を認識できません。")
			pass
	


if __name__ == "__main__":
	order_input()
