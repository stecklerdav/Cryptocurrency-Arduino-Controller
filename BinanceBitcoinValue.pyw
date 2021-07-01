
from tkinter import *
from tkinter.ttk import *
import websocket
import threading 
import time
import math
import sys
import glob
import serial
import serial.tools.list_ports


def serial_ports():
	global ports;
	if(sys.platform.startswith('win')):
		ports = ['COM%s' % (i + 1) for i in range(256)]
	elif(sys.platform.startswith('linux') or sys.platform.startswith('cygwin')):
		# this excludes your current terminal "/dev/tty"
		ports = glob.glob('/dev/tty[A-Za-z]*')
	elif(sys.platform.startswith('darwin')):
		ports = glob.glob('/dev/tty.*')
	else:
		raise EnvironmentError('Unsupported platform')

	result = []
	for port in ports:
		try:
			s = serial.Serial(port)
			s.close()
			result.append(port)
		except (OSError, serial.SerialException):
			pass
	print(result)
	return result


def on_select_ports(event=None):
    # get selection from event    
    print("event.widget:", event.widget.get())
    # or get selection directly from combobox
    print("comboboxes: ", puerto.get())


def on_message(ws,message):
	global valor_
	inicial = message.index("c")
	final	= message.index("h")	
	valor_ = message[inicial+3:final-2]# message[141:157];		
	print(valor_);
	valorCryptoTRealLabel.config(text=valor_[1:11])
	historialCrypto.insert(END,valor_ + time.ctime());
	if(float(valor_[1:11]) < (float(precioConsigna))):
		print("Minera Apagada")
		loadimages = PhotoImage(file="redButton.png")
		photoimages = loadimages.subsample(30, 30)
		#if(estadoMina.state == 'enable'):	
		UART.write(b'L');
	else:
		print("Minera Encendida")
		loadimages = PhotoImage(file="greenButton.png")
		photoimages = loadimages.subsample(30, 30)
		#if(estadoMina.state == 'enable'):	
		UART.write(b'H');		
	#time.sleep(1)
	estadoMina.config(image = photoimages)
	estadoMina.photo = photoimages;		
	print(time.ctime());
				
def on_close(ws):
	print('closed');

def moneda(event):
	global socket;
	global ws;
	global evento;
	global task_Socket;
	global botonLogoMoneda;
	
	ws.close(status=websocket.STATUS_PROTOCOL_ERROR)
	#time.sleep(0.5)	
	#del ws
	if (event.widget.get() =="Bitcoin BTC"):
		socket = f'wss://stream.binance.com:9443/ws/btcusdt@kline_1m';
		loadimage = PhotoImage(file="bitcoin.png")
		photoimage = loadimage.subsample(14, 14)		
	elif (event.widget.get() =="Ethereum ETH"):
		socket = f'wss://stream.binance.com:9443/ws/ethusdt@kline_1m';
		loadimage = PhotoImage(file="ethereum.png")
		photoimage = loadimage.subsample(23, 23)			
	elif (event.widget.get() =="Dogecoin DOGE"):
		socket = f'wss://stream.binance.com:9443/ws/dogeusdt@kline_1m';	
		loadimage = PhotoImage(file="dogecoin.png")
		photoimage = loadimage.subsample(14, 14)		
	elif (event.widget.get() =="Litecoin LTC"):
		socket = f'wss://stream.binance.com:9443/ws/ltcusdt@kline_1m';
		loadimage = PhotoImage(file="litecoin.png")
		photoimage = loadimage.subsample(14, 14)
	elif (event.widget.get() =="Binance coin BNB"):
		socket = f'wss://stream.binance.com:9443/ws/bnbusdt@kline_1m';
		loadimage = PhotoImage(file="binancecoin.png")
		photoimage = loadimage.subsample(14, 14)	
	elif (event.widget.get() =="Cardano ADA"):
		socket = f'wss://stream.binance.com:9443/ws/adausdt@kline_1m';
		loadimage = PhotoImage(file="cardano.png")
		photoimage = loadimage.subsample(14, 14)	
	elif (event.widget.get() =="Shiba Inu SHIB"):
		socket = f'wss://stream.binance.com:9443/ws/shibusdt@kline_1m';
		loadimage = PhotoImage(file="shibacoin.png")
		photoimage = loadimage.subsample(13, 13)			
	else:
		socket = f'wss://stream.binance.com:9443/ws/ethusdt@kline_1m';
		loadimage = PhotoImage(file="ethereum.png")
		photoimage = loadimage.subsample(14, 14)
	
	botonLogoMoneda.config(image = photoimage)
	botonLogoMoneda.photo = photoimage;
	
	valorCryptoTRealLabel.config(text="          --")	

	print(event.widget.get());  
	historialCrypto.insert(END,event.widget.get());	
	task_Socket = threading.Thread(target=BinanceConnect);	
	task_Socket.start();	
	print(socket)	


