var items = [];
var total_price;
const Item = class {
	constructor(code, name, price) {
		this.code = code;
		this.name = name;
		this.price = price;
	}
}

// 文字を桁揃え(右埋め)
function padding_right(val,char,n){
	for(; val.length < n; val+=char);
	return val;
}
// 文字を桁揃え(左埋め)
function padding_left(val,char,n){
	for(; val.length < n; val=char+val);
	return val;
}

eel.expose(alert_js);
function alert_js(text){
	alert(text);
}

// [入力クリア] ボタン
input_clear.addEventListener( 'click',order_input_clear , false );
function order_input_clear(){
	item_code.value = "";
	item_name.value = "";
	item_price.value = "";
	item_cnt.value = "0";
	item_price_total.value = "";
}

// ページを読み込んだ時に規定の商品リストを読み込む
window.onload = function(){
	eel.set_item_master_csv("item_master.csv");
	// 注文データのインスタンス生成
	eel.order_init();
}
// [商品リスト読み込み] ボタン read_item_list
read_item_list.addEventListener("change",file_select,false);
function file_select(){
	eel.set_item_master_csv(read_item_list.files[0].name);
}
// 商品リスト<textarea>に１商品を１行追記
eel.expose(item_list_add_item_js);
function item_list_add_item_js(code, name, price){
	if(code==null && name==null && price==null) {
		item_list.value = "";
		items = [];
	} else {
		name = padding_right(name,"　",5);
		price = padding_left(price," ",4);
		item_list.value += code +" "+ name + price + "円\n";
		items.push( new Item(code, name, price) );
	}
}

// 入力された商品コードから商品名・価格をitems[]より取得
item_code.addEventListener("change",code_change,false);
function code_change() {
	item_name.value = "";
	item_price.value = "";
	item_price_total.value = "";

	for (let i in items){
		if( items[i].code == item_code.value){
			item_name.value = items[i].name;
			item_price.value = items[i].price;
			item_price_total.value = item_price.value * item_cnt.value;
		}
	}
}
// 入力された注文数から小計を算出
item_cnt.addEventListener("change",cnt_change,false);
function cnt_change() {
	if( item_price.value != "" ){
		item_price_total.value = item_price.value * item_cnt.value;
	}
}


// [かごに追加] ボタン
add_order.addEventListener( 'click',add_order_js , false );
function add_order_js() {
	if(item_cnt.value == 0){
		alert("注文数を入力して下さい");
		item_cnt.focus();
	}else if (item_name.value=="") {
		alert("商品コードを入力して下さい");
		item_code.focus();
		// document.getElementById('item_code').focus();
	}else{
		order_list.value="";
		// 注文マスターに追加する関数を呼び出し
		eel.add_order_list(item_code.value,item_name.value,item_price.value,item_cnt.value);
		order_input_clear();
	}
}
// 買い物かご(order_list)に追記
eel.expose(order_list_add_write_js);
function order_list_add_write_js(message){
	order_list.value += message;
}


// [支払いキャンセル] ボタン
pay_cancel.addEventListener( 'click',cancel_pay , false );
function cancel_pay(){
	pay_here.textContent="お　会　計";
	for(let i in document.getElementsByClassName("pay_input") ) {
		document.getElementsByClassName("pay_input")[i].style.display="none";
	}
}

// [お会計] ボタン
pay_here.addEventListener( 'click',order_pay , false );
function order_pay(){
	if(order_list.value == ""){
	}else if( pay_here.textContent == "お　会　計"){
		pay_here.textContent="支　払　う";
		for(let i in document.getElementsByClassName("pay_input") ) {
			document.getElementsByClassName("pay_input")[i].style.display="inline";
		}
		cash.focus();
	}else{
		if ( cash.value=="" || cash.value<= 0 || /\D+/.test(cash.value)){
			alert("お支払い金額を入力して下さい。");
			cash.value =""
			cash.focus();
		}else{
			// 清算処理
			eel.order_payment(cash.value);
		}
	}
}
eel.expose(payment_result_js);
function payment_result_js(rst){
	if (rst<0){
		alert((rst*-1)+"円不足しています。");
		cash.focus();
	} else if (rst== 0){
		alert("お買い上げ、ありがとうございました！");
		cash.value="";
		order_list.value="";
		eel.order_init();
		// cancel_pay();
		pay_here.textContent="お　会　計";
		cash.style.display="none";
		cash_label.style.display="none";
		cash_label2.style.display="none";
		pay_cancel.style.display="none";

	}
};
