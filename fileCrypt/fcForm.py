#!/usr/bin/python
# -*- coding: utf-8 -*-

# 
# fileCrypt - fileCrypt.py
# ------------------------
# This handles the filling of combined reports


import Tkinter
import tkFileDialog
import tkSimpleDialog
import tkMessageBox
import os
from multiprocessing import Pool

from fileCrypt import *

class form(Tkinter.Tk):
    """
    Form
    ----
    
    This is the base form class with a couple of 
    special methods for inheriting
    """
    
    def __init__(self, parent):
        Tkinter.Tk.__init__(self, parent)
        self.parent = parent
        self.initialise()
        
        
    def initialise(self):
        '''Overload this method and init controls!'''
        pass
    
class fcForm(form):
    """
    fcForm
    ------
    
    Provides simple file doalog style access to en/decrypt files/directories
    """
    fileList = []
    def initialise(self):
        # Set title
        self.title('fileCrypt')
        
        # set Size
        self.geometry('250x100')

        # initialise grid/form
        self.grid()
        
        # Set menubar
        self.menubar = Tkinter.Menu(self)
        filemenu = Tkinter.Menu(self.menubar, tearoff=0)
        filemenu.add_command(label="Exit", command=self.quit)
        self.menubar.add_cascade(label='File', menu=filemenu)
        self.config(menu=self.menubar)
        
        self.lblPasswd = Tkinter.Label(self, text="Password:", anchor="w")
        self.lblPasswd.grid(column=0, row=0, sticky='WENS')
        self.tbPasswd = Tkinter.Entry(self)
        self.tbPasswd.grid(column=0, row=1, sticky='WENS')
        
        # set top buttons
        self.btnEncrypt = Tkinter.Button(self, text=u"Encrypt...", command=self.fdEncrypt)
        self.btnEncrypt.grid(column=0, row=2, sticky='WENS')
        self.btnDecrypt = Tkinter.Button(self, text=u"Decrypt...", command=self.fdDecrypt)
        self.btnDecrypt.grid(column=0, row=3, sticky='WENS')
        
        # Allow resize to work proerly
        self.grid_columnconfigure(0, weight=1)
        for row in range(0,4):
            self.grid_rowconfigure(row, weight=1)
        
    def fdEncrypt(self):
        self._getPasswd()
        self.fileList = tkFileDialog.askopenfilenames(filetypes=[('All Files','*.*')], title='Select files to encrypt...', parent=self)
        if self.fileList == []:
            tkMessageBox.showerror(title='No Files Selected', message='You did not select any files...')
        else:
            count = 0
            for filePath in self.fileList:
                self._updateStatus(count)
                ext = os.path.splitext(filePath)[1]
                outFilePath = os.path.splitext(filePath)[0] + '.enc' + ext
                #filePath2 = open(filePath, 'rb').read()
                encryptToFile(filePath, outFilePath, self.password)
                count += 1

    def fdDecrypt(self):
        self._getPasswd()
        self.fileList = tkFileDialog.askopenfilenames(filetypes=[('All Files','*.*')], title='Select files to decrypt...', parent=self)
        if self.fileList == []:
            tkMessageBox.showerror(title='No Files Selected', message='You did not select any files...')
        else:
            count = 0
            for filePath in self.fileList:
                self._updateStatus(count)
                ext = os.path.splitext(filePath)[1]
                outFilePath = os.path.splitext(filePath)[0][:-4] + '.dec' + ext
                #filePath2 = open(filePath, 'rb').read()
                decryptToFile(filePath, outFilePath, self.password)
                count += 1
    
    def _updateStatus(self, count):
        total = len(self.fileList)
        self.status = 'completed: ' + str(count) + ' / ' + str(total)
        if count == total:
            self.status = 'fileCrypt - Complete!'
        self.title(string=self.status)
        #self.update_idletasks()
        self.update()
    
    def _getPasswd(self):
        self.password = self.tbPasswd.get()