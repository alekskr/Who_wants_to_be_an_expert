# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import json
import random
import socket
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
import pandas as pd

from PySide2 import QtCore
from PySide2.QtWidgets import QApplication, QLabel, QPushButton, QGridLayout, QMainWindow, QFrame
from PySide2.QtGui import QPixmap, QIcon, QCursor
from PySide2.QtWidgets import QGraphicsDropShadowEffect  # for the splash screen
from PySide2.QtGui import QColor  # for the splash screen

from splashscreen import Ui_SplashScreen


MOVIE = 'https://opentdb.com/api.php?amount=50&category=11&type=multiple'
MUSIC = 'https://opentdb.com/api.php?amount=50&category=12&difficulty=easy&type=multiple'
GEOGRAPHY = 'https://opentdb.com/api.php?amount=50&category=22&type=multiple'  # geography
HISTORY = 'https://opentdb.com/api.php?amount=50&category=23&difficulty=easy&type=multiple'  # history
# VIDEO_GAMES = 'https://opentdb.com/api.php?amount=50&category=15&difficulty=easy&type=multiple'
# CARS = 'https://opentdb.com/api.php?amount=50&category=28&type=multiple'  # cars

parameters = {
    'question': [],
    'answer1': [],
    'answer2': [],
    'answer3': [],
    'answer4': [],
    'correct': [],
    'score': 0,
    'index': []
}


def formatting(fraze):
    formatting_list = [
        ("#039;", "'"),
        ("&'", "'"),
        ("&quot;", '"'),
        ("&ldquo;", '"'),
        (",&rdquo;", '"'),
        ("quot;", ''),
        ("&lt;", "less than SYMBOL"),
        ("&gt;", "greater than SYMBOL"),
        ("&amp;", ""),
        ("&ntilde;&aacute;", "na"),
        ("&eacute;", "e"),
        ("&rsquo;", "'")]
    for q in formatting_list:
        fraze = fraze.replace(q[0], q[1])
    return fraze


def formatting_wrong(wrong):
    formatting_list = [
        ("#039;", "'"),
        ("&'", "'"),
        ("&quot;", '"'),
        ("quot;", ''),
        ("&lt;", "less than SYMBOL"),
        ("&gt;", "greater than SYMBOL"),
        ("&amp;", ""),
        ("&rsquo;", "'"),
        ("&ntilde;&aacute;", "na")]
    for w in formatting_list:
        wrong = [j.replace(w[0], w[1]) for j in wrong]
    return wrong


class MainFrame(QMainWindow):
    """Window with logo and button PLAY"""
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Who want to be an EXPERT')
        self.setMinimumSize(1000, 600)
        self.setStyleSheet('background: #282a36;')

        self.ico = QIcon()
        self.ico.addFile('ico_expert.ico')
        self.setWindowIcon(self.ico)

        self.image = QPixmap('logo_expert1.png')
        self.logo = QLabel()
        self.logo.setPixmap(self.image)
        self.logo.setAlignment(QtCore.Qt.AlignCenter)

        self.message_category = QLabel('Select Category:')
        self.message_category.setMinimumHeight(200)
        self.message_category.setAlignment(QtCore.Qt.AlignCenter)
        self.message_category.setStyleSheet(
            'font-family: Arial;'
            'font-size: 30px;'
            'color: "#8be9fd";'
            'padding: 75px;'
        )

        self.btn_movie = self.create_btn_lvl('MOVIE', 85, 15)
        self.btn_history = self.create_btn_lvl("HISTORY", 15, 85)
        self.btn_music = self.create_btn_lvl("MUSIC", 85, 15)
        self.btn_geography = self.create_btn_lvl("GEOGRAPHY", 15, 85)

        self.btn_movie.setIcon(QIcon('ico_movie.png'))
        self.btn_movie.setIconSize(QtCore.QSize(30, 30))
        self.btn_music.setIcon(QIcon('ico_music.png'))
        self.btn_music.setIconSize(QtCore.QSize(30, 30))
        self.btn_history.setIcon(QIcon('ico_history.png'))
        self.btn_history.setIconSize(QtCore.QSize(30, 30))
        self.btn_geography.setIcon(QIcon('ico_geography.png'))
        self.btn_geography.setIconSize(QtCore.QSize(30, 30))

        self.grid = QGridLayout()
        self.grid.addWidget(self.logo, 0, 0, 1, 2)
        # self.grid.addWidget(self.message_category, 1, 0, 1, 2)
        self.grid.addWidget(self.btn_movie, 2, 0)
        self.grid.addWidget(self.btn_history, 2, 1)
        self.grid.addWidget(self.btn_music, 3, 0)
        self.grid.addWidget(self.btn_geography, 3, 1)

        self.container = QFrame()
        self.container.setLayout(self.grid)
        self.setCentralWidget(self.container)

        self.show()

    def create_btn_lvl(self, lvl_name, l_margin, r_margin):
        print(lvl_name)
        self.btn_lvl = QPushButton(lvl_name)
        self.btn_lvl.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_lvl.setFixedWidth(500)
        self.btn_lvl.setStyleSheet(
            '*{border: 4px solid "#bd93f9";'
            'margin-left: ' + str(l_margin) + 'px;'
            'margin-right: ' + str(r_margin) + 'px;'
            'border-radius: 25px;'
            'font-size: 25px;'
            'padding: 15px 0;'
            # 'margin-top: 20px;'
            'margin-bottom: 30px;'
            'color: "#8be9fd";}'
            '*:hover{background: "#6272a4";}')
        self.btn_lvl.clicked.connect(lambda x: self.click_on_play(lvl_name))
        return self.btn_lvl

    def click_on_play(self, lvl_name):
        """Open window with question and answers by clicking on button PLAY"""
        if lvl_name == 'MOVIE':
            GameFrame(MOVIE, lvl_name)
        elif lvl_name == 'HISTORY':
            GameFrame(HISTORY, lvl_name)
        elif lvl_name == 'MUSIC':
            GameFrame(MUSIC, lvl_name)
        elif lvl_name == 'GEOGRAPHY':
            GameFrame(GEOGRAPHY, lvl_name)
        self.close()


