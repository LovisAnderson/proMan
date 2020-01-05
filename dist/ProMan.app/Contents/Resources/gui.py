# -*- coding: utf-8 -*-


from tkinter import *
from tkinter import filedialog, messagebox
from tmp.configure import Configuration
from PIL import Image, ImageTk
from tmp.copy_folders import copy_directory, create_empty_dir
from tmp.combobox import AutocompleteCombobox
from pathlib import Path
import subprocess
from collections import OrderedDict
import os


btn_h = 3
btn_w = 20
gui_width = 750
gui_height = 400
font_color = '#4d1300'
btn_bg_color = '#e6e6e6'
bg_color = 'white'


APPLICATION_PATH = ''


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def __main__():

    root = Tk()
    root.wm_title("Datei Management System")
    root.config(background=bg_color)  # sets background color to white
    configuration = Configuration()
    Gui(root, configuration)
    root.mainloop()
    pass


class Gui():
    def __init__(self, root, configuration):
        self.root = root
        self.configuration = ()
        self.action_frame = NewCustomer(self.root, configuration, self)
        self.upper_frame = StaticUpperMenu(self.root, configuration, self)


class UpperFrame(object):
    def __init__(self, root, configuration, gui):
        self.gui = gui
        self.frame = Frame(root, width=gui_width, height=100, bg=bg_color)
        self.frame.grid(row=0, pady=15, padx=15, sticky=W)
        self.configuration = configuration
        self.root = root

        pass


class StaticUpperMenu(UpperFrame):
    def __init__(self, root, configuration, gui):
        self.name = 'static upper menu'
        super(StaticUpperMenu, self).__init__(root, configuration, gui)

        btn_h = 45
        btn_w = 60
        pady = 1
        btn_bdw = 3

        image_path = os.path.join(APPLICATION_PATH, "plus_small.png")
        image = Image.open(image_path)
        self.photo = ImageTk.PhotoImage(image)

        new_customer_btn = Button(self.frame, bg=btn_bg_color,  text='Kunde',
                                  command=self.new_customer,
                                  borderwidth=btn_bdw,
                                  height=btn_h, width=btn_w,
                                  highlightthickness=0, highlightbackground='white',
                                  fg=font_color, compound='left', image=self.photo)

        new_customer_btn.grid(row=0, column=0, padx=2, pady=pady, sticky=W)

        new_project_btn = Button(self.frame, bg=btn_bg_color, text='Projekt',
                                 command=self.new_project,
                                 borderwidth=btn_bdw,
                                 height= btn_h, width=btn_w,
                                 highlightthickness=0, highlightbackground='white',
                                 fg=font_color, compound='left', image=self.photo)
        new_project_btn.grid(row=0, column=1, padx=2, pady=pady, sticky=W)

        image_path = os.path.join(APPLICATION_PATH, "settings_small.png")
        image = Image.open(image_path)
        self.settings_icon = ImageTk.PhotoImage(image)
        settings_btn = Button(self.frame,
                              borderwidth=btn_bdw,
                              image=self.settings_icon,
                              bg=bg_color,
                              command=self.settings,
                              highlightthickness=0,
                              highlightbackground='white')

        settings_btn.grid(row=0, column=2, sticky=W, padx=2, pady=pady)

        image_path = os.path.join(APPLICATION_PATH, "folder_small.png")
        image = Image.open(image_path)
        self.folder_icon = ImageTk.PhotoImage(image)
        folder_btn = Button(self.frame,
                            borderwidth=btn_bdw,
                            image=self.folder_icon,
                            bg=bg_color,
                            command=self.open_folder,
                            highlightthickness=0,
                            highlightbackground='white'
                            )

        folder_btn.grid(row=0, column=3, padx=2, pady=pady, sticky=W)


    def settings(self):
        self.gui.action_frame.frame.destroy()
        self.gui.action_frame = Settings(self.root, self.configuration, self.gui)

    def back(self):
        self.gui.action_frame.destroy()
        Settings(self.root, self.configuration, self.gui)

    def close_program(self):
        self.root.quit()

    def open_folder(self):
        if not self.configuration.dict['superfolder']:
            messagebox.showerror("Masterordner Fehler",
                                   ("Sie haben noch keinen Masterordner festgelegt." +
                                    ' Bitte setzen Sie den entsprechenden Ordner unter Einstellungen.'))
            return
        subprocess.call(['open', '-R', self.configuration.dict['superfolder']])
        pass

    def new_customer(self):
        self.gui.action_frame.frame.destroy()
        self.gui.action_frame = NewCustomer(self.root, self.configuration, self.gui)
        pass

    def new_project(self):
        self.gui.action_frame.frame.destroy()
        self.gui.action_frame = NewProject(self.root, self.configuration, self.gui)
        pass


