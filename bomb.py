from PyQt5 import QtCore, QtGui, QtWidgets
from tkinter import Tk
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementNotVisibleException,
)

# pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QMessageBox


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        root = Tk()
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowTitle("What A Bomb :: WhatsApp Bomber")
        warn = """
        <b>Legal disclaimer</b>: Usage of "What a Bomb" is only for educational and entertainment purpose. Developers assume no liability and are not responsible for any misuse or damage caused by this program
        """
        MainWindow.resize(674, 379)
        width = root.winfo_screenwidth()
        height = root.winfo_screenheight()
        MainWindow.move(width // 4, height // 5)
        QMessageBox.warning(MainWindow, "Disclaimer", warn)
        MainWindow.setMinimumSize(QtCore.QSize(674, 379))
        MainWindow.setMaximumSize(QtCore.QSize(674, 379))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 40, 151, 30))
        self.label.setObjectName("label")
        self.cgname = QtWidgets.QLineEdit(self.centralwidget)
        self.cgname.setGeometry(QtCore.QRect(190, 40, 451, 29))
        self.cgname.setObjectName("cgname")
        self.msgs = QtWidgets.QLineEdit(self.centralwidget)
        self.msgs.setGeometry(QtCore.QRect(190, 80, 451, 29))
        self.msgs.setObjectName("msgs")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(30, 80, 151, 30))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(30, 120, 151, 30))
        self.label_3.setObjectName("label_3")
        self.bombSend = QtWidgets.QPushButton(self.centralwidget)
        self.bombSend.setGeometry(QtCore.QRect(540, 320, 95, 31))
        self.bombSend.setObjectName("bombSend")
        self.msg = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.msg.setGeometry(QtCore.QRect(190, 130, 451, 161))
        self.msg.setObjectName("msg")
        self.about = QtWidgets.QPushButton(self.centralwidget)
        self.about.setGeometry(QtCore.QRect(420, 320, 95, 31))
        self.about.setObjectName("about")
        MainWindow.setCentralWidget(self.centralwidget)
        self.about.clicked.connect(self.MYABOUT)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.obj = MainWindow
        self.bombSend.clicked.connect(self.bomb)
        pass

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.label.setText(_translate("MainWindow", "Contact / Group Name"))
        self.cgname.setPlaceholderText(
            _translate("MainWindow",
                       "casesensitive field and enter full name"))
        self.msgs.setPlaceholderText(_translate("MainWindow", "only numbers"))
        self.label_2.setText(_translate("MainWindow", "Number of messages"))
        self.label_3.setText(_translate("MainWindow", "Message Body"))
        self.bombSend.setText(_translate("MainWindow", "Bomb"))
        self.about.setText(_translate("MainWindow", "About"))
        pass

    def bomb(self):
        global search
        search = None
        box = QtWidgets.QMessageBox(self.obj)
        target = self.cgname.text()
        number = self.msgs.text()
        mesage = self.msg.toPlainText()
        if target == "":
            box.setStandardButtons(QMessageBox.Ok)
            box.setIcon(QMessageBox.Warning)
            box.setWindowTitle("Wait!!!")
            box.setText("It seems you forgot to enter target")
            box.show()
            self.cgname.setFocus()
            return None

        try:
            number = int(number)
        except:
            QMessageBox.critical(self.obj, "Error!!!",
                                 "Enter any number starting from <b>1</b>")
            self.msgs.setFocus()
            return None

        if mesage == "":
            QtWidgets.QMessageBox.information(
                None, "No Message",
                "Since there is no input message. Taking \"Hello, {name}\"")
            mesage = "Hello, " + target

        QtWidgets.QMessageBox.information(
            self.obj,
            "The last thing",
            "<h2>We are opening your browser now, just scan QR code and rest we will do</h2>",
        )
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get("https://web.whatsapp.com")
        while True:
            try:
                search = driver.find_element_by_xpath(
                    "/html/body/div[1]/div/div/div[3]/div/div[1]/div/label/div/div[2]"
                )
                break
            except Exception:
                pass
        search.click()
        search.send_keys(target)

        tries = 15

        while tries:
            try:
                driver.find_element_by_xpath(
                    '//span[@title = "{}"]'.format(target)).click()
                break
                tries -= 1

            except:
                pass
        else:
            QtWidgets.QMessageBox.critical(
                None, "No Account Found",
                "No user found with display name '%s'" % target)
            return None

        msg_box = driver.find_element_by_xpath(
            "/html[1]/body[1]/div[1]/div[1]/div[1]/div[4]/div[1]/footer[1]/div[1]/div[2]/div[1]/div[2]"
        )

        for i in range(number):
            msg_box.send_keys(mesage.replace("\n", Keys.SHIFT + Keys.ENTER))
            msg_box.send_keys(Keys.ENTER)
            print("sent {} messages".format(i + 1), end="\r")
        driver.quit()
        QMessageBox.information(
            self.obj,
            "Sent",
            "<span style='font-size:20px'>Target successfully bombed</span>",
        )
        pass

    def MYABOUT(self):
        box = QtWidgets.QMessageBox(self.obj)
        msg = """
        This program is coded by <b>Gurkirat Singh (T3r@bYt3)</b>. <br><br><br>
        Thanks to : <b>Sameer Bhatt</b> (for giving me the implementation example)
        """
        box.setStandardButtons(QMessageBox.Ok)
        box.setIcon(QMessageBox.Information)
        box.setWindowTitle("About")
        box.setText(msg)
        box.show()
        pass

    pass


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
