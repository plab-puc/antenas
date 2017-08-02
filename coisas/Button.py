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
		
		self.log = open('log.txt', 'w+')
		
		Gtk.Window.__init__(self, title="Programa")
		
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
		
		self.bt_refresh = Gtk.Button(None, image=Gtk.Image(stock=Gtk.STOCK_REFRESH))
		self.box.pack_start(self.bt_refresh, 1, 0, 1)
		self.bt_refresh.connect("clicked", self.on_button_connect_clicked)
		
		self.distance_label = Gtk.Label()
		self.distance_label.set_markup("Distância: 20cm")
		self.vbox1.pack_start(self.distance_label, False, True, 0)
		
		self.box_botoes = Gtk.HBox(spacing=6)
		self.vbox1.pack_start(self.box_botoes, False, False, 0)

		self.grid = Gtk.Grid()
		self.box_botoes.pack_start(self.grid, True, True, 0)

		self.bt_esq = Gtk.Button(None, image=Gtk.Image(stock=Gtk.STOCK_GO_BACK))
		self.bt_esq.connect("clicked", self.on_button_left_clicked)
		self.grid.attach(self.bt_esq, 0, 0, 1, 1)

		self.bt_dir = Gtk.Button(None, image=Gtk.Image(stock=Gtk.STOCK_GO_FORWARD))
		self.bt_dir.connect("clicked", self.on_button_right_clicked)
		self.grid.attach(self.bt_dir, 1, 0, 1, 1)
		
		self.grid2 = Gtk.Grid()
		self.box_botoes.pack_start(self.grid2, True, True, 0)

		self.bt_frente = Gtk.Button(None, image=Gtk.Image(stock=Gtk.STOCK_GO_UP))
		self.bt_frente.connect("clicked", self.on_button_up_clicked)
		self.grid2.attach(self.bt_frente, 0, 0, 1, 1)

		self.bt_tras = Gtk.Button(None, image=Gtk.Image(stock=Gtk.STOCK_GO_DOWN))
		self.bt_tras.connect("clicked", self.on_button_down_clicked)
		self.grid2.attach(self.bt_tras, 0, 1, 1, 1)
		
		self.bt_test = Gtk.Button(label="Testar sinal")
		self.bt_test.connect("clicked", self.on_test_clicked)
		self.vbox1.pack_start(self.bt_test, False, True, 0)

		self.button = Gtk.Button(label="Desconectar")
		self.button.connect("clicked", self.on_button_clicked)
		self.vbox1.pack_start(self.button, False, True, 0)
		
		scrolledwindow = Gtk.ScrolledWindow()
		scrolledwindow.set_hexpand(True)
		scrolledwindow.set_vexpand(True)
		self.extContainer.pack_start(scrolledwindow, True, True, 0)

		self.textview = Gtk.TextView()
		self.textbuffer = self.textview.get_buffer()
		self.textbuffer.set_text("")
		scrolledwindow.add(self.textview)

	def on_button_connect_clicked(self, widget):
		print("Conectar")
		Client.Connect()
		
	def on_test_clicked(self, widget):
		signal = Client.SendAndWait('S')
		
		for i in range(0,10):
			self.TextWrite("Sinal lido(dist +"+signal[1]+", rot "+signal[0]+"): "+signal[i+2]+"dBm\n")

	def on_button_clicked(self, widget):
		print("Goodbye")
		Client.Close()

	def on_button_up_clicked(self, widget):
		Client.Send('u')

	def on_button_down_clicked(self, widget):
		Client.Send('d')
		
	def on_button_left_clicked(self, widget):
		Client.Send('l')
		
	def on_button_right_clicked(self, widget):
		Client.Send('r')
		
	def OnConnect(self):
		self.conectado.set_markup("<span foreground='green'><b>Conectado</b></span>")
		st = datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y %H:%M:%S')
		win.TextWrite(">>Teste iniciado: "+st+"\n")
	
	def TextWrite(self, text):
		end_iter = self.textbuffer.get_end_iter()
		self.textbuffer.insert(end_iter, text)
		self.log.write(text)
	
	def TextClear(self):
		self.textbuffer = self.textview.get_buffer()
		self.textbuffer.set_text("")

win = MyWindow()

Client.connectCallback = win.OnConnect;

win.connect("delete-event", Gtk.main_quit)

win.show_all()
Gtk.main()

st = datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y %H:%M:%S')
win.log.write(">>Fim do teste: "+st+"\n")
win.log.close()