class ActionFrame(object):
    def __init__(self, root, configuration, gui, settings=False):
        self.btn_w = 30
        self.btn_h = 2
        self.gui = gui
        self.frame = Frame(root, width=gui_width, height=300, bg=bg_color, bd=3)
        if not settings:
            self.frame.grid(row=2, column=0, pady=15, padx=15, sticky=W)
        else:
            self.frame.grid(row=2, column=0, pady=5, padx=15)
        self.configuration = configuration
        self.root = root
        pass

    def customers_ordered(self):
        customers_dict = OrderedDict(sorted(self.configuration.database.dict['customers'].items()))
        return customers_dict.keys()


class ProjectCreated(ActionFrame):
    def __init__(self, root, configuration, gui, customer_name, project_name):
        self.name = 'project_created'
        super(ProjectCreated,self).__init__(root, configuration, gui)
        project_created_label = Label(self.frame, bg=bg_color,
                                      text='Das Projekt wurde erfolgreich angelegt.', fg=font_color)
        project_created_label.grid(row=0, columnspan=2, padx=2, pady=1)
        customer_label = Label(self.frame, bg=bg_color,
                                      text='Kunde: ' + customer_name, fg=font_color)
        customer_label.grid(row=1, column=0, padx=2, pady=1, sticky=W)
        customer_number = Label(self.frame, bg=bg_color,
                               text='Kundennummer: '
                                    + configuration.database.dict['customers'][customer_name]['index'], fg=font_color)
        customer_number.grid(row=1, column=1, padx=2, pady=1, sticky=W)
        project_label = Label(self.frame, bg=bg_color,
                               text='Projekt: ' + project_name, fg=font_color)
        project_label.grid(row=2, column=0, padx=2, pady=1, sticky=W)
        project_number = Label(self.frame, bg=bg_color,
                                text='Projektnummer: '
                                     + configuration.database.dict['customers'][customer_name]['projects'][project_name]['index'],
                                fg=font_color)
        project_number.grid(row=2, column=1, padx=2, pady=1, sticky=W)


