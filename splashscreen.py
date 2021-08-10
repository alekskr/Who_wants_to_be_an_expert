# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SplashScreenJxOXFa.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_SplashScreen(object):
    def setupUi(self, SplashScreen):
        if not SplashScreen.objectName():
            SplashScreen.setObjectName(u"SplashScreen")
        SplashScreen.resize(680, 400)
        self.centralwidget = QWidget(SplashScreen)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.dropShadowFrame = QFrame(self.centralwidget)
        self.dropShadowFrame.setObjectName(u"dropShadowFrame")
        self.dropShadowFrame.setStyleSheet(u"QFrame {\n"
"	background-color: #282a36;\n"
"	color: #8be9fd;\n"
"	border-radius: 10px;\n"
"}")
        self.dropShadowFrame.setFrameShape(QFrame.StyledPanel)
        self.dropShadowFrame.setFrameShadow(QFrame.Raised)
        self.label_title = QLabel(self.dropShadowFrame)
        self.label_title.setObjectName(u"label_title")
        self.label_title.setGeometry(QRect(0, 30, 661, 111))
        font = QFont()
        font.setFamily(u"Segoe UI")
        font.setPointSize(20)
        self.label_title.setFont(font)
        self.label_title.setStyleSheet(u"\n"
"color: #8be9fd;")
        self.label_title.setAlignment(Qt.AlignCenter)
        self.label_description = QLabel(self.dropShadowFrame)
        self.label_description.setObjectName(u"label_description")
        self.label_description.setGeometry(QRect(0, 210, 661, 41))
        font1 = QFont()
        font1.setFamily(u"Segoe UI")
        font1.setPointSize(14)
        self.label_description.setFont(font1)
        self.label_description.setStyleSheet(u"/*color: rgb(79, 179, 255)*/\n"
"color: #8be9fd")
        self.label_description.setAlignment(Qt.AlignCenter)
        self.progressBar = QProgressBar(self.dropShadowFrame)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(80, 260, 501, 23))
        self.progressBar.setStyleSheet(u"QProgressBar {\n"
"	color: rgb(66, 66, 66);\n"
"	\n"
"	/*background-color: rgb(79, 179, 255);*/\n"
"	\n"
"	background-color: rgb(66, 66, 66);\n"
"	border-style: none;\n"
"	border-radius: 10px;\n"
"	text-align: center;\n"
"}\n"
"QProgressBar::chunk{\n"
"	border-radius: 10px;\n"
"	\n"
"	/*background-color: rgb(254, 122, 7);*/\n"
"	/*background-color: qlineargradient(spread:pad, x1:0, y1:0.489, x2:1, y2:0.528, stop:0 rgba(255, 126, 195, 255), stop:1 rgba(170, 0, 255, 255));*/\n"
"	background-color: qlineargradient(spread:pad, x1:0, y1:0.489, x2:1, y2:0.528, stop:0 #50fa7b, stop:1 rgba(127, 253, 49));\n"
"}\n"
"")
        self.progressBar.setValue(0)
        self.label_credits = QLabel(self.dropShadowFrame)
        self.label_credits.setObjectName(u"label_credits")
        self.label_credits.setGeometry(QRect(50, 330, 571, 31))
        font2 = QFont()
        font2.setFamily(u"Segoe UI")
        font2.setPointSize(10)
        self.label_credits.setFont(font2)
        self.label_credits.setStyleSheet(u"/*color: rgb(79, 179, 255)*/\n"
"color: #8be9fd")
        self.label_credits.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.verticalLayout.addWidget(self.dropShadowFrame)

        SplashScreen.setCentralWidget(self.centralwidget)

        self.retranslateUi(SplashScreen)

        QMetaObject.connectSlotsByName(SplashScreen)
    # setupUi

    def retranslateUi(self, SplashScreen):
        SplashScreen.setWindowTitle(QCoreApplication.translate("SplashScreen", u"MainWindow", None))
        self.label_title.setText(QCoreApplication.translate("SplashScreen", u"<html><head/><body><p align=\"center\">WELCOME TO</p><p align=\"center\"><span style=\" font-family:'JetBrains Mono','monospace'; font-weight:600; color:#50fa7b;\">who wants to be an EXPERT</span></p></body></html>", None))
        self.label_description.setText(QCoreApplication.translate("SplashScreen", u"<strong>APP </strong>DESCRIPTION", None))
        self.label_credits.setText(QCoreApplication.translate("SplashScreen", u"<strong>Created</strong>: Alex K", None))
    # retranslateUi