class GameFrame(QMainWindow):
    """Window with question and answers"""
    def __init__(self, lvl_url, lvl_name):
        super().__init__()

        with urlopen(lvl_url) as webpage:
            print(lvl_url)
            data = json.loads(webpage.read().decode())
            self.df = pd.DataFrame(data['results'])
            # print(df['question'])
            # print(df.head())
            # print(df.columns)  # creating a list of all columns
            # print(df.shape)

        self.get_data(self.df)
        self.setWindowTitle(f'Who want to be a {lvl_name} EXPERT')
        self.setStyleSheet('background: #282a36;')
        self.setMinimumSize(1000, 600)

        self.ico = QIcon()
        self.ico.addFile('ico_expert.ico')
        self.setWindowIcon(self.ico)

        self.question = QLabel(parameters['question'][-1])
        self.question.setMinimumHeight(220)
        self.question.setWordWrap(True)
        self.question.setAlignment(QtCore.Qt.AlignCenter)
        self.question.setStyleSheet(
            'font-family: Arial;'
            'font-size: 25px;'
            'color: "#8be9fd";'
            'padding: 75px;')

        self.score = QLabel(str(parameters['score']))
        self.score.setAlignment(QtCore.Qt.AlignCenter)
        self.score.setFixedSize(70, 70)
        self.score.setStyleSheet(
            'font-size: 35px;'
            'color: "#282a36";'
            'background: "#50fa7b";'
            'border: 1px solid "#64A314";'
            'border-radius: 35px;')

        self.your_score = QLabel("Your <strong>score</strong>:")
        self.your_score.setAlignment(QtCore.Qt.AlignRight)
        self.your_score.setStyleSheet(
            "font-family: 'Arial'; "
            "font-size: 35px; "
            "color: '#50fa7b'; "
            "margin: 50px 0px;")

        self.btn1 = self.create_button(parameters['answer1'][-1], 85, 15)
        self.btn2 = self.create_button(parameters['answer2'][-1], 15, 85)
        self.btn3 = self.create_button(parameters['answer3'][-1], 85, 15)
        self.btn4 = self.create_button(parameters['answer4'][-1], 15, 85)
        self.click_on_btn(lvl_name)

        self.image = QPixmap('logo_expert1.png')
        self.logo = QLabel()
        self.logo.setPixmap(self.image)
        self.logo.setAlignment(QtCore.Qt.AlignCenter)
        self.logo.setStyleSheet('margin-top: 50px; margin-bottom: 30px;')

        self.grid = QGridLayout()
        self.grid.addWidget(self.your_score, 0, 0)
        self.grid.addWidget(self.score, 0, 1)
        self.grid.addWidget(self.question, 1, 0, 1, 2)
        self.grid.addWidget(self.btn1, 2, 0)
        self.grid.addWidget(self.btn2, 2, 1)
        self.grid.addWidget(self.btn3, 3, 0)
        self.grid.addWidget(self.btn4, 3, 1)
        self.grid.addWidget(self.logo, 4, 0, 1, 2)

        self.container = QFrame()
        self.container.setLayout(self.grid)
        self.setCentralWidget(self.container)
        self.show()

    def get_index(self):
        self.index = random.randint(0, 49)
        for _ in parameters['index']:
            if self.index in parameters['index']:
                self.index = random.randint(0, 49)
        else:
            parameters['index'].append(self.index)
            print(parameters['index'][-1])

    def get_data(self, df):
        self.get_index()
        parameters['question'].append(formatting(df['question'][parameters['index'][-1]]))
        print("parameters['question']", parameters['question'][-1])

        parameters['correct'].append(formatting(df['correct_answer'][parameters['index'][-1]]))
        print("parameters['correct']", parameters['correct'][-1])

        wrong_answers = formatting_wrong(df['incorrect_answers'][parameters['index'][-1]])
        print('wrong_answers', wrong_answers)

        all_answers = wrong_answers + [parameters['correct'][-1]]
        random.shuffle(all_answers)
        print('all answers', all_answers)
        parameters['answer1'].append(all_answers[0])
        parameters['answer2'].append(all_answers[1])
        parameters['answer3'].append(all_answers[2])
        parameters['answer4'].append(all_answers[3])

    def create_button(self, answer, l_margin, r_margin):
        """Method create buttons with answers"""
        self.btn = QPushButton(answer)
        self.btn.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.btn.setFixedWidth(500)
        self.btn.setStyleSheet(
            '*{border: 4px solid "#bd93f9";'
            'margin-left: ' + str(l_margin) + 'px;'
            'margin-right: ' + str(r_margin) + 'px;'
            'border-radius: 25px;'
            'font-size: 16px;'
            'color: "#8be9fd";'
            'padding: 15px 0;'
            'margin-top: 20px;'
            '}'
            '*:hover{background: "#6272a4";}')
        return self.btn

    def click_on_btn(self, lvl_name):
        """Button click event with response"""
        self.btn1.clicked.connect(lambda x: self.click(self.btn1.text(), lvl_name))
        self.btn2.clicked.connect(lambda x: self.click(self.btn2.text(), lvl_name))
        self.btn3.clicked.connect(lambda x: self.click(self.btn3.text(), lvl_name))
        self.btn4.clicked.connect(lambda x: self.click(self.btn4.text(), lvl_name))

    def click(self, text, lvl_name):
        """The method checks whether the answer is correct or not and open Victory window or Lose window"""
        if text == parameters['correct'][-1]:
            parameters['score'] += 10

            if parameters['score'] == 100:
                WinFrame(lvl_name).show()
                self.close()
            self.score.setText(str(parameters['score']))
            self.get_data(self.df)
            self.question.setText(parameters['question'][-1])
            self.btn1.setText(parameters['answer1'][-1])
            self.btn2.setText(parameters['answer2'][-1])
            self.btn3.setText(parameters['answer3'][-1])
            self.btn4.setText(parameters['answer4'][-1])

        else:
            LoseFrame().show()
            self.close()