class Settings(ActionFrame):
    def __init__(self, root, configuration, gui):
        self.name = 'settings'

        super(Settings, self).__init__(root, configuration, gui, settings=True)

        folder_btn = Button(self.frame, width=self.btn_w, height=self.btn_h, bg=btn_bg_color,
                            text='Kundenverzeichnis setzen', command=self.set_folder)
        folder_btn.grid(row=0, column=0, padx=2, pady=5)

        standard_import_btn = Button(self.frame, width=self.btn_w, height=self.btn_h, bg=btn_bg_color,
                            text='Standard Importordner setzen', command=self.set_import_folder)
        standard_import_btn.grid(row=1, column=0, padx=2, pady=5)


        actualize_db_btn = Button(self.frame, width=self.btn_w, height=self.btn_h, bg=btn_bg_color,
                                     text='Kundenverzeichnis neu einlesen', command=self.actualize_db)
        actualize_db_btn.grid(row=2, column=0, padx=2, pady=5)

        set_subfolder_btn = Button(self.frame, width=self.btn_w, height=self.btn_h, bg=btn_bg_color,
                                  text='Unterordner (inaktiv) setzen', command=self.set_subfolder)
        set_subfolder_btn.grid(row=3, column=0, padx=2, pady=5)



    def actualize_db(self):
        self.configuration.database.reset_database()
        self.import_database_structure(self.configuration.dict['superfolder'])

    def set_db(self):
        directory = filedialog.askdirectory()
        if directory:
            try:
                self.configuration.change_database_location(directory)
            except:
                messagebox.showerror("Open Source File", "Failed to read directory \n'%s'" % directory)

    def set_subfolder(self):
        directory = filedialog.askdirectory()
        if directory:
            directory = Path(directory)
            if not directory.is_dir():
                messagebox.showerror("Not a directory", "'%s'" % directory)
                return
            directory = Path(directory).name
            try:
                self.configuration.set_subfolder(directory)
            except:
                messagebox.showerror("Open Source File", "Failed to read directory \n'%s'" % directory)

    def set_folder(self):
        dir_opt = options = {}
        directory = filedialog.askdirectory()
        if directory:
            self.configuration.set_superfolder(directory)
            self.configuration.change_database_location(directory)
            # self.import_database_structure(directory)

    def set_import_folder(self):
        dir_opt = options = {}
        directory = filedialog.askdirectory()
        if directory:
            try:
                self.configuration.set_import_folder(directory)
            except:
                messagebox.showerror("Open Source File", "Failed to read directory \n'%s'" % directory)

    def choose_import_directory(self):
        dir_opt = options = {}
        directory = filedialog.askdirectory()
        if directory:
            try:
                self.import_database_structure(directory)
            except:
                messagebox.showerror("Open Source File", "Failed to read directory \n'%s'" % directory)

    def import_database_structure(self, startpath):
        startpath = Path(startpath)
        subfolder_full_path = startpath / self.configuration.dict["extra_subfolder"]

        for i, dir_to_iter in enumerate([subfolder_full_path, startpath]):
            for dir in dir_to_iter.iterdir():
                if not dir.is_dir():
                    continue
                in_subfolder = i == 0

                customer_index = dir.name[:3]
                customer_name = dir.name[4:]

                if customer_index.isdigit():
                    self.configuration.database.new_customer_from_path(int(customer_index),
                                                                       customer_name,
                                                                       in_subfolder=in_subfolder)
                    # print('Kundenname: {}'.format(customer_name))
                    # print('Kundenindex: {}'.format(customer_index))
                    for subdir in dir.iterdir():
                        if not subdir.is_dir():
                            continue
                        project_index = subdir.name[4:7]
                        project_name = subdir.name[8:]
                        if project_index.isdigit() and subdir.name[:3] == self.configuration.database.dict['customers'][customer_name]['index']:
                            self.configuration.database.new_project_from_path(customer_name,
                                                                              int(project_index),
                                                                              project_name,
                                                                              )
        print("number customers: ", len(self.configuration.database.dict["customers"]))


class NewCustomer(ActionFrame):

    def __init__(self, root, configuration, gui):
        self.name = 'new customer'
        super(NewCustomer, self).__init__(root, configuration, gui)

        new_customer_lbl = Label(self.frame, fg=font_color,
                                 text='Kundenname:')
        new_customer_lbl.grid(row=0, column=0, padx=2, pady=10, sticky=W)
        self.e = Entry(self.frame)
        self.e.grid(row=0, column=1, padx=20, pady=10, sticky=W)
        btn = Button(self.frame, bg=btn_bg_color, text='Kunden anlegen',
                     command=self.new_customer, fg = font_color)
        btn.grid(row=1, column=0, padx=2, pady=15, sticky=W)

    def new_customer(self):
        customer_name = self.e.get()
        customer = self.configuration.database.new_customer(customer_name)
        if not customer:
            messagebox.showerror("Kundennamen Fehler",
                                   ("Es existiert bereits ein Kunde mit dem Namen \n'%s'" % customer_name))
            return
        self.gui.action_frame.frame.destroy()
        self.gui.action_frame = NewProject(self.root, self.configuration, self.gui, customer_name=customer_name)


