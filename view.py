import eel
import desktop
import pos_system

app_name="html"
end_point="index.html"
size=(870,600)

@ eel.expose
def order_input():
	pos-system.ordere_input()

desktop.start(app_name,end_point,size)
#desktop.start(size=size,appName=app_name,endPoint=end_point)
