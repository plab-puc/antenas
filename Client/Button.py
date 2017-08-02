# This Python file uses the following encoding: utf-8
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import Client
import datetime
import time

#Client.Connect()

#Interface
class MyWindow(Gtk.Window):

	def __init__(self):
		instancia = self
		
		Gtk.Window.__init__(self, title="Programa")

		self.log = None
		
		self.extContainer = Gtk.HBox(spacing=6)
		self.add(self.extContainer)

		self.vbox1 = Gtk.VBox(spacing=6)
		self.extContainer.pack_start(self.vbox1, False, False, 0)
		
		self.box = Gtk.HBox(spacing=6)
		self.vbox1.pack_start(self.box, False, False, 0)
		
		self.conectado = Gtk.Label()
		self.conectado.set_markup("<span foreground='red'><b>Desconectado</b></span>")
		self.conectado.set_justify(Gtk.Justification.LEFT)
		self.box.pack_start(self.conectado, 1, 0, 1)
		
		self.bt_refresh = Gtk.Button(None, image=Gtk.Image(stock=Gtk.STOCK_CONNECT))
		self.box.pack_start(self.bt_refresh, 1, 0, 1)
		self.bt_refresh.connect("clicked", self.on_button_connect_clicked)
		
		self.distance_label = Gtk.Label()
		self.distance_label.set_markup("Distância: 20cm")
		self.vbox1.pack_start(self.distance_label, False, True, 0)
		
		self.box_botoes = Gtk.HBox(spacing=6)
		self.vbox1.pack_start(self.box_botoes, False, False, 0)

		self.grid = Gtk.Grid()
		self.box_botoes.pack_start(self.grid, True, True, 0)

		self.bt_frente = Gtk.Button(None, image=Gtk.Image(stock=Gtk.STOCK_GO_UP))
		self.bt_frente.connect("clicked", self.on_button_up_clicked)
		self.grid.attach(self.bt_frente, 0, 0, 1, 1)

		self.bt_tras = Gtk.Button(None, image=Gtk.Image(stock=Gtk.STOCK_GO_DOWN))
		self.bt_tras.connect("clicked", self.on_button_down_clicked)
		self.grid.attach(self.bt_tras, 0, 1, 1, 1)
		
		self.bt_test = Gtk.Button(label="Testar sinal")
		self.bt_test.connect("clicked", self.on_test_clicked)
		self.box_botoes.pack_start(self.bt_test, False, True, 0)
		
		scrolledwindow = Gtk.ScrolledWindow()
		scrolledwindow.set_hexpand(True)
		scrolledwindow.set_vexpand(True)
		self.extContainer.pack_start(scrolledwindow, True, True, 0)

		self.textview = Gtk.TextView()
		self.textbuffer = self.textview.get_buffer()
		self.textbuffer.set_text("")
		scrolledwindow.add(self.textview)

	def on_button_connect_clicked(self, widget):
		if(Client.connected == False):
			print("Conectar")
			Client.Connect()
		else:
			print("Desconectar")
			Client.Close()
		
	def on_test_clicked(self, widget):
		self.TextWrite(">Lendo sinal\n")

		signal = Client.SendAndWait('s')
		
		for i in range(0,10):
			self.TextWrite("Sinal lido "+str(i)+": "+signal[i]+"dBm\n")

	def on_button_up_clicked(self, widget):
		Client.Send('u')

	def on_button_down_clicked(self, widget):
		Client.Send('d')
		
	def OnConnect(self):
		self.conectado.set_markup("<span foreground='green'><b>Conectado</b></span>")
		self.bt_refresh.set_image(Gtk.Image(stock=Gtk.STOCK_DISCONNECT))

		if(self.log == None):
			self.log = open('log.txt', 'w+')

		st = datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y %H:%M:%S')
		win.TextWrite(">>Teste iniciado: "+st+"\n")

	def OnDisconnect(self):
		self.conectado.set_markup("<span foreground='red'><b>Desconectado</b></span>")
		self.bt_refresh.set_image(Gtk.Image(stock=Gtk.STOCK_CONNECT))
		st = datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y %H:%M:%S')
		self.log.write(">>Fim do teste: "+st+"\n")
		self.log.close()
		self.log = None
	
	def TextWrite(self, text):
		end_iter = self.textbuffer.get_end_iter()
		self.textbuffer.insert(end_iter, text)
		self.log.write(text)
	
	def TextClear(self):
		self.textbuffer = self.textview.get_buffer()
		self.textbuffer.set_text("")

win = MyWindow()

Client.connectCallback = win.OnConnect;
Client.disconnectCallback = win.OnDisconnect;

win.connect("delete-event", Gtk.main_quit)

win.show_all()
Gtk.main()

st = datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y %H:%M:%S')
win.log.write(">>Fim do teste: "+st+"\n")
win.log.close()
