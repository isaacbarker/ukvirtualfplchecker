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
        MainWindow.resize(545, 496)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.flight_details_layout = QHBoxLayout()
        self.flight_details_layout.setObjectName(u"flight_details_layout")
        self.callsign_label = QLabel(self.centralwidget)
        self.callsign_label.setObjectName(u"callsign_label")
        self.callsign_label.setStyleSheet(u"")

        self.flight_details_layout.addWidget(self.callsign_label)


        self.verticalLayout.addLayout(self.flight_details_layout)

        self.arr_dep_details_layout = QHBoxLayout()
        self.arr_dep_details_layout.setObjectName(u"arr_dep_details_layout")
        self.dep_label = QLabel(self.centralwidget)
        self.dep_label.setObjectName(u"dep_label")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dep_label.sizePolicy().hasHeightForWidth())
        self.dep_label.setSizePolicy(sizePolicy)
        self.dep_label.setWordWrap(True)

        self.arr_dep_details_layout.addWidget(self.dep_label)

        self.arr_label = QLabel(self.centralwidget)
        self.arr_label.setObjectName(u"arr_label")
        sizePolicy.setHeightForWidth(self.arr_label.sizePolicy().hasHeightForWidth())
        self.arr_label.setSizePolicy(sizePolicy)
        self.arr_label.setWordWrap(True)

        self.arr_dep_details_layout.addWidget(self.arr_label)


        self.verticalLayout.addLayout(self.arr_dep_details_layout)

        self.scroll_area = QScrollArea(self.centralwidget)
        self.scroll_area.setObjectName(u"scroll_area")
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll_area.setFrameShadow(QFrame.Shadow.Plain)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 527, 351))
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.check_results = QLabel(self.scrollAreaWidgetContents)
        self.check_results.setObjectName(u"check_results")

        self.verticalLayout_2.addWidget(self.check_results)

        self.scroll_area.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scroll_area)

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


        self.verticalLayout.addLayout(self.verticalLayout_3)

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
        self.check_results.setText("")
        self.connection_label.setText(QCoreApplication.translate("MainWindow", u"CONNECTION", None))
        self.reconnect_btn.setText(QCoreApplication.translate("MainWindow", u"Re-connect", None))
        self.version_label.setText(QCoreApplication.translate("MainWindow", u"VERSION", None))
    # retranslateUi