class WinFrame(QMainWindow):
    """Victory window with congratulations"""
    def __init__(self, lvl_name):
        super().__init__()

        self.setWindowTitle(f'Who want to be a {lvl_name} EXPERT')
        self.setMinimumSize(1000, 600)
        self.setStyleSheet('background: #282a36;')

        self.ico = QIcon()
        self.ico.addFile('ico_expert.ico')
        self.setWindowIcon(self.ico)

        self.grid = QGridLayout()
        self.container = QFrame()
        self.container.setLayout(self.grid)
        self.setCentralWidget(self.container)

        self.win_message = QLabel(f'Congratulations!\nYou are a TRUE {lvl_name} EXPERT!\n\nYour score is:')
        self.win_message.setAlignment(QtCore.Qt.AlignRight)
        self.win_message.setStyleSheet("font-family: 'Arial'; font-size: 25px; color: '#50fa7b'; margin: 50px 0px;")

        self.image = QPixmap('logo_expert1.png')
        self.logo = QLabel()
        self.logo.setPixmap(self.image)
        self.logo.setAlignment(QtCore.Qt.AlignCenter)

        self.score = QLabel('100')
        self.score.setAlignment(QtCore.Qt.AlignLeft)
        self.score.setStyleSheet("font-family: 'Arial'; font-size: 100px; color: #f1fa8c; margin: 50px 75px 0px 75px;")

        self.message = QLabel("OK, now go back to WORK \n\n OR")
        self.message.setAlignment(QtCore.Qt.AlignCenter)
        self.message.setStyleSheet("font-family: 'Arial'; font-size: 30px; color: '#8be9fd'; ")

        self.btn_try_again = QPushButton('TRY AGAIN')
        self.btn_try_again.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_try_again.setStyleSheet(
            '*{border: 4px solid "#bd93f9";'
            'border-radius: 45px;'
            'font-family: Arial;'
            'font-size: 35px;'
            'color: "#8be9fd";'
            'padding: 25px 0;'  # space inside the button
            'margin: 50px 200px;'  # space outside the button
            '}'
            '*:hover{background: "#6272a4";}')
        self.btn_try_again.clicked.connect(lambda x: self.click_try_again())

        self.grid.addWidget(self.win_message, 1, 0)
        self.grid.addWidget(self.score, 1, 1)
        self.grid.addWidget(self.message, 2, 0, 1, 2)
        self.grid.addWidget(self.btn_try_again, 3, 0, 1, 2)
        self.grid.addWidget(self.logo, 4, 0, 1, 2)

    def click_try_again(self):
        global parameters
        parameters = {
            'question': [],
            'answer1': [],
            'answer2': [],
            'answer3': [],
            'answer4': [],
            'correct': [],
            'score': 0,
            'index': []
        }
        MainFrame()
        self.close()


