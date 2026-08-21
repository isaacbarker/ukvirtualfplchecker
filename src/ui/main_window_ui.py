# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.11.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QMainWindow, QPushButton, QScrollArea, QSizePolicy,
    QStatusBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(251, 585)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_4 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.flight_details_layout = QHBoxLayout()
        self.flight_details_layout.setObjectName(u"flight_details_layout")
        self.callsign_label = QLabel(self.centralwidget)
        self.callsign_label.setObjectName(u"callsign_label")
        self.callsign_label.setStyleSheet(u"")

        self.flight_details_layout.addWidget(self.callsign_label)


        self.verticalLayout_4.addLayout(self.flight_details_layout)

        self.line_2 = QFrame(self.centralwidget)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_4.addWidget(self.line_2)

        self.dep_label = QLabel(self.centralwidget)
        self.dep_label.setObjectName(u"dep_label")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dep_label.sizePolicy().hasHeightForWidth())
        self.dep_label.setSizePolicy(sizePolicy)
        self.dep_label.setWordWrap(True)

        self.verticalLayout_4.addWidget(self.dep_label)

        self.arr_dep_details_layout = QHBoxLayout()
        self.arr_dep_details_layout.setObjectName(u"arr_dep_details_layout")
        self.arr_label = QLabel(self.centralwidget)
        self.arr_label.setObjectName(u"arr_label")
        sizePolicy.setHeightForWidth(self.arr_label.sizePolicy().hasHeightForWidth())
        self.arr_label.setSizePolicy(sizePolicy)
        self.arr_label.setWordWrap(True)

        self.arr_dep_details_layout.addWidget(self.arr_label)


        self.verticalLayout_4.addLayout(self.arr_dep_details_layout)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.aircraft_name_label = QLabel(self.centralwidget)
        self.aircraft_name_label.setObjectName(u"aircraft_name_label")

        self.verticalLayout.addWidget(self.aircraft_name_label)

        self.wake_cat_label = QLabel(self.centralwidget)
        self.wake_cat_label.setObjectName(u"wake_cat_label")

        self.verticalLayout.addWidget(self.wake_cat_label)

        self.line_3 = QFrame(self.centralwidget)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line_3)


        self.verticalLayout_4.addLayout(self.verticalLayout)

        self.scroll_area = QScrollArea(self.centralwidget)
        self.scroll_area.setObjectName(u"scroll_area")
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll_area.setFrameShadow(QFrame.Shadow.Plain)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 233, 336))
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.check_results = QLabel(self.scrollAreaWidgetContents)
        self.check_results.setObjectName(u"check_results")

        self.verticalLayout_2.addWidget(self.check_results)

        self.scroll_area.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_4.addWidget(self.scroll_area)

        self.line_4 = QFrame(self.centralwidget)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.Shape.HLine)
        self.line_4.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_4.addWidget(self.line_4)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.connection_label = QLabel(self.centralwidget)
        self.connection_label.setObjectName(u"connection_label")

        self.horizontalLayout.addWidget(self.connection_label)

        self.reconnect_btn = QPushButton(self.centralwidget)
        self.reconnect_btn.setObjectName(u"reconnect_btn")

        self.horizontalLayout.addWidget(self.reconnect_btn)


        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.version_label = QLabel(self.centralwidget)
        self.version_label.setObjectName(u"version_label")

        self.verticalLayout_3.addWidget(self.version_label)


        self.verticalLayout_4.addLayout(self.verticalLayout_3)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Virtual UK ATC Assistant", None))
        self.callsign_label.setText("")
        self.dep_label.setText("")
        self.arr_label.setText("")
        self.aircraft_name_label.setText(QCoreApplication.translate("MainWindow", u"AIRCRAFT NAME", None))
        self.wake_cat_label.setText(QCoreApplication.translate("MainWindow", u"CAA WAKE CAT", None))
        self.check_results.setText("")
        self.connection_label.setText(QCoreApplication.translate("MainWindow", u"CONNECTION", None))
        self.reconnect_btn.setText(QCoreApplication.translate("MainWindow", u"Re-connect", None))
        self.version_label.setText(QCoreApplication.translate("MainWindow", u"VERSION", None))
    # retranslateUi

