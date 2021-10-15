from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
import sys
from PyQt5.uic import loadUiType
from pytube import Playlist
import urllib.request
import pafy
import humanize


ui,_ = loadUiType("main.ui")

class MainApp(QMainWindow, ui):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.InitUI()
        self.Handel_Buttons()
        self.setWindowIcon(QtGui.QIcon("icon\download.png"))
        self.setIconSize(QtCore.QSize(50, 50))
        self.setWindowTitle("Download")



    def InitUI(self):
        pass

    def Handel_Buttons(self):
        self.pushButton.clicked.connect(self.Download)
        self.pushButton_2.clicked.connect(self.Handel_Browse)
        self.pushButton_5.clicked.connect(self.get_video_data)
        self.pushButton_4.clicked.connect(self.download_video_audio)
        self.pushButton_3.clicked.connect(self.Save_Browse)
        self.radioButton.toggled.connect(self.video)
        self.radioButton_2.toggled.connect(self.audio)
        self.pushButton_6.clicked.connect(self.save_to)
        self.pushButton_8.clicked.connect(self.get_playlist)
        self.pushButton_7.clicked.connect(self.download_playlist)



       #======================================Download File============================================#
    def Handel_Progress(self, blocknum, blocksize, totalsize):
        readed_data = blocknum * blocksize
        print(blocknum, blocksize, totalsize)
        if totalsize > 0:
            download_percentage = readed_data * 100 / totalsize
            self.progressBar.setValue(download_percentage)
            QApplication.processEvents()

    def Handel_Browse(self):
        save_location = QFileDialog.getSaveFileName(self, caption="Sava as", directory=".", filter="All Files(*.*)")
        print(str(save_location[0]))
        self.lineEdit_2.setText(str(save_location[0]))


    def Download(self):
        print("UwU yeah")
        download_url = self.lineEdit.text()
        save_location = self.lineEdit_2.text()
        print(download_url, save_location)
        if download_url == '' or save_location == '':
            QMessageBox.warning(self, "Data Error", "Provide a valid URL or save location")
        else:
            try:
                urllib.request.urlretrieve(download_url, save_location, self.Handel_Progress)
            except Exception:
                QMessageBox.warning(self, "Download Error", "Provide a valid URL or save location")
                return

        QMessageBox.information(self, "Download Completed", "The Download Completed Successfully ")

        self.lineEdit.setText('')
        self.lineEdit_2.setText('')
        self.progressBar.setValue(0)



     #=================================Download One Video Or Audio==========================================#

    def Save_Browse(self):
        save_location = QFileDialog.getExistingDirectory(self, caption="Sava as")
        print(str(save_location))
        self.lineEdit_4.setText(str(save_location))


    def video(self):
        global radio
        radio = "Video"
        print(radio)

    def audio(self):
        global radio
        radio = "Audio"
        print(radio)


    def get_video_data(self):
        video_url = self.lineEdit_3.text()
        print(video_url)
        if video_url == '':
            QMessageBox.warning(self, "Data Error", "Provide a valid video URL")
        else:
            video = pafy.new(video_url)
            print(video.allstreams)
            print(video.title)
            print(video.duration)
            print(video.author)
            print(video.length)
            print(video.viewcount)
            print(video.likes)
            print(video.dislikes)

        # =====================================Video=======================================#
        video_streams = video.videostreams
        print(video_streams)
        for streams in video_streams:
            size = humanize.naturalsize(streams.get_filesize())
            data = f"{streams.mediatype} {streams.extension} {streams.quality} {size}"
            self.comboBox.addItem(data)
        #=====================================Audio=======================================#
        video_streams = video.audiostreams
        print(video_streams)
        for streams in video_streams:
            size = humanize.naturalsize(streams.get_filesize())
            data = f"{streams.mediatype} {streams.extension} {streams.quality} {size}"
            self.comboBox_3.addItem(data)


    def download_video_audio(self):
        download_video = self.lineEdit_3.text()
        save = self.lineEdit_4.text()
        print("Download One Video")
        print(download_video, save)
        if download_video == '' or save == '':
            QMessageBox.warning(self, "Data Error", "Provide a valid URL or save location")
        else:
            try:
                video = pafy.new(download_video)
                if radio == "Video":
                    print(radio)
                    combo_Box_list_1 = []
                    video_streams_1 = video.videostreams
                    for streams in video_streams_1:
                        size = humanize.naturalsize(streams.get_filesize())
                        data = f"{streams.mediatype} {streams.extension} {streams.quality} {size}"
                        combo_Box_list_1.append(data)

                    if self.comboBox.currentText() in combo_Box_list_1:
                        print(f"insex: {combo_Box_list_1.index(self.comboBox.currentText())}, video: {combo_Box_list_1[combo_Box_list_1.index(self.comboBox.currentText())]}, comboBox: {self.comboBox.currentText()}")

                        combo_Box_1 = combo_Box_list_1.index(self.comboBox.currentText())
                        save += f"/{video_streams_1[combo_Box_1].title}.{video_streams_1[combo_Box_1].extension}"
                        print(save)
                        video_streams_1[combo_Box_1].download(filepath=save, callback=self.video_audio_progress)

                elif radio == "Audio":
                    print(radio)
                    combo_Box_list_2 = []
                    video_streams_2 = video.audiostreams
                    for streams in video_streams_2:
                        size = humanize.naturalsize(streams.get_filesize())
                        data = f"{streams.mediatype} {streams.extension} {streams.quality} {size}"
                        combo_Box_list_2.append(data)

                    if self.comboBox_3.currentText() in combo_Box_list_2:
                        print(f"insex: {combo_Box_list_2.index(self.comboBox_3.currentText())}, Audio: {combo_Box_list_2[combo_Box_list_2.index(self.comboBox_3.currentText())]}, comboBox: {self.comboBox_3.currentText()}")
                        combo_Box_2 = combo_Box_list_2.index(self.comboBox_3.currentText())
                        save += f"/{video_streams_2[combo_Box_2].title}.{video_streams_2[combo_Box_2].extension}"
                        print(save)
                        video_streams_2[combo_Box_2].download(filepath=save, callback=self.video_audio_progress)

                else:
                    QMessageBox.warning(self, "Download Error", "Provide a valid URL or save location")
            except:
                QMessageBox.warning(self, "Download Error", "Provide a valid URL or save location")
                return


            QMessageBox.information(self, "Download Completed", "The Download Completed Successfully ")
            self.progressBar_2.setValue(0)
            self.lineEdit_3.setText('')
            self.lineEdit_4.setText('')
            self.comboBox.setItem('')
            self.comboBox_3.setItem('')
            #self.radioButton_2.setToggled('')


    def video_audio_progress(self,total, recvd, ratio, rate, eta):
        self.progressBar_2.setValue(int(ratio * 100))

        QApplication.processEvents()



    #=======================================Dawnload Playlist============================================#

    #Save
    def save_to(self):
        save_location = QFileDialog.getExistingDirectory(self, caption="Sava as")
        print(str(save_location))
        self.lineEdit_6.setText(str(save_location))

    #Get Playlist
    def get_playlist(self):
        playlist_url1 = self.lineEdit_5.text()
        print(playlist_url1)
        if playlist_url1 == '':
            QMessageBox.warning(self, "Data Error", "Provide a valid video URL")
        else:
            playlist = Playlist(playlist_url1)
            print(len(playlist), playlist)
            print(playlist.title)
            self.lcdNumber_2.display(len(playlist))
            count = 1
            for video in playlist:
                vide = video
                video = pafy.new(video)
                best = video.getbestvideo(preftype="mp4")
                #size =  {round(int(best.get_filesize()) * (10 ** -6))}MB
                data = f"{best.title} {best.extension} {best.quality} {humanize.naturalsize(best.get_filesize())}"
                print(f"{count}-:  {data} Link:  {vide}")
                self.comboBox_2.addItem(f"{count}- {data}")
                count += 1

    #Download Playlist
    def download_playlist(self):

        playlist_url1 = self.lineEdit_5.text()
        save = self.lineEdit_6.text()
        print(playlist_url1)
        if playlist_url1 == '':
            QMessageBox.warning(self, "Data Error", "Provide a valid video URL")
        else:
            count = 1
            playlist = Playlist(playlist_url1)
            print(len(playlist), playlist)
            print(playlist.title)
            #self.lcdNumber_2.display(len(playlist))
            for video in playlist:
                self.lcdNumber.display(count)
                #vide = video
                video = pafy.new(video)
                best = video.getbestvideo(preftype="mp4")
                save += f"/{best.title}.{best.extension}"
                print(save)
                try:
                    best.download(filepath=save, callback=self.playlist_progress)
                    save = self.lineEdit_6.text()                    
                    count += 1
                except:
                    QMessageBox.warning(self, "Download Error", "Provide a valid URL or save location")
            QMessageBox.information(self, "Download Completed", "The Download Completed Successfully ")

            count = 0
            self.lineEdit_6.setText('')
            self.lineEdit_5.setText('')
            self.progressBar_3.setValue(0)


    def playlist_progress(self,total, recvd, ratio, rate, eta):
        self.progressBar_3.setValue(int(ratio * 100))

        QApplication.processEvents()



def main():
        app = QApplication(sys.argv)
        window = MainApp()
        window.show()
        app.exec_()


if __name__ == '__main__':
    main()

