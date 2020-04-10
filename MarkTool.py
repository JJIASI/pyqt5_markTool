# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MarkTool.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import os
import cv2


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(928, 711)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(40, 30, 121, 41))
        self.pushButton.setObjectName("pushButton")

        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(30, 140, 256, 221))
        self.listWidget.setObjectName("listWidget")

        self.listWidget_2 = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget_2.setGeometry(QtCore.QRect(30, 420, 256, 221))
        self.listWidget_2.setObjectName("listWidget_2")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(40, 110, 161, 21))
        self.label.setObjectName("label")

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(40, 390, 161, 21))
        self.label_2.setObjectName("label_2")

        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(330, 70, 521, 391))
        self.label_3.setObjectName("label_3")

        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(310, 566, 381, 71))
        self.textEdit.setObjectName("textEdit")

        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(320, 540, 58, 15))
        self.label_4.setObjectName("label_4")

        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(720, 600, 101, 41))
        self.pushButton_2.setObjectName("pushButton_2")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 928, 25))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.sel_dir = ""
        self.initUI()
    def retranslateUi(self, MainWindow):
        """名稱設定
        """
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Import"))
        self.label.setText(_translate("MainWindow", "Unlabeled Image List"))
        self.label_2.setText(_translate("MainWindow", "labeled Image List"))
        self.label_3.setText(_translate("MainWindow", "Image"))
        self.label_4.setText(_translate("MainWindow", "value"))
        self.pushButton_2.setText(_translate("MainWindow", "OK"))

    def initUI(self):
        """初始化按鈕功能
        """
        self.pushButton.clicked.connect(self.clickedImport)
        self.listWidget.clicked.connect(self.clickedList)
        self.pushButton_2.clicked.connect(self.clickedOK)
        self.listWidget_2.clicked.connect(self.clickedList_2)

    def clickedImport(self):
        """Import 點擊事件
        """
        path = QtWidgets.QFileDialog.getExistingDirectory()
        if path != "":
            self.sel_dir = path
            self.getFileNmae()

    def getFileNmae(self):
        """資料夾內檔案名稱填入list
        """
        dir_list = os.listdir(self.sel_dir)
        labeled_list, unlabeled_list = self.splitFile(dir_list)

        # init list
        self.listWidget_2.clear()
        self.listWidget.clear()

        # fillin list
        self.listWidget_2.addItems(labeled_list)
        self.listWidget.addItems(unlabeled_list)


    def splitFile(self, arr):
        """區分是否標註
        """
        labeled_list = []
        unlabeled_list = []
        for filename in arr:
            if "_" in filename:
                labeled_list.append(filename)
            else:
                unlabeled_list.append(filename)

        return labeled_list, unlabeled_list

    def clickedList(self):
        """點擊List事件
        """
        self.filename = self.listWidget.currentItem().text()
        self.textEdit.clear()
        # 畫圖
        img_tmp = cv2.imread(self.sel_dir+'/'+self.filename)
        self.img = cv2.resize(img_tmp, (500,250), cv2.INTER_CUBIC)
        self.refreshShow()

    def clickedList_2(self):
        """點擊List2事件
        """
        self.filename = self.listWidget_2.currentItem().text()
        self.textEdit.clear()
        # 畫圖
        img_tmp = cv2.imread(self.sel_dir+'/'+self.filename)
        self.img = cv2.resize(img_tmp, (500,250), cv2.INTER_CUBIC)
        self.refreshShow()

        # 寫入textbox
        self.textEdit.setText(self.filename.split("_")[0])

    def refreshShow(self):
        height, width, _ = self.img.shape
        bytesPerLine = 3 * width
        self.qImg = QtGui.QImage(self.img.data, width, height, bytesPerLine,
                           QtGui.QImage.Format_RGB888).rgbSwapped()

        self.label_3.setPixmap(QtGui.QPixmap.fromImage(self.qImg))

    def clickedOK(self):
        text = self.textEdit.toPlainText()
        if "_" in self.filename:
            raw_filename = self.filename.split("_")[1]
            os.rename(f'{self.sel_dir}/{self.filename}', f'{self.sel_dir}/{text}_{raw_filename}')
            self.getFileNmae()
            
        else:
            os.rename(f'{self.sel_dir}/{self.filename}', f'{self.sel_dir}/{text}_{self.filename}')
            self.getFileNmae()
        self.label_3.setText("請點選圖片")
        self.textEdit.clear()

if __name__ == '__main__':  
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()

    ui.setupUi(MainWindow) 
    MainWindow.show()
    sys.exit(app.exec_())