### 
from xml.dom import minidom
import os
import shutil
import pandas as pd
from PIL import Image
from tifffile import imsave, imread, imwrite
from math import ceil, log2
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget
import imagej
import pathlib
FIJI_path = os.path.join(pathlib.Path().absolute(),'Fiji.app')
ij=imagej.init(FIJI_path)
from jnius import autoclass

class Ui_PyramidalStitcher(QWidget):
    
    Pix_shift = 0
    Input_dir = []
    Output_dir = []
    result_np = []
    
    def setupUi(self, PyramidalStitcher):
        PyramidalStitcher.setObjectName("PyramidalStitcher")
       # PyramidalStitcher.resize(450, 300)
        self.centralwidget = QtWidgets.QWidget(PyramidalStitcher)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_stitcher = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_stitcher.setObjectName("gridLayout_stitcher")
        ### input folder button
        self.input_PushButton = QtWidgets.QPushButton(self.centralwidget)
        self.gridLayout_stitcher.addWidget(self.input_PushButton, 0, 0, 1, 2)
        #self.input_PushButton.setGeometry(QtCore.QRect(40, 40, 171, 71))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.input_PushButton.setFont(font)
        self.input_PushButton.setObjectName("input_PushButton")
        
        self.input_PushButton.clicked.connect(lambda: self.INPUT_FOLDER_LOADBTN())
        
        #### output folder button
        self.Output_PushButton = QtWidgets.QPushButton(self.centralwidget)
        self.gridLayout_stitcher.addWidget(self.Output_PushButton, 0, 2, 1, 2)
        #self.Output_PushButton.setGeometry(QtCore.QRect(260, 40, 171, 71))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.Output_PushButton.setFont(font)
        self.Output_PushButton.setObjectName("Output_PushButton")
        
        self.Output_PushButton.clicked.connect(lambda: self.OUTPUT_FOLDER_LOADBTN())
        
        # Overlap label and spinbox
        self.overlap_Label = QtWidgets.QLabel(self.centralwidget)
        self.gridLayout_stitcher.addWidget(self.overlap_Label, 1, 0, 1, 2)
        #self.overlap_Label.setGeometry(QtCore.QRect(80, 140, 170, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.overlap_Label.setFont(font)
        self.overlap_Label.setObjectName("overlap_Label")
        self.overlap_spinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.gridLayout_stitcher.addWidget(self.overlap_spinBox, 1, 2, 1, 1)
        #self.overlap_spinBox.setGeometry(QtCore.QRect(280, 140, 81, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.overlap_spinBox.setFont(font)
        self.overlap_spinBox.setMaximum(1000)
        self.overlap_spinBox.setObjectName("overlap_spinBox")
        
        #### output type checkboxes
        self.sep_channels_checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.gridLayout_stitcher.addWidget(self.sep_channels_checkBox, 3, 0, 1, 2)
        #self.sep_channels_checkBox.setGeometry(QtCore.QRect(30, 230, 221, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.sep_channels_checkBox.setFont(font)
        self.sep_channels_checkBox.setObjectName("sep_channels_checkBox")
        self.multi_ch_checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.gridLayout_stitcher.addWidget(self.multi_ch_checkBox, 4, 0, 1, 2)
        #self.multi_ch_checkBox.setGeometry(QtCore.QRect(30, 270, 221, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.multi_ch_checkBox.setFont(font)
        self.multi_ch_checkBox.setObjectName("multi_ch_checkBox")
        self.multi_ch_pyr_checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.gridLayout_stitcher.addWidget(self.multi_ch_pyr_checkBox, 5, 0, 1, 2)
        #self.multi_ch_pyr_checkBox.setGeometry(QtCore.QRect(30, 310, 230, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.multi_ch_pyr_checkBox.setFont(font)
        self.multi_ch_pyr_checkBox.setObjectName("multi_ch_pyr_checkBox")
        self.min_size_label = QtWidgets.QLabel(self.centralwidget)
        self.gridLayout_stitcher.addWidget(self.min_size_label, 5, 2, 1, 1)
        #self.min_size_label.setGeometry(QtCore.QRect(270, 310, 140, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.min_size_label.setFont(font)
        self.min_size_label.setStyleSheet("color: red")
        self.min_size_label.setObjectName("min_size_label")
        self.min_size_spinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.gridLayout_stitcher.addWidget(self.min_size_spinBox, 5, 3, 1, 1)
        #self.min_size_spinBox.setGeometry(QtCore.QRect(410, 310, 91, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.min_size_spinBox.setFont(font)
        self.min_size_spinBox.setMaximum(10001)
        self.min_size_spinBox.setObjectName("min_size_spinBox")
        self.outputtype_Label = QtWidgets.QLabel(self.centralwidget)
        self.gridLayout_stitcher.addWidget(self.outputtype_Label, 2, 0, 1, 2)
        #self.outputtype_Label.setGeometry(QtCore.QRect(30, 190, 130, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setItalic(True)
        self.outputtype_Label.setStyleSheet("color: blue")
        self.outputtype_Label.setFont(font)
        self.outputtype_Label.setObjectName("outputtype_Label")
        
        ### Run Push button
        self.run_PushButton = QtWidgets.QPushButton(self.centralwidget)
        self.gridLayout_stitcher.addWidget(self.run_PushButton, 6, 1, 1, 2)
        #self.run_PushButton.setGeometry(QtCore.QRect(150, 360, 171, 55))
        font = QtGui.QFont()
        font.setPointSize(17)
        self.run_PushButton.setFont(font)
        self.run_PushButton.setObjectName("run_PushButton")
        PyramidalStitcher.setCentralWidget(self.centralwidget)
        
        self.run_PushButton.clicked.connect(lambda: self.ON_RUN_BTN())

        self.retranslateUi(PyramidalStitcher)
        QtCore.QMetaObject.connectSlotsByName(PyramidalStitcher)

    def retranslateUi(self, PyramidalStitcher):
        _translate = QtCore.QCoreApplication.translate
        PyramidalStitcher.setWindowTitle(_translate("PyramidalStitcher", "PyramidalStitcher"))
        self.input_PushButton.setText(_translate("PyramidalStitcher", "Input Folder"))
        self.Output_PushButton.setText(_translate("PyramidalStitcher", "Output Folder"))
        self.overlap_Label.setText(_translate("PyramidalStitcher", "Overlap In Pixels:"))
        self.sep_channels_checkBox.setText(_translate("PyramidalStitcher", "Separate Channels"))
        self.multi_ch_checkBox.setText(_translate("PyramidalStitcher", "Multi-Channel"))
        self.multi_ch_pyr_checkBox.setText(_translate("PyramidalStitcher", "Multi-Channel-Pyramidal"))
        self.min_size_label.setText(_translate("PyramidalStitcher", "Minimum Size:"))
        self.outputtype_Label.setText(_translate("PyramidalStitcher", "Ouput Type:"))
        self.run_PushButton.setText(_translate("PyramidalStitcher", "Run"))
        
    def INPUT_FOLDER_LOADBTN(self):
        
        options = QtWidgets.QFileDialog.Options()
        self.Input_dir = QtWidgets.QFileDialog.getExistingDirectory(self, caption= "Select Input Directory", options=options)
        
        #### READING .MES FILE FOR EXTRACTING PIXEL OVERLAP
        for mes_file in os.listdir(self.Input_dir):
            if mes_file.endswith(".mes"):
                mesfilename = os.path.join(self.Input_dir,mes_file)
                mydoc_mes = minidom.parse(mesfilename)
                items_mes = mydoc_mes.getElementsByTagName('bts:PartialTiledPosition')

                self.Pix_shift = int(items_mes[0].attributes['bts:OverlappingPixels'].value)/2
                self.overlap_spinBox.setValue(self.Pix_shift)
    def OUTPUT_FOLDER_LOADBTN(self):
        
        options = QtWidgets.QFileDialog.Options()
        self.Output_dir = QtWidgets.QFileDialog.getExistingDirectory(self, caption= "Select Output Directory", options=options)
     
     
    def ON_RUN_BTN(self):
        
        for mlf_file in os.listdir(self.Input_dir):
            if mlf_file.endswith(".mlf"):
                metadatafilename = os.path.join(self.Input_dir,mlf_file)

        mydoc = minidom.parse(metadatafilename)
        PATH_TO_FILES = os.path.split(metadatafilename)[0]
        items = mydoc.getElementsByTagName('bts:MeasurementRecord')

        #### READING .MES FILE FOR EXTRACTING PIXEL OVERLAP
        for mes_file in os.listdir(self.Input_dir):
            if mes_file.endswith(".mes"):
                mesfilename = os.path.join(self.Input_dir,mes_file)

        mydoc_mes = minidom.parse(mesfilename)
        items_mes = mydoc_mes.getElementsByTagName('bts:PartialTiledPosition')

        Pix_shift = int(items_mes[0].attributes['bts:OverlappingPixels'].value)/2

        df_cols = ["ImageName", "Column", "Row", "TimePoint", "FieldIndex", "Channel", "Xposition", "Yposition", "Zposition"]
        rows = []

        for i in range(items.length):
            if items[i].attributes['bts:Type'].value=="IMG":
                rows.append({
                             "ImageName": os.path.join(items[i].firstChild.data), 
                             "Column": items[i].attributes['bts:Column'].value, 
                             "Row": items[i].attributes['bts:Row'].value, 
                             "TimePoint": items[i].attributes['bts:TimePoint'].value, 
                             "FieldIndex": items[i].attributes['bts:FieldIndex'].value, 
                             "Channel":items[i].attributes['bts:Ch'].value,
                             "Xposition": items[i].attributes['bts:X'].value,
                             "Yposition": items[i].attributes['bts:Y'].value,
                             "Zposition": items[i].attributes['bts:Z'].value 
                            })
            
        out_df = pd.DataFrame(rows, columns = df_cols)

        xpos = out_df['Xposition'].unique()
        ypos = out_df['Yposition'].unique()
        channels_names = out_df['Channel'].unique()

        num_channels = channels_names.__len__()

        for i in range(num_channels):
                            
            configfile = open(os.path.join(self.Input_dir,"TileConfiguration.txt"),"w") 
            L = ["# Define the number of dimensions we are working on \n",
                 "dim  = 2",
                 "\n\n",
                 "# Define the image coordinates \n"]
            configfile.writelines(L)

            for x in range(xpos.__len__()):
                for y in range(ypos.__len__()):
                    select_color =out_df.loc[(out_df['Xposition'] == str(xpos[x])) 
                                             & (out_df['Yposition'] == str(ypos[y]))
                                             & (out_df['Channel'] == str(channels_names[i]))]

                    if i==0:
                        im = Image.open(os.path.join(self.Input_dir,select_color['ImageName'].iloc[0]))
                        height, width = np.asarray(im).shape
                    x_shift = x*(width-Pix_shift)
                    y_shift = y*(height-Pix_shift)
                    img_name = select_color['ImageName'].iloc[0]
                    lines = img_name + "; ; (" + str(x_shift) + "," + str(y_shift) + ") \n"
                    configfile.writelines(lines)
            configfile.close()

            args = {'type': 'Positions from file', 'order': 'Defined by TileConfiguration', 'directory':self.Input_dir, 
                    'ayout_file': 'TileConfiguration.txt', 'fusion_method': 'Linear Blending', 'regression_threshold': '0.30', 
                    'max/avg_displacement_threshold':'2.50', 'absolute_displacement_threshold': '3.50', 
                    'computation_parameters': 'Save computation time (but use more RAM)', 'image_output': 'Fuse and display'}

            plugin = "Grid/Collection stitching"
            print(self.Input_dir)
            ij.py.run_plugin(plugin, args)
            
            WindowManager = autoclass('ij.WindowManager')
            result = WindowManager.getCurrentImage()
            fiji_image_to_np = ij.py.from_java(result).astype('uint16')
            
            self.result_np.append(fiji_image_to_np)
            
            if self.sep_channels_checkBox.isChecked() == True:
                
                sep_ch_path = os.path.join(self.Output_dir, 'Separate Channels')
                if os.path.isdir(sep_ch_path) == False:
                    os.mkdir(sep_ch_path)  

                stitched_image_name = 'Stitched_Channel_'+ str(channels_names[i]) + '.tif'
                Out_img_name = os.path.join(sep_ch_path, stitched_image_name)
                imsave(Out_img_name,fiji_image_to_np)
            os.remove(os.path.join(self.Input_dir,"TileConfiguration.txt"))
        
        multi_ch_path = os.path.join(self.Output_dir, 'Multi Channel')
        if os.path.isdir(multi_ch_path) == False:
            os.mkdir(multi_ch_path)
        multi_ch_image_name = 'Multi_Channel.tif'
        multi_ch_img_name = os.path.join(multi_ch_path, multi_ch_image_name)
        multi_channel = np.stack(self.result_np, axis=0)
        imwrite(multi_ch_img_name, multi_channel, imagej=True)
        
        #imsave(multi_ch_img_name,multi_channel)
        h,w,c = multi_channel.shape
        
        if self.multi_ch_pyr_checkBox.isChecked() == True:
            
            multi_ch_pyr_path = os.path.join(self.Output_dir, 'Pyramidal Tif')
            if os.path.isdir(multi_ch_pyr_path) == False:
                os.mkdir(multi_ch_pyr_path)
            multi_ch_pyramid_image_name = 'Multi_Channel_pyramidal.tif'
            pyr_img_name = os.path.join(multi_ch_pyr_path, multi_ch_pyramid_image_name)
            
            img_min_size = self.min_size_spinBox.value()
            pyr_res = ceil(log2(max(w, h)/img_min_size))
            
            command_part1= r'.\\bftools\\bfconvert -tilex 512 -tiley 512 -noflat -pyramid-resolutions '  + str(pyr_res) 
            command_part2=  ' -pyramid-scale 2 ' + r'"'+ multi_ch_img_name + r'"' + r' "' + pyr_img_name +  r'"'
            command = command_part1+command_part2
            os.system(command)
            
        if self.multi_ch_checkBox.isChecked() == False:
            
            shutil.rmtree(multi_ch_path)



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    PyramidalStitcher = QtWidgets.QMainWindow()
    ui = Ui_PyramidalStitcher()
    ui.setupUi(PyramidalStitcher)
    PyramidalStitcher.show()
    sys.exit(app.exec_())

