import sys
from PyQt4 import QtGui, QtCore
import cv2
import random
import time
import openface_implementation
import calcul_csv

class VideoClass(QtGui.QWidget):


    def __init__(self):
        self.rep = 0
        super(QtGui.QWidget, self).__init__()
        self.lastsave = time.time()
        self.fps = 24

        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')

        self.doneNeutral = False
        self.shouldrec = False
        self.shouldanal = False
        self.shouldscore = False

        self.emotion = ""

        self.emotionList = ["Neutral", "Happy","Sad","Surprised","Angry","Embarrassment"]
        #self.emotionVisited
        self.cap = cv2.VideoCapture(0)

        emotionfont = QtGui.QFont()
        emotionfont.setPointSize(50)
        emotionfont.setBold(True)

        self.video_label = QtGui.QLabel()
        self.pushButton = QtGui.QPushButton(self.emotionList[0])

        self.pushButton.setStyleSheet('QPushButton {background-color: #B13E34; color: white;}')
        self.pushButton.setFont(emotionfont)
        self.pushButton2 = QtGui.QPushButton("Initializing")
        self.progressBar = QtGui.QProgressBar()
        self.progressBar.setProperty("Initializing", 0)

        lay = QtGui.QVBoxLayout()
        lay.setMargin(0)
        lay.addWidget(self.pushButton2)
        lay.addWidget(self.progressBar)
        lay.addWidget(self.video_label)
        lay.addWidget(self.pushButton)


        self.setLayout(lay)
        self.setGeometry(630,1,1,1) # webcam position for 1080p res screens
        self.setWindowTitle('Analysing...')

    def setEmotion(self):
        if self.doneNeutral:
            num = random.randint(0, len(self.emotionList) - 1)
        else:
            num = 0
            self.doneNeutral = True

        self.emotion = self.emotionList[num]
        self.pushButton.setText(self.emotion)
        self.emotionList.pop(num)


    def processFrame(self):
        ret, frame = self.cap.read()

        #self.out.write(frame)
        if self.shouldrec == True:
            if self.emotion == "Happy":
                self.happyout.write(frame)
            elif self.emotion == "Sad":
                self.sadout.write(frame)
            elif self.emotion == "Surprised":
                self.surprisedout.write(frame)
            elif self.emotion == "Angry":
                self.angryout.write(frame)
            elif self.emotion == "Neutral":
                self.neutralout.write(frame)
            elif self.emotion == "Embarrassment":
                self.embout.write(frame)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = QtGui.QImage(frame, 640, 480, QtGui.QImage.Format_RGB888)
        pix = QtGui.QPixmap.fromImage(img)
        self.video_label.setPixmap(pix)
        seconds_left = (time.time() - self.lastsave)
        self.pushButton2.setText("Time Left : " + str(round(10 - seconds_left,1)) + "s" )
        self.progressBar.setValue( seconds_left/10 * 100)
        if time.time() - self.lastsave > 10:
            if self.rep < 0:
                self.pushButton2.setText("Processing...") # This does not trigger unfortunately
                self.deleteLater()
                if self.shouldanal:
                    self.processVideoForCSV()
                    print("processed")
                if self.shouldscore:
                    self.processCSVForResult()
                    print("scored")
                msgbox = QtGui.QMessageBox.about(self, 'Done', 'Processing Complete!\nPlease restart the program for further use!')

            else:
                self.setEmotion()
                self.lastsave = time.time()
                self.rep-=1
                print(str(self.rep))


    def processVideoForCSV(self):
        if self.shouldanal:
            print("analysing")
            emolist = ["neu", "hap", "sad", "sur", "ang","emb"]
            #time.sleep(1)  # I think we dont need this. AVI conversion is immediate
            while len(emolist) > 0:
                emo = emolist.pop(0)
                print(str(emo))
                openface_implementation.openface_execute(self.filename + emo, self.filename+emo)



    def processCSVForResult(self):
        if self.shouldscore:
            print("scoring")
            emolist = ["hap", "sad", "sur", "ang","emb"]
            # reading standard AU
            calcul_csv.stand_read_csv("extreme_au_extract.csv")

            #add neutral part
            neutral_mean = calcul_csv.neut_read_csv(self.filename + "neu.csv")
            calcul_csv.calcul_nue_dis(neutral_mean)

            f = open(self.filename+"distance_output.txt", "w")
            f2 = open(self.filename+"score_output.txt", "w")
            while len(emolist) > 0:
                emo = emolist.pop(0)
                return_dict, minimum = calcul_csv.calcul_emotion_dis_csv(self.filename + emo + ".csv")

                #calculate score & write score file
                #print(emo+ " " + str(calcul_csv.score_calcul(emo, minimum)))
                total_sc, fi_sc = calcul_csv.score_calcul(emo, minimum)
                f2.write(emo+"\n")
                f2.write(str(total_sc)+"\n")
                f2.write(str(fi_sc)+"\n")

                #write distance file
                f.write(emo + " : " + str(minimum) + "\n")
                for key in return_dict:
                    f.write(str(key) + '\t')
                    for i in range(0, len(return_dict[key])):
                        f.write(str(return_dict[key][i]) + "\t")
                    f.write("\n")
                    # f.write(emo + " : " + str(calcul_csv.calcul_read_csv(emo+".csv"))+"\n")

    def start(self,emotion,crec,canal,cscore,name):
        if emotion == "Start":
            self.rep = 4
        else:
            self.rep = -1
        self.setEmotion()
        # self.pushButton.setText("EMOTION : " + str(emotion))
        self.shouldanal = canal
        self.shouldrec = crec
        self.shouldscore = cscore

        self.lastsave = time.time()

        if name != "":
            self.filename = name + "_"
        else:
            self.filename = ""

        if self.shouldrec:
            self.neutralout = cv2.VideoWriter(self.filename + "neu.avi", self.fourcc, self.fps, (640, 480))
            self.happyout = cv2.VideoWriter(self.filename+"hap.avi", self.fourcc, self.fps, (640, 480))
            self.sadout = cv2.VideoWriter(self.filename+"sad.avi", self.fourcc, self.fps, (640, 480))
            self.surprisedout = cv2.VideoWriter(self.filename+"sur.avi", self.fourcc, self.fps, (640, 480))
            self.angryout = cv2.VideoWriter(self.filename+"ang.avi", self.fourcc, self.fps, (640, 480))
            self.embout = cv2.VideoWriter(self.filename+"emb.avi", self.fourcc, self.fps, (640, 480))
            self.timer = QtCore.QTimer()
            self.timer.timeout.connect(self.processFrame)
            self.timer.start(1000. / self.fps)
        if self.shouldrec==False:
            self.pushButton.setText("Please Wait")
            self.processVideoForCSV()
            self.processCSVForResult()
            self.deleteLater()
            msgbox = QtGui.QMessageBox.about(self,'Done','Processing Complete!\nPlease restart the program for further use!')


    def stop(self):
        self.timer.stop()


    def deleteLater(self):
        self.cap.release()
        super(QtGui.QWidget, self).deleteLater()


