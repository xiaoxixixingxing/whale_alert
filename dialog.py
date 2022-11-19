# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'myWindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!
from playsound import playsound

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QThread,pyqtSignal,QObject
from PyQt5.QtWidgets import QApplication,QMainWindow
import time,sys
import json
import requests
import configparser
class Ui_Dialog(QObject):

    sin = pyqtSignal()

    def __init__(self):


        super(Ui_Dialog,self).__init__()
        self.myThread1 = myThread()
        self.sin.connect(self.myThread1.stop)
        self.myThread1.strsin.connect(self.updateText)
        self.myThread1.strsnewin.connect(self.updateText_new)
        self.myThread1.strsclear.connect(self.clearText)



    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(662, 331)
        self.startButton = QtWidgets.QPushButton(Dialog)
        self.startButton.setGeometry(QtCore.QRect(10, 300, 75, 23))
        self.startButton.setObjectName("pushButton")
        self.stopButton = QtWidgets.QPushButton(Dialog)
        self.stopButton.setGeometry(QtCore.QRect(100, 300, 75, 23))
        self.stopButton.setObjectName("pushButton_2")
        self.textBrowser = QtWidgets.QTextBrowser(Dialog)
        self.textBrowser.setGeometry(QtCore.QRect(0, 0, 661, 291))
        self.textBrowser.setObjectName("textBrowser")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.update_tag = 1
        self.startButton.clicked.connect(lambda: self.startOrstop(self.startButton.text()))
        self.stopButton.clicked.connect(lambda: self.startOrstop(self.stopButton.text()))




    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.startButton.setText(_translate("Dialog", "开始监控"))
        self.stopButton.setText(_translate("Dialog", "停止监控"))

    def startOrstop(self,text):
        try:
            print(text)
            myThread1 = myThread()
            self.sin.connect(myThread1.stop)

            if text =='开始监控':
                self.update_tag = 0
                self.textBrowser.clear()
                self.myThread1.flag = 1
                self.myThread1.start()
            elif text == '停止监控':
                self.update_tag = 1
                #self.sin.emit()
        except Exception as e:
            print(e)


    def updateText(self,text):
        self.textBrowser.append(text)

    def updateText_new(self,text):
        self.textBrowser.append("<font color= 'red' > " +text+"ront")

    def clearText(self):
        self.textBrowser.clear()




class myThread(QThread):

    strsin = pyqtSignal(str)
    strsnewin = pyqtSignal(str)
    strsclear = pyqtSignal()


    def __init__(self,parent=None):
        super(myThread,self).__init__(parent)
        self.flag = 1

    def paly_sound(self):
        playsound('ly.mp3')

    def run(self):
        file = './ini.txt'
        con = configparser.ConfigParser()
        con.read(file, encoding='utf-8')

        sections = con.sections()

        items = dict(con.items('config'))
        api_key = items['api_key']
        min_value = items['min_value']
        try:
            tmp_trans = []
            time_start = str(int(time.time() - 600))
            url = 'https://api.whale-alert.io/v1/transactions?api_key={}&start={}&min_value={}&'.format(api_key,
                time_start,min_value)
            # url_state = 'https://api.whale-alert.io/v1/status?api_key=your-api-key-here'

            response = json.loads(requests.get(url=url).text)
            print(response)

            for transaction in response['transactions']:
                tmp_trans.append(transaction['hash'])
                out_line = ' '.join([time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(transaction['timestamp'])),
                                     str(transaction['amount']), transaction['symbol'],
                                     '(' + str(transaction["amount_usd"]) + ' USD' + ')',
                                     transaction['transaction_type'], 'from', transaction['from']['owner'], 'to',
                                     transaction['to']['owner']])
                self.strsin.emit(out_line)
                time.sleep(0.1)
                QtWidgets.QApplication.processEvents()
            time.sleep(15)

            while (True):
                try:
                    self.strsclear.emit()
                    if self.flag == 1:
                        time_start = str(int(time.time() - 600))
                        url = 'https://api.whale-alert.io/v1/transactions?api_key={}&start={}&min_value={}&'.format(api_key,
                            time_start,min_value)
                        # url_state = 'https://api.whale-alert.io/v1/status?api_key=your-api-key-here'

                        response = json.loads(requests.get(url=url).text)
                        #print(response)
                        in_trans = []
                        for transaction in response['transactions']:
                            in_trans.append(transaction['hash'])
                            if 'owner' in transaction['from'] and 'owner' in transaction['to']:
                                out_line = ' '.join([time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(transaction['timestamp'])),
                                                 str(transaction['amount']), transaction['symbol'],
                                                 '(' + str(transaction["amount_usd"]) + ' USD' + ')',
                                                 transaction['transaction_type'], 'from', transaction['from']['owner'], 'to',
                                                 transaction['to']['owner']])
                            else:
                                continue
                            if transaction['hash'] in tmp_trans:
                                self.strsin.emit(out_line)
                                time.sleep(0.01)
                            else:
                                self.strsnewin.emit(out_line)
                                self.paly_sound()
                                #time.sleep(0.01)
                            QtWidgets.QApplication.processEvents()
                        time.sleep(15)
                        tmp_trans = in_trans
                    elif self.flag == 0:
                        #self.strsin.emit("stop thread")
                        time.sleep(10)
                        break
                except Exception as e:
                    print(e)
                    time.sleep(10)
        except Exception as e:
            print(e)


    def stop(self):
        self.flag = 0


if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui_dialog = Ui_Dialog()
    ui_dialog.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())