def conexionUART(event):
	global UART;
	print(event.widget.get()[0:5])
	if(UART.isOpen()==True):
		UART.close();


	UART = serial.Serial(event.widget.get()[0:5],'9600',timeout = 1);
	time.sleep(2);	
	print(event.widget.get()[0:5])	
	UART.write(b'A');
	t = UART.read();
	print(t)
	if( t == b'B'):
		print("Arduino conectado")
		loadimage_ = PhotoImage(file="greenButton_.png")
		estadoMina.config(state = 'enable')	
		historialCrypto.insert(END,"Arduino Conectado OK");		
	else:
		print("No es un Arduino")
		loadimage_ = PhotoImage(file="redButton_.png")
		historialCrypto.insert(END,"Arduino No Conectado");
		UART.close();
		estadoMina.config(state = 'disabled')	
		time.sleep(2)
	
	photoimage_ = loadimage_.subsample(30, 30)
	estadoArduino.config(image = photoimage_)
	estadoArduino.photo = photoimage_;

def consignaCallback(): #compara el precio actual con el precio fijado	
	global precioConsigna
	
	precioConsigna = valorEsperado.get();	#print(precioConsigna)#valor deseado e introducido por el minero
	#print(valor_)#valor del mercado
def clickActualizacion(event):
	puerto['values']= (serial.tools.list_ports.comports());
	

def puertoArduino(event = None):
	return serial.tools.list_ports.comports()
def salir():
	window.destroy();
