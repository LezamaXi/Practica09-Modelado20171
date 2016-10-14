import sys
from PyQt4 import QtGui, QtCore, uic
from random import randint 

class Snake():
    
    def __init__(self):
        self.color = (206, 254, 241)
        self.casillas = [[5,4],[5,5],[5,6], [5,7], [5,8], [5,9], [5,10],[5,11], [5,12]]
        self.tam = len(self.casillas)
        self.direccion = "Derecha"

class MainWindow(QtGui.QMainWindow):

    def __init__(self):

        super(MainWindow, self).__init__()
        uic.loadUi('servidor.ui', self)
        self.setStyleSheet("QMainWindow {background-color: #ACE7EF;}")
        self.pushButton_3.hide()
        self.juego_empezado = False
        self.juego_pausado = False
        self.timer = None
        self.timer_comida = None 
        self.num_serpientes = []
        self.comida = []
        self.tabla()
        self.rellenar_tab()
        self.tableWidget.setSelectionMode(QtGui.QTableWidget.NoSelection)
        self.spinBox_2.valueChanged.connect(self.actualizar_tabla) 
        self.spinBox_3.valueChanged.connect(self.actualizar_tabla)
        self.spinBox.valueChanged.connect(self.actualizar_timer)
        self.pushButton_2.clicked.connect(self.comenzar_juego)
        self.pushButton_3.clicked.connect(self.terminar_juego)
        self.show()

    def mover_serpientes(self):
       
        for serpiente in self.num_serpientes:
            if self.choca_con_el(serpiente):
                self.num_serpientes.remove(serpiente)
                self.rellenar_tab()
                serpiente_1 = Snake()
                self.num_serpientes = [serpiente_1]
            self.tableWidget.item(serpiente.casillas[0][0],serpiente.casillas[0][1]).setBackground(QtGui.QColor(206, 254, 241))
            x = 0
            for tupla in serpiente.casillas[0: len(serpiente.casillas)-1]:
                x += 1
                tupla[0] = serpiente.casillas[x][0]
                tupla[1] = serpiente.casillas[x][1]
            
            if serpiente.direccion is "Abajo":
                if serpiente.casillas[-1][0] + 1 < self.tableWidget.rowCount():
                    serpiente.casillas[-1][0] += 1
                else:
                    serpiente.casillas[-1][0] = 0
            if serpiente.direccion is "Derecha":
                if serpiente.casillas[-1][1] + 1 < self.tableWidget.columnCount():
                    serpiente.casillas[-1][1] += 1
                else:
                    serpiente.casillas[-1][1] = 0
            if serpiente.direccion is "Arriba":
                if serpiente.casillas[-1][0] != 0:
                    serpiente.casillas[-1][0] -= 1
                else:
                    serpiente.casillas[-1][0] = self.tableWidget.rowCount()-1
            if serpiente.direccion is "Izquierda":
                if serpiente.casillas[-1][1] != 0:
                    serpiente.casillas[-1][1] -= 1
                else:
                    serpiente.casillas[-1][1] = self.tableWidget.columnCount()-1
        self.dibujar_serpientes()
    
    def comenzar_juego(self):
        
        if not self.juego_empezado:
            self.pushButton_3.show()
            serpiente_1 = Snake()
            self.num_serpientes.append(serpiente_1)
            self.pushButton_2.setText("Pausar el Juego")
            self.dibujar_serpientes()
            self.timer = QtCore.QTimer(self)
            self.timer_comida = QtCore.QTimer(self)
            self.timer.timeout.connect(self.mover_serpientes)
            self.timer.start(150)
            self.timer_comida.start(100)
            self.timer_comida.timeout.connect(self.crear_comida) 
            self.timer_comida.start(3000) 
            self.tableWidget.installEventFilter(self)
            self.juego_empezado = True 
        elif self.juego_empezado and not self.juego_pausado:
            self.timer.stop()
            self.timer_comida.stop()
            self.juego_pausado = True
            self.pushButton_2.setText("Reanudar el Juego")
        elif self.juego_pausado:
            self.timer.start()
            self.timer_comida.start()
            self.juego_pausado = False
            self.pushButton_2.setText("Pausar el Juego")

    def eventFilter(self, source, event):
        
        if (event.type() == QtCore.QEvent.KeyPress and
            source is self.tableWidget):
                key = event.key() 
                if (key == QtCore.Qt.Key_Up and
                    source is self.tableWidget):
                    for serpiente in self.num_serpientes:
                        if serpiente.direccion is not "Abajo":
                            serpiente.direccion = "Arriba"
                elif (key == QtCore.Qt.Key_Down and
                    source is self.tableWidget):
                    for serpiente in self.num_serpientes:
                        if serpiente.direccion is not "Arriba":
                            serpiente.direccion = "Abajo"
                elif (key == QtCore.Qt.Key_Right and
                    source is self.tableWidget):
                    for serpiente in self.num_serpientes:
                        if serpiente.direccion is not "Izquierda":
                            serpiente.direccion = "Derecha"
                elif (key == QtCore.Qt.Key_Left and
                    source is self.tableWidget):
                    for serpiente in self.num_serpientes:
                        if serpiente.direccion is not "Derecha":
                            serpiente.direccion = "Izquierda"
        return QtGui.QMainWindow.eventFilter(self, source, event)
    
    def terminar_juego(self):
        
        self.num_serpientes = []
        self.comida = []
        self.timer_comida.stop()
        self.timer.stop()
        self.juego_empezado = False 
        self.pushButton_3.hide()
        self.pushButton_2.setText("Inicia Juego") 
        self.rellenar_tab()

    def choca_con_el(self, serpiente):
       
        for cola in serpiente.casillas[0:len(serpiente.casillas)-2]: 
            if serpiente.casillas[-1][0] == cola[0] and serpiente.casillas[-1][1] == cola[1]:
                return True
        return False
    
    def actualizar_timer(self):
        valor = self.spinBox.value()
        self.timer.setInterval(valor)
     

    def rellenar_tab(self):
        for i in range(self.tableWidget.rowCount()):
            for j in range(self.tableWidget.columnCount()):
                self.tableWidget.setItem(i,j, QtGui.QTableWidgetItem())
                self.tableWidget.item(i,j).setBackground(QtGui.QColor(206, 254, 241))

    
    def dibujar_serpientes(self):
        for serpiente in self.num_serpientes:
            for cola in serpiente.casillas:
                self.tableWidget.item(cola[0], cola[1]).setBackground(QtGui.QColor(165, 108, 193))
    
    def crear_comida(self):
        posicion = False
        while not posicion:
            i = randint(0, self.tableWidget.rowCount()-1) 
            j = randint(0, self.tableWidget.columnCount()-1)
            for serpiente in self.num_serpientes:
                if [i,j] in serpiente.casillas:
                    break
            posicion = True
            self.comida.append([i,j])
            self.tableWidget.item(i,j).setBackground(QtGui.QColor(166, 172, 236))

    def tabla(self):
        
        self.tableWidget.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setResizeMode(QtGui.QHeaderView.Stretch)

    def actualizar_tabla(self):
        
        num_filas = self.spinBox_3.value()
        num_columnas = self.spinBox_2.value()
        self.tableWidget.setRowCount(num_filas)  
        self.tableWidget.setColumnCount(num_columnas)
        self.rellenar_tab()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ventana = MainWindow() 
    sys.exit(app.exec_()) 