class LoseFrame(WinFrame):
    """Lose window"""
    def __init__(self):
        super().__init__(lvl_name=None)
        self.lose_message = QLabel("Sorry, this answer was wrong!\n\n Your score is:")
        self.lose_message.setAlignment(QtCore.Qt.AlignRight)
        self.lose_message.setStyleSheet("font-family: 'Arial'; font-size: 25px; color: '#50fa7b'; margin: 100px 0px;")

        self.lose_score = QLabel(str(parameters['score']))
        self.lose_score.setAlignment(QtCore.Qt.AlignLeft)
        self.lose_score.setStyleSheet("font-size: 100px; color: #ff5555; margin: 80px 75px 0px 75px;")

        self.grid = QGridLayout()
        self.grid.addWidget(self.lose_message, 1, 0)
        self.grid.addWidget(self.lose_score, 1, 1)
        self.grid.addWidget(self.btn_try_again, 3, 0, 1, 2)
        self.grid.addWidget(self.logo, 4, 0, 1, 2)

        self.container = QFrame()
        self.container.setLayout(self.grid)
        self.setCentralWidget(self.container)


class NoInternet(QMainWindow):
    """Window when there is no internet"""
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Who want to be an EXPERT')
        self.setMinimumSize(500, 300)
        self.setStyleSheet('background: #282a36;')

        self.ico = QIcon()
        self.ico.addFile('ico_expert.ico')
        self.setWindowIcon(self.ico)

        self.message = QLabel('Some problems with Internet connection.\n\nTry again later.')
        self.message.setMinimumHeight(220)
        self.message.setAlignment(QtCore.Qt.AlignCenter)
        self.message.setStyleSheet(
            'font-family: Arial;'
            'font-size: 25px;'
            'color: "#ff5555";'
        )

        self.image = QPixmap('logo_expert1.png')
        self.logo = QLabel()
        self.logo.setPixmap(self.image)
        self.logo.setAlignment(QtCore.Qt.AlignCenter)

        self.grid = QGridLayout()
        self.container = QFrame()
        self.container.setLayout(self.grid)
        self.setCentralWidget(self.container)
        self.grid.addWidget(self.message)
        self.grid.addWidget(self.logo)

        self.show()


class SplashScreen(QMainWindow, Ui_SplashScreen):
    """Startup splash screen with loading process"""
    def __init__(self):
        super().__init__()
        self.ico = QIcon()
        self.ico.addFile('ico_expert.ico')
        self.setWindowIcon(self.ico)
        self.setupUi(self)
        self.setWindowTitle('Who want to be an EXPERT')

        # REMOVE TITLE BAR
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # DROP SHADOW EFFECT
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 60))
        self.dropShadowFrame.setGraphicsEffect(self.shadow)

        # Q TIMER ==> START
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.progress)
        self.timer.start(20)  # time in ms after which the counter changes in def progress

        # CHANGE DESCRIPTION
        QtCore.QTimer.singleShot(0, lambda: self.label_description.setText('<strong>LOADING</strong> DATABASE'))
        QtCore.QTimer.singleShot(2000, lambda: self.label_description.setText('<strong>LOADING</strong> '
                                                                              'USER INTERFACE'))
        self.show()

    def progress(self):
        global counter
        self.progressBar.setValue(counter)  # SET VALUE TO progressBar
        if counter > 100:  # CLOSE SPLASH SCREEN AND OPEN APP
            self.timer.stop()  # STOP Timer
            MainFrame()
            self.close()  # CLOSE SPLASH SCREEN
        counter += 1


counter = 0  # counter for SplashScreen

if __name__ == '__main__':
    urls = [MOVIE, HISTORY, MUSIC, GEOGRAPHY]
    for i in urls:
        try:
            response = urlopen(i)
            print('ok')
            app = QApplication(sys.argv)
            example = SplashScreen()
            # example = MainFrame()
            sys.exit(app.exec_())
        except (HTTPError, URLError) as error:
            print(f'Data of not retrieved because {error}\nURL: {i}')
        except socket.timeout:
            print(f'socket timed out - URL {i}')

        print('not ok')
        app = QApplication(sys.argv)
        example = NoInternet()
        sys.exit(app.exec_())