def GraphicUserInterface():
	global socket;
	global window;	
	window = Tk();	
	window.resizable(False, False)
	window.geometry('500x390');#('560x400');
	window.iconbitmap('logo_icono.ico')
	window.title("AntMiner - Controller - Arduino");
	

	def donothing():
		filewin = Toplevel(window)
		button = Button(filewin, text="Do nothing button")
		button.pack()
	menubar = Menu(window) 
	filemenu = Menu(menubar, tearoff=0)
	filemenu.add_command(label="New", command=donothing)
	filemenu.add_command(label="Open", command=donothing)
	filemenu.add_command(label="Save", command=donothing)
	filemenu.add_command(label="Save as...", command=donothing)
	filemenu.add_command(label="Close", command=donothing)
	filemenu.add_separator()
	filemenu.add_command(label="Exit", command=window.quit)
	menubar.add_cascade(label="File", menu=filemenu)
	editmenu = Menu(menubar, tearoff=0)
	editmenu.add_command(label="Undo", command=donothing)
	editmenu.add_separator()
	editmenu.add_command(label="Cut", command=donothing)
	editmenu.add_command(label="Copy", command=donothing)
	editmenu.add_command(label="Paste", command=donothing)
	editmenu.add_command(label="Delete", command=donothing)
	editmenu.add_command(label="Select All", command=donothing)
	menubar.add_cascade(label="Edit", menu=editmenu)
	helpmenu = Menu(menubar, tearoff=0)
	helpmenu.add_command(label="Help Index", command=donothing)
	helpmenu.add_command(label="About...", command=donothing)
	menubar.add_cascade(label="Help", menu=helpmenu)
	window.config(menu=menubar);

	#frame = Frame(window);
	#frame.pack();

	global puerto;
	puerto = Combobox(window,state="readonly");		
	puerto['values']= (puertoArduino());
	puerto.current(0) ;#set the selected item
	puerto.place(x=170, y=1, width=300, height=30)
	#puerto.bind('<<ComboboxSelected>>',on_select_ports)
	puerto.bind('<<ComboboxSelected>>',conexionUART)
	puerto.bind('<Button-1>', clickActualizacion)#selecciono y detecta que se quito el arduino de la lista
	
	global exchange;
	exchange = Combobox(window,state="readonly", font=("comics sans", 10),justify='center');
	exchange['values']= ("Binance", "CoinMarketCap","CoinBase", "Investing", "CryptoBuyer", "OKEx");
	exchange.current(0) ;#set the selected item
	exchange.place(x=1, y=1, width=152, height=30)
	#exchange.grid(column=0, row=0);

	crypto = Combobox(window,state="readonly", font=("comics sans", 10),justify='center');
	crypto['values']= ("Bitcoin BTC", "Ethereum ETH", "Dogecoin DOGE", "Litecoin LTC","Binance coin BNB","Cardano ADA","Shiba Inu SHIB");
	crypto.current(0); #set the selected item
	#crypto.grid(column=0, row=1);
	crypto.place(x=1, y=35, width=152, height=30)
	crypto.bind('<<ComboboxSelected>>',moneda)

	global botonLogoMoneda;
	loadimage_1 = PhotoImage(file="bitcoin.png")
	photoimage_1 = loadimage_1.subsample(14, 14)
	botonLogoMoneda = Button(window, image =photoimage_1)
	botonLogoMoneda.place(x=1, y=80)

	precioRequeridoLabel = Label(window, text="Precio Deseado ($)", font=("calibri", 10));
	precioRequeridoLabel.place(x=12, y=230, width=152, height=30)
	
	global valorEsperado;
	valorEsperado = Entry(window,font=("calibri", 12),justify='center')
	valorEsperado.place(x=1, y=260 ,width=152, height=30)
	#valorEsperado.bind("<Key>", cuandoEscriba)
	#valorEsperado.bind("<Double-1>", dobleclick)

	global Consigna;
	Consigna = Button(window, text ="Actualizar Precio", command =consignaCallback)
	Consigna.grid(column=0, row=3);
	Consigna.place(x=1, y=300, width=152, height=30)
	

	valorL = Label(window, text="Historial", font=("calibri", 10));
	valorL.place(x=280, y=40)

	valorDeMercadoLabel = Label(window, text="Valor Mercado ($)", font=("calibri", 12));
	valorDeMercadoLabel.place(x=240, y=265)

	antminerLabel = Label(window, text="   AntMiner", font=("calibri", 14,"italic","bold"));
	antminerLabel.place(x=1, y=330)

	global historialCrypto;	
	historialCrypto = Listbox ( window,fg = "Blue",width= 40,height = 12 );		
	historialCrypto.place(x=170, y=65, width=300, height=200)

	scrollbar = Scrollbar(window,command = historialCrypto.yview );
	scrollbar.place(x=475, y=65, width=20, height=200)
	historialCrypto.config(yscrollcommand = scrollbar.set)	

	global estadoMina;
	loadimage = PhotoImage(file="greenButton.png")
	photoimage = loadimage.subsample(30, 30)
	estadoMina = Button(window, image = photoimage)
	estadoMina.place(x=123, y=330)
	estadoMina['state'] = 'disabled'

	global estadoArduino;
	loadimage_ = PhotoImage(file="redButton_.png")
	photoimage_ = loadimage_.subsample(30, 30)
	estadoArduino = Button(window, image = photoimage_)
	estadoArduino.place(x=470, y=1)

	global valorCryptoTRealLabel;	
	valorCryptoTRealLabel = Label(window, text="          --", font=("calibri", 30, "italic"));
	valorCryptoTRealLabel.place(x=200, y=290)	

	window.mainloop();
def BinanceConnect():
	#Extraccion del valor BTC de Binance
	global ws;
	global socket;	
	

	ws = websocket.WebSocketApp(socket,on_message = on_message, on_close = on_close);
	ws.keep_running = False
	ws.run_forever();

if __name__ == "__main__":	
	global task_Socket;	
	valor_="1000000000.0";
	precioConsigna = "00.0";
	UART = serial.Serial(None,'9600');
	UART.close();	
	
	print (puertoArduino())	
	socket = f'wss://stream.binance.com:9443/ws/btcusdt@kline_1m';		
	task_GUI = threading.Thread(target=GraphicUserInterface);
	task_Socket = threading.Thread(target=BinanceConnect);
	
	task_GUI.start();
	task_Socket.start();