class NewProject(ActionFrame):

    def __init__(self, root, configuration, gui, customer_name=None):
        self.name = 'new project'
        super(NewProject, self).__init__(root, configuration, gui)

        self.project_name = ''
        self.customer_name = customer_name

        if customer_name is not None:
            self.fixed_customer = True
        else:
            self.fixed_customer = False
        self.project_folder_src_dir = self.configuration.dict['import_folder']
        self.project_folder_empty = IntVar()

        self.customers_list = self.customers_ordered()
        self.customer_dialog()

        self.project_dialog()


    def customer_dialog(self):

        if self.customer_name is not None:
            customer_lbl = Label(self.frame, bg="white", text='Kunde: ' + self.customer_name)
            customer_lbl.grid(row=0, column=0, padx=2, pady=10, sticky=W)

        elif self.customer_name is None:
            customer_sel = Label(self.frame, bg="white", text='Kundenauswahl')
            customer_sel.grid(row=0, column=0, padx=2, pady=10, sticky=W)

            self.customer_menu()

    def customer_menu(self):
        self.menu = AutocompleteCombobox(self.frame)
        self.menu.set_completion_list(self.customers_list)

        self.menu.grid(row=0, column=1, padx=2, pady=10, sticky=W)

    def project_dialog(self):

        self.entry_dialog()

        self.check_buttons()

        self.btn = Button(self.frame, bg=btn_bg_color, text='Projekt anlegen',fg=font_color,
                          command=self.new_project)

        self.btn.grid(row=7, column=0, padx=2, pady=10, sticky=W)


    def display_directory(self):

        if self.project_folder_src_dir:
            self.folder_label = Label(self.frame, bg=bg_color, text=self.project_folder_src_dir,
                                      fg=font_color)
            self.folder_label.grid(row=6, columnspan=2, padx=2, pady=10, sticky=W)

    def entry_dialog(self):
        self.new_project_lbl = Label(self.frame, bg="white", text='Projektname:')
        self.new_project_lbl.grid(row=1, column=0, padx=2, pady=10, sticky=W)

        self.e = Entry(self.frame)
        self.e.grid(row=1, column=1, padx=2, pady=10, sticky=W)

    def project_folder(self):
        directory = filedialog.askdirectory()

        if directory:
            try:
                self.project_folder_src_dir = directory
                self.display_directory()
            except:
                messagebox.showerror("Open Source Folder", "Failed to read directory \n'%s'" % directory)

    def check_buttons(self):

        c = Checkbutton(self.frame, text="Projektordner leer anlegen",
                        bg='white', variable=self.project_folder_empty,
                        borderwidth=0,
                        )

        c.grid(row=2, column=0, padx=10, pady=5, sticky=W)

    def new_project(self):
        if not self.fixed_customer:
            self.customer_name = self.menu.get()
        self.project_name = self.e.get()

        if self.wrong_input():
            return

        customer_found = self.configuration.database.customer_activity_change(self.customer_name)
        if not customer_found:
            messagebox.showerror('Kundenordner nicht gefunden!')
        project = self.configuration.database.new_project(self.customer_name, self.project_name)



        if self.project_folder_empty.get() == 1:
            create_empty_dir(project.dict['folder'])
        else:
            copy_directory(self.project_folder_src_dir, project.dict['folder'])

        self.gui.action_frame.frame.destroy()
        self.gui.action_frame = ProjectCreated(self.root, self.configuration, self.gui, self.customer_name, self.project_name)


    def wrong_input(self):

        if not self.configuration.database.dict['customers'].get(self.customer_name):
            messagebox.showerror('Kundenname falsch',
                                   'Der eingegebene Kunde existiert noch nicht.' +
                                   ' Bitte wählen Sie einen existierenden Namen aus oder legen Sie einen neuen Kunden an.')
            return True

        if not self.configuration.dict['superfolder']:
            messagebox.showerror("Masterordner Fehler", 'Sie haben noch keinen Pfad für die Datenbank gesetzt. ' +
                                                          'Bitte setzen Sie diesen unter Einstellungen.')
            return True

        if self.customer_name is None:
            messagebox.showerror('Kundenname fehlt', 'Bitte wählen Sie einen Kunden aus!')
            return True

        try:
            os.listdir(self.configuration.dict['import_folder'])
        except OSError:
            messagebox.showerror("Import Ordner Fehler", ("Der Import Ordner \n'%s'" % self.configuration.dict['import_folder']) +
                                   '\n kann nicht gefunden werden.')
            return True

        if self.configuration.database.dict['customers'][self.customer_name]['projects'].get(self.project_name):
            messagebox.showerror("Projektname Fehler", ("Der Projektname \n'%s'" % self.project_name) +
                                   '\n existiert bereits. Bitte wählen Sie einen anderen Namen.')
            return True

        if self.project_name is None or self.project_name == '':
            messagebox.showerror("Projektname fehlt", 'Bitte geben Sie einen Projektnamen ein!')
            return True

        if self.project_folder_empty.get() == 0 and self.project_folder_src_dir is None:
            messagebox.showerror("Import Ordner Fehler",
                                   'Bitte legen Sie in den Einstellungen einen Importordner fest!')
            return True
        return False

    def actualize_customer(self, customer):
        self.customer_name = customer


__main__()