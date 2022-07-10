
from load import *


# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'interfaceolpFfD.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *



import resources_rc
import resources_rc

class estatistica(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(813, 476)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"@font-face {\n"
"    font-family: NovaFlat;\n"
"    src: url(:/fonts/Nova_Flat/NovaFlat-Regular.ttf) format(\"truetype\");\n"
"}\n"
"*{\n"
"color: #fff;\n"
"font-family: NovaFlat;\n"
"font-size: 12px;\n"
"border: nine;\n"
"background: none;\n"
"}\n"
"#centralwidget{\n"
"background-color: rgb(33, 43, 51);\n"
"}\n"
"#left_menu_widget, #percentage_bar_chart, #nested_donuts,\n"
"#line_charts, #bar_charts, #temperature_bar_chart\n"
"{\n"
"background-color: rgba(61, 80, 95, 100)\n"
"}\n"
"#header_frame, #frame_3, #frame_5{\n"
"background-color: rgb(61, 80, 95);\n"
"}\n"
"#frame_4 QPushButton{\n"
"padding: 10px;\n"
"border-radius: 5px;\n"
"background-color: rgba(33, 43, 51, 100);\n"
"}\n"
"#header_nav QPushButton{\n"
"	background-color: rgb(61, 80, 95);\n"
"	border-radius: 15px;\n"
"	border: 3px solid rgb(120, 157, 186);\n"
"}\n"
"#header_nav QPushButton:hover{\n"
"	background-color: rgb(120, 157, 186);\n"
"}\n"
"")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.left_menu_widget.setObjectName(u"left_menu_widget")
        self.verticalLayout = QVBoxLayout(self.left_menu_widget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame_3 = QFrame(self.left_menu_widget)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(6, 0, 0, 0)
        self.label_14 = QLabel(self.frame_3)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setMinimumSize(QSize(40, 40))
        self.label_14.setMaximumSize(QSize(40, 40))
        self.label_14.setPixmap(QPixmap(u":/icons/icons/pie-chart.svg"))
        self.label_14.setScaledContents(True)

        self.horizontalLayout_2.addWidget(self.label_14)

        self.label = QLabel(self.frame_3)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setFamily(u"NovaFlat")
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)

        self.horizontalLayout_2.addWidget(self.label)


        self.verticalLayout.addWidget(self.frame_3, 0, Qt.AlignTop)

        self.frame_4 = QFrame(self.left_menu_widget)
        self.frame_4.setObjectName(u"frame_4")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_4.sizePolicy().hasHeightForWidth())
        self.frame_4.setSizePolicy(sizePolicy)
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_4)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.percentage_bar_btn = QPushButton(self.frame_4)
        self.percentage_bar_btn.setObjectName(u"percentage_bar_btn")
        icon = QIcon()
        icon.addFile(u":/icons/icons/bar-chart-2.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.percentage_bar_btn.setIcon(icon)

        self.verticalLayout_2.addWidget(self.percentage_bar_btn)

        self.temperature_bar_btn = QPushButton(self.frame_4)
        self.temperature_bar_btn.setObjectName(u"temperature_bar_btn")
        icon1 = QIcon()
        icon1.addFile(u":/icons/icons/thermometer.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.temperature_bar_btn.setIcon(icon1)

        self.verticalLayout_2.addWidget(self.temperature_bar_btn)

        self.nested_donut_btn = QPushButton(self.frame_4)
        self.nested_donut_btn.setObjectName(u"nested_donut_btn")
        icon2 = QIcon()
        icon2.addFile(u":/icons/icons/target.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.nested_donut_btn.setIcon(icon2)

        self.verticalLayout_2.addWidget(self.nested_donut_btn)

        self.line_chart_btn = QPushButton(self.frame_4)
        self.line_chart_btn.setObjectName(u"line_chart_btn")
        icon3 = QIcon()
        icon3.addFile(u":/icons/icons/git-merge.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.line_chart_btn.setIcon(icon3)

        self.verticalLayout_2.addWidget(self.line_chart_btn)

        self.bar_charts_btn = QPushButton(self.frame_4)
        self.bar_charts_btn.setObjectName(u"bar_charts_btn")
        icon4 = QIcon()
        icon4.addFile(u":/icons/icons/bar-chart.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.bar_charts_btn.setIcon(icon4)

        self.verticalLayout_2.addWidget(self.bar_charts_btn)


        self.verticalLayout.addWidget(self.frame_4)

        self.frame_5 = QFrame(self.left_menu_widget)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.frame_5)
        self.horizontalLayout_7.setSpacing(6)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(6, 0, 0, 0)
        self.label_15 = QLabel(self.frame_5)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setMinimumSize(QSize(40, 40))
        self.label_15.setMaximumSize(QSize(40, 40))
        self.label_15.setPixmap(QPixmap(u":/icons/icons/smile.svg"))
        self.label_15.setScaledContents(True)

        self.horizontalLayout_7.addWidget(self.label_15)

        self.label_2 = QLabel(self.frame_5)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)

        self.horizontalLayout_7.addWidget(self.label_2)


        self.verticalLayout.addWidget(self.frame_5, 0, Qt.AlignTop)

        self.frame_6 = QFrame(self.left_menu_widget)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.gridLayout_6 = QGridLayout(self.frame_6)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.label_5 = QLabel(self.frame_6)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_6.addWidget(self.label_5, 1, 1, 1, 1)

        self.label_4 = QLabel(self.frame_6)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_6.addWidget(self.label_4, 2, 1, 1, 1)

        self.label_3 = QLabel(self.frame_6)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_6.addWidget(self.label_3, 0, 1, 1, 1)

        self.label_16 = QLabel(self.frame_6)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setMinimumSize(QSize(30, 30))
        self.label_16.setMaximumSize(QSize(30, 30))
        self.label_16.setPixmap(QPixmap(u":/images/images/icons8-patreon-50.png"))
        self.label_16.setScaledContents(True)

        self.gridLayout_6.addWidget(self.label_16, 0, 0, 1, 1)

        self.label_17 = QLabel(self.frame_6)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setMinimumSize(QSize(30, 30))
        self.label_17.setMaximumSize(QSize(30, 30))
        self.label_17.setPixmap(QPixmap(u":/images/images/icons8-youtube-studio-50.png"))
        self.label_17.setScaledContents(True)

        self.gridLayout_6.addWidget(self.label_17, 1, 0, 1, 1)

        self.label_18 = QLabel(self.frame_6)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setMinimumSize(QSize(30, 30))
        self.label_18.setMaximumSize(QSize(30, 30))
        self.label_18.setPixmap(QPixmap(u":/images/images/icons8-paypal-50.png"))
        self.label_18.setScaledContents(True)

        self.gridLayout_6.addWidget(self.label_18, 2, 0, 1, 1)


        self.verticalLayout.addWidget(self.frame_6)


        self.horizontalLayout.addWidget(self.left_menu_widget)

        self.frame_2 = QFrame(self.centralwidget)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frame_2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(6, 0, 0, 0)
        self.header_frame = QFrame(self.frame_2)
        self.header_frame.setObjectName(u"header_frame")
        self.header_frame.setMaximumSize(QSize(16777215, 50))
        self.header_frame.setFrameShape(QFrame.StyledPanel)
        self.header_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.header_frame)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.frame_10 = QFrame(self.header_frame)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setFrameShape(QFrame.StyledPanel)
        self.frame_10.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame_10)
        self.horizontalLayout_4.setSpacing(2)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.open_close_side_bar_btn = QPushButton(self.frame_10)
        self.open_close_side_bar_btn.setObjectName(u"open_close_side_bar_btn")
        icon5 = QIcon()
        icon5.addFile(u":/icons/icons/align-center.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.open_close_side_bar_btn.setIcon(icon5)
        self.open_close_side_bar_btn.setIconSize(QSize(30, 30))

        self.horizontalLayout_4.addWidget(self.open_close_side_bar_btn)

        self.label_6 = QLabel(self.frame_10)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_4.addWidget(self.label_6)


        self.horizontalLayout_3.addWidget(self.frame_10, 0, Qt.AlignLeft)

        self.frame_11 = QFrame(self.header_frame)
        self.frame_11.setObjectName(u"frame_11")
        self.frame_11.setFrameShape(QFrame.StyledPanel)
        self.frame_11.setFrameShadow(QFrame.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.frame_11)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.label_7 = QLabel(self.frame_11)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font)
        self.label_7.setAlignment(Qt.AlignCenter)

        self.verticalLayout_5.addWidget(self.label_7)


        self.horizontalLayout_3.addWidget(self.frame_11)

        self.header_nav = QFrame(self.header_frame)
        self.header_nav.setObjectName(u"header_nav")
        self.header_nav.setFrameShape(QFrame.StyledPanel)
        self.header_nav.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.header_nav)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.minimize_window_button = QPushButton(self.header_nav)
        self.minimize_window_button.setObjectName(u"minimize_window_button")
        self.minimize_window_button.setMinimumSize(QSize(30, 30))
        self.minimize_window_button.setMaximumSize(QSize(30, 30))
        icon6 = QIcon()
        icon6.addFile(u":/icons/icons/minus.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.minimize_window_button.setIcon(icon6)

        self.horizontalLayout_5.addWidget(self.minimize_window_button)

        self.restore_window_button = QPushButton(self.header_nav)
        self.restore_window_button.setObjectName(u"restore_window_button")
        self.restore_window_button.setMinimumSize(QSize(30, 30))
        self.restore_window_button.setMaximumSize(QSize(30, 30))
        icon7 = QIcon()
        icon7.addFile(u":/icons/icons/maximize-2.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.restore_window_button.setIcon(icon7)

        self.horizontalLayout_5.addWidget(self.restore_window_button)

        self.close_window_button = QPushButton(self.header_nav)
        self.close_window_button.setObjectName(u"close_window_button")
        self.close_window_button.setMinimumSize(QSize(30, 30))
        self.close_window_button.setMaximumSize(QSize(30, 30))
        icon8 = QIcon()
        icon8.addFile(u":/icons/icons/x.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.close_window_button.setIcon(icon8)

        self.horizontalLayout_5.addWidget(self.close_window_button)


        self.horizontalLayout_3.addWidget(self.header_nav, 0, Qt.AlignRight)


        self.verticalLayout_4.addWidget(self.header_frame, 0, Qt.AlignTop)

        self.frame_8 = QFrame(self.frame_2)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setFrameShape(QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QFrame.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.frame_8)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.stackedWidget = QStackedWidget(self.frame_8)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setFont(font)
        self.percentage_bar_chart = QWidget()
        self.percentage_bar_chart.setObjectName(u"percentage_bar_chart")
        self.verticalLayout_8 = QVBoxLayout(self.percentage_bar_chart)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.frame_15 = QFrame(self.percentage_bar_chart)
        self.frame_15.setObjectName(u"frame_15")
        self.frame_15.setFrameShape(QFrame.StyledPanel)
        self.frame_15.setFrameShadow(QFrame.Raised)
        self.verticalLayout_9 = QVBoxLayout(self.frame_15)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.label_9 = QLabel(self.frame_15)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setFont(font)
        self.label_9.setAlignment(Qt.AlignCenter)

        self.verticalLayout_9.addWidget(self.label_9, 0, Qt.AlignTop)


        self.verticalLayout_8.addWidget(self.frame_15, 0, Qt.AlignTop)

        self.frame_16 = QFrame(self.percentage_bar_chart)
        self.frame_16.setObjectName(u"frame_16")
        sizePolicy.setHeightForWidth(self.frame_16.sizePolicy().hasHeightForWidth())
        self.frame_16.setSizePolicy(sizePolicy)
        self.frame_16.setFrameShape(QFrame.StyledPanel)
        self.frame_16.setFrameShadow(QFrame.Raised)
        self.percentage_bar_chart_cont = QGridLayout(self.frame_16)
        self.percentage_bar_chart_cont.setObjectName(u"percentage_bar_chart_cont")

        self.verticalLayout_8.addWidget(self.frame_16)

        self.stackedWidget.addWidget(self.percentage_bar_chart)
        self.temperature_bar_chart = QWidget()
        self.temperature_bar_chart.setObjectName(u"temperature_bar_chart")
        self.verticalLayout_11 = QVBoxLayout(self.temperature_bar_chart)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.frame_17 = QFrame(self.temperature_bar_chart)
        self.frame_17.setObjectName(u"frame_17")
        self.frame_17.setFont(font)
        self.frame_17.setFrameShape(QFrame.StyledPanel)
        self.frame_17.setFrameShadow(QFrame.Raised)
        self.verticalLayout_10 = QVBoxLayout(self.frame_17)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.label_10 = QLabel(self.frame_17)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setFont(font)
        self.label_10.setAlignment(Qt.AlignCenter)

        self.verticalLayout_10.addWidget(self.label_10, 0, Qt.AlignTop)


        self.verticalLayout_11.addWidget(self.frame_17)

        self.frame_18 = QFrame(self.temperature_bar_chart)
        self.frame_18.setObjectName(u"frame_18")
        sizePolicy.setHeightForWidth(self.frame_18.sizePolicy().hasHeightForWidth())
        self.frame_18.setSizePolicy(sizePolicy)
        self.frame_18.setFrameShape(QFrame.StyledPanel)
        self.frame_18.setFrameShadow(QFrame.Raised)
        self.temperature_bar_chart_cont = QGridLayout(self.frame_18)
        self.temperature_bar_chart_cont.setObjectName(u"temperature_bar_chart_cont")

        self.verticalLayout_11.addWidget(self.frame_18)

        self.stackedWidget.addWidget(self.temperature_bar_chart)
        self.nested_donuts = QWidget()
        self.nested_donuts.setObjectName(u"nested_donuts")
        self.verticalLayout_13 = QVBoxLayout(self.nested_donuts)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.frame_19 = QFrame(self.nested_donuts)
        self.frame_19.setObjectName(u"frame_19")
        self.frame_19.setFont(font)
        self.frame_19.setFrameShape(QFrame.StyledPanel)
        self.frame_19.setFrameShadow(QFrame.Raised)
        self.verticalLayout_12 = QVBoxLayout(self.frame_19)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.label_11 = QLabel(self.frame_19)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setFont(font)
        self.label_11.setAlignment(Qt.AlignCenter)

        self.verticalLayout_12.addWidget(self.label_11, 0, Qt.AlignTop)


        self.verticalLayout_13.addWidget(self.frame_19)

        self.frame_20 = QFrame(self.nested_donuts)
        self.frame_20.setObjectName(u"frame_20")
        sizePolicy.setHeightForWidth(self.frame_20.sizePolicy().hasHeightForWidth())
        self.frame_20.setSizePolicy(sizePolicy)
        self.frame_20.setFrameShape(QFrame.StyledPanel)
        self.frame_20.setFrameShadow(QFrame.Raised)
        self.nested_donut_chart_cont = QGridLayout(self.frame_20)
        self.nested_donut_chart_cont.setObjectName(u"nested_donut_chart_cont")

        self.verticalLayout_13.addWidget(self.frame_20)

        self.stackedWidget.addWidget(self.nested_donuts)
        self.line_charts = QWidget()
        self.line_charts.setObjectName(u"line_charts")
        self.verticalLayout_15 = QVBoxLayout(self.line_charts)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.frame_21 = QFrame(self.line_charts)
        self.frame_21.setObjectName(u"frame_21")
        self.frame_21.setFrameShape(QFrame.StyledPanel)
        self.frame_21.setFrameShadow(QFrame.Raised)
        self.verticalLayout_14 = QVBoxLayout(self.frame_21)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.label_12 = QLabel(self.frame_21)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setFont(font)
        self.label_12.setAlignment(Qt.AlignCenter)

        self.verticalLayout_14.addWidget(self.label_12, 0, Qt.AlignTop)


        self.verticalLayout_15.addWidget(self.frame_21)

        self.frame_22 = QFrame(self.line_charts)
        self.frame_22.setObjectName(u"frame_22")
        sizePolicy.setHeightForWidth(self.frame_22.sizePolicy().hasHeightForWidth())
        self.frame_22.setSizePolicy(sizePolicy)
        self.frame_22.setFrameShape(QFrame.StyledPanel)
        self.frame_22.setFrameShadow(QFrame.Raised)
        self.line_charts_cont = QGridLayout(self.frame_22)
        self.line_charts_cont.setObjectName(u"line_charts_cont")

        self.verticalLayout_15.addWidget(self.frame_22)

        self.stackedWidget.addWidget(self.line_charts)
        self.bar_charts = QWidget()
        self.bar_charts.setObjectName(u"bar_charts")
        self.verticalLayout_17 = QVBoxLayout(self.bar_charts)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.frame_23 = QFrame(self.bar_charts)
        self.frame_23.setObjectName(u"frame_23")
        self.frame_23.setFrameShape(QFrame.StyledPanel)
        self.frame_23.setFrameShadow(QFrame.Raised)
        self.verticalLayout_16 = QVBoxLayout(self.frame_23)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.label_13 = QLabel(self.frame_23)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setFont(font)
        self.label_13.setAlignment(Qt.AlignCenter)

        self.verticalLayout_16.addWidget(self.label_13, 0, Qt.AlignTop)


        self.verticalLayout_17.addWidget(self.frame_23)

        self.frame_24 = QFrame(self.bar_charts)
        self.frame_24.setObjectName(u"frame_24")
        sizePolicy.setHeightForWidth(self.frame_24.sizePolicy().hasHeightForWidth())
        self.frame_24.setSizePolicy(sizePolicy)
        self.frame_24.setFrameShape(QFrame.StyledPanel)
        self.frame_24.setFrameShadow(QFrame.Raised)
        self.bar_charts_cont = QGridLayout(self.frame_24)
        self.bar_charts_cont.setObjectName(u"bar_charts_cont")

        self.verticalLayout_17.addWidget(self.frame_24)

        self.stackedWidget.addWidget(self.bar_charts)

        self.verticalLayout_7.addWidget(self.stackedWidget)


        self.verticalLayout_4.addWidget(self.frame_8)

        self.footer_frame = QFrame(self.frame_2)
        self.footer_frame.setObjectName(u"footer_frame")
        self.footer_frame.setFrameShape(QFrame.StyledPanel)
        self.footer_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.footer_frame)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.frame_13 = QFrame(self.footer_frame)
        self.frame_13.setObjectName(u"frame_13")
        self.frame_13.setFrameShape(QFrame.StyledPanel)
        self.frame_13.setFrameShadow(QFrame.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.frame_13)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.label_8 = QLabel(self.frame_13)
        self.label_8.setObjectName(u"label_8")

        self.verticalLayout_6.addWidget(self.label_8)


        self.horizontalLayout_6.addWidget(self.frame_13)

        self.frame_14 = QFrame(self.footer_frame)
        self.frame_14.setObjectName(u"frame_14")
        self.frame_14.setFrameShape(QFrame.StyledPanel)
        self.frame_14.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_14)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.size_grip = QFrame(self.frame_14)
        self.size_grip.setObjectName(u"size_grip")
        self.size_grip.setMinimumSize(QSize(10, 10))
        self.size_grip.setMaximumSize(QSize(10, 10))
        self.size_grip.setFrameShape(QFrame.StyledPanel)
        self.size_grip.setFrameShadow(QFrame.Raised)

        self.verticalLayout_3.addWidget(self.size_grip)


        self.horizontalLayout_6.addWidget(self.frame_14, 0, Qt.AlignRight|Qt.AlignBottom)


        self.verticalLayout_4.addWidget(self.footer_frame, 0, Qt.AlignBottom)


        self.horizontalLayout.addWidget(self.frame_2)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label_14.setText("")
        self.label.setText(QCoreApplication.translate("MainWindow", u"QT CHARTS", None))
        self.percentage_bar_btn.setText(QCoreApplication.translate("MainWindow", u"Percentage Bar Chart", None))
        self.temperature_bar_btn.setText(QCoreApplication.translate("MainWindow", u"Temperature Records", None))
        self.nested_donut_btn.setText(QCoreApplication.translate("MainWindow", u"Nested Donuts", None))
        self.line_chart_btn.setText(QCoreApplication.translate("MainWindow", u"Line Charts", None))
        self.bar_charts_btn.setText(QCoreApplication.translate("MainWindow", u"Bar Charts", None))
        self.label_15.setText("")
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"SUPPORT ME", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Subscribe to YouTube", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"PayPal", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Patreon", None))
        self.label_16.setText("")
        self.label_17.setText("")
        self.label_18.setText("")
        self.open_close_side_bar_btn.setText("")
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"MENU", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"DASHBOARD", None))
        self.minimize_window_button.setText("")
        self.restore_window_button.setText("")
        self.close_window_button.setText("")
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Percentage Bar Chart", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Temperature Bar Chart", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Nested Donut Chart", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"Line Charts", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"Bar Chart", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Copyright Spinn Co. V. 1.0.2", None))
    # retranslateUi

