#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygtk
pygtk.require('2.0')
import gtk,gobject
import os
import threading

class TdxDrivers:

    def Create_Dialog(self):
        if 0 == self.index: 
            self.dialog = gtk.FileChooserDialog("请选择系统的镜像文件...",
                                            self.window,gtk.FILE_CHOOSER_ACTION_OPEN,
                                            (gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,
                                            gtk.STOCK_OK,gtk.RESPONSE_OK))
        else:
            self.dialog = gtk.FileChooserDialog("请选择U盘或光盘的目录...",
                                            self.window,gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,
                                            (gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,
                                            gtk.STOCK_OK,gtk.RESPONSE_OK))
        #dialog.set_action(gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER)

        self.dialog.set_default_response(gtk.RESPONSE_OK)
        filter = gtk.FileFilter()
        filter.set_name("所有文件")
        filter.add_pattern("*")
        self.dialog.add_filter(filter)

        filter = gtk.FileFilter()
        filter.set_name("镜像文件")
        filter.add_pattern("*.iso")
        filter.add_pattern("*.ISO")
        self.dialog.add_filter(filter)

        response = self.dialog.run()
        if response == gtk.RESPONSE_OK:
            return self.dialog
        elif response == gtk.RESPONSE_CANCEL:
            self.dialog.destroy()

    def changed_cb(self,combobox):
        self.index = combobox.get_active()

    def start_search(self,widget=None,data=None):
        self.window.hide()
        gtk.gdk.flush()
        try:
            if 0 == self.index:
                print "creating /media/cdrom"
                os.system("mkdir -p /media/cdrom")
                print "mounting file to /media/cdrom"
                os.system("mount '%s' /media/cdrom" % self.filename)
                mount_point = "/media/cdrom"
            else:
                mount_point = self.filename

            abs_path = os.path.join(mount_point,"README.diskdefines")
            if not os.path.isfile(abs_path):
                message = gtk.MessageDialog(type=gtk.MESSAGE_ERROR,buttons=gtk.BUTTONS_OK)
                message.set_markup("请选择一个系统镜像、或者刻有系统的U盘或光盘")
                message.run()
                gtk.main_quit()
                return False
                             
            print "copying sources.list..."
            os.system("cp /etc/apt/sources.list /etc/apt/sources.list.bak")
            print "clearing content of sources.list..."
            os.system("echo '' > /etc/apt/sources.list")
            print "executing apt-cdrom..."
            os.system("apt-cdrom -m -d '%s' add" % mount_point)
            print "updating soft infomation..."
            os.system("apt-get update")
            print "calling software-properties-gtk..."
            os.system("software-properties-gtk --open-tab=4")
            print "restoring sources.list..."
            os.system("mv /etc/apt/sources.list.bak /etc/apt/sources.list")
            print "unmouting /media/cdrom..."
            os.system("umount '%s'" % mount_point)
            gtk.main_quit()
        except:
            pass

    def openfile(self,widget=None,data=None):
        self.dialog = self.Create_Dialog()
        if self.dialog:
            self.filename = self.dialog.get_filename()
            self.entry.set_text(self.filename)
            self.dialog.destroy()

    def close_application(self,widget=None,data=None):
        gtk.main_quit()
        return False
   
    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("离线安装无线网卡驱动")
        self.window.connect("delete_event",lambda w,e:gtk.main_quit())
        self.window.set_border_width(20)
        self.window.set_size_request(600,-1)
    
        vbox = gtk.VBox(False,0)
        self.window.add(vbox)

        hbox1 = gtk.HBox(False,10)
        vbox.pack_start(hbox1,True,False,2)
        
        combobox = gtk.combo_box_new_text()
        hbox1.pack_start(combobox,False,False,0)
        combobox.append_text('镜像:')
        combobox.append_text('光盘:')
        combobox.append_text('优盘:')
        combobox.connect('changed',self.changed_cb)
        combobox.set_active(0)

        #label = gtk.Label("镜像:")
        #hbox1.pack_start(label,False,False,0)

        self.entry = gtk.Entry()
        hbox1.pack_start(self.entry,True,True,0)
    
        button = gtk.Button("选择镜像")
        button.connect("clicked",self.openfile,None)
        hbox1.pack_start(button,False,False,0)

        separator = gtk.HSeparator()
        vbox.pack_start(separator,True,True,5)

        hbox2 = gtk.HBox(True,10)
        vbox.pack_start(hbox2,True,False,2)

        button_exit = gtk.Button("退出")
        button_exit.set_size_request(80,-1)
        button_exit.connect("clicked",self.close_application,None)
        hbox2.pack_start(button_exit,True,False,0)

        button_search = gtk.Button("开始检测")
        button_search.set_size_request(80,-1)
        button_search.connect("clicked",self.start_search,None)
        hbox2.pack_start(button_search,True,False,0)
        
        self.window.show_all()

def main():
    gtk.main()
    return 0
if __name__ == "__main__":
    TdxDrivers()
    main()