class MainMenuClass(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.capture = None

        self.checkRecord = False
        self.checkAnalyse = False
        self.checkScore = False
        self.name = ""

        menufont = QtGui.QFont()
        menufont.setPointSize(18)

        self.full_start = QtGui.QPushButton('Start!')
        self.full_start.clicked.connect(lambda: self.startCapture("Start",self.checkRecord,self.checkAnalyse,self.checkScore,self.name))

        self.record_check_box = QtGui.QCheckBox('Record Video')
        self.analyse_check_box = QtGui.QCheckBox('Analyse Video')
        self.score_check_box = QtGui.QCheckBox('Score Extacted Data')

        self.record_check_box.stateChanged.connect(self.recordCheckBoxChecked)
        self.analyse_check_box.stateChanged.connect(self.analyseCheckBoxChecked)
        self.score_check_box.stateChanged.connect(self.scoreCheckBoxChecked)

        self.full_start.setFont(menufont)
        # self.happy_start = QtGui.QPushButton('Happy')
        # self.happy_start.clicked.connect(lambda: self.startCapture("Happy"))
        #
        # self.sad_start = QtGui.QPushButton('Sad')
        # self.sad_start.clicked.connect(lambda: self.startCapture("Sad"))
        #
        # self.surprised_start = QtGui.QPushButton('Surprised')
        # self.surprised_start.clicked.connect(lambda: self.startCapture("Surprised"))
        #
        # self.anger_start = QtGui.QPushButton('Anger')
        # self.anger_start.clicked.connect(lambda: self.startCapture("Anger"))

        self.info_button = QtGui.QPushButton('Info')
        self.info_button.clicked.connect(self.infoActivate)

        self.quit_button = QtGui.QPushButton('Stop Recording')
        self.quit_button.clicked.connect(self.endCapture)

        self.lineedit = QtGui.QLineEdit('<enter name>')

        self.lineedit.textChanged.connect(self.namechanged)


        lay2 = QtGui.QVBoxLayout(self)
        lay2.addWidget(self.full_start)
        lay2.addWidget(self.lineedit)
        lay2.addWidget(self.record_check_box)
        lay2.addWidget(self.analyse_check_box)
        lay2.addWidget(self.score_check_box)


        # lay2.addWidget(self.happy_start)
        # lay2.addWidget(self.sad_start)
        # lay2.addWidget(self.surprised_start)
        # lay2.addWidget(self.anger_start)
        # lay2.addWidget(self.emotion_button)
        lay2.addWidget(self.info_button)
        lay2.addWidget(self.quit_button)



        self.setLayout(lay2)
        self.setWindowTitle('Emotion Intensity Analyser')
        self.show()

    def namechanged(self,text):
        self.name = text


    def infoActivate(self):
        infostr =  ""
        infostr += "1. Record Video: Activate webcam\n"
        infostr += "2. Analyse Video: Video -> CSV\n"
        infostr += "3. Score Data: CSV -> Score\n "
        infostr += ""
        infostr += "\n\n"
        infostr += "- Made By -\n"
        infostr += "Seoyeon Park\n"
        infostr += "Youhyeon Hwang\n"
        infostr += "Minhyung Kim"
        msgbox = QtGui.QMessageBox.about(self, 'Information',
                                         infostr)

    def recordCheckBoxChecked(self):
        if self.record_check_box.isChecked():
            self.checkRecord = True
        else:
            self.checkRecord = False

    def analyseCheckBoxChecked(self):
        if self.analyse_check_box.isChecked():
            self.checkAnalyse = True
        else:
            self.checkAnalyse = False

    def scoreCheckBoxChecked(self):
        if self.score_check_box.isChecked():
            self.checkScore = True
            #warningbox = QtGui.QMessageBox.about(self, 'Warning!','NOTE: This will only analyse csv files with no naming conventions (ex. adrian_hap.csv will NOT work)')
        else:
            self.checkScore = False

    def cemotion(self):
        self.capture.setEmotion()

    def startCapture(self, emotion, crec, canal, cscore, name):
        self.full_start.setStyleSheet('QPushButton {background-color: #7C9060; color: white;}')
        self.full_start.setText("Please Restart after Recording / Analysis :)")
        if not self.capture:
            self.capture = VideoClass() # Create VideoClass instance
            self.capture.setParent(self) # 메인 닫으면 비디오도 꺼버려
            self.capture.setWindowFlags(QtCore.Qt.Window) # 비디오는 따로 윈도우 띄우기
        self.capture.start(emotion,crec,canal,cscore,name)

        self.capture.show()

    def endCapture(self):
        self.capture.deleteLater()
        self.capture = None

if __name__ == '__main__':


    app = QtGui.QApplication(sys.argv)
    window = MainMenuClass()
    sys.exit(app.exec_())