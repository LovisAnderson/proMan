import json
from tmp.customer_project import Customer, Project
import shutil
import os
from os.path import expanduser
from tmp.util import nr2str


class Database():
    def __init__(self, configuration):
        self.path = os.path.abspath(configuration.dict['database'])
        self.dict = self.load_database()
        self.superfolder = configuration.dict['superfolder']
        self.subfolder = configuration.dict["extra_subfolder"]

    def load_database(self):
        if os.path.exists(self.path):

            print(f'load database from {self.path}')
            with open(self.path) as path:
                dict = json.load(path)
            return dict
        else:
            print('new database')
            self.new_database()
            self.save()
            return self.dict

    def new_database(self):
        self.dict = {'customers': {},
                     'customer_index': 0
                    }

    def save(self):
        with open(self.path, 'w') as outfile:
            json.dump(self.dict, outfile, indent=4)

    def new_customer(self, customer_name):
        if self.dict['customers'].get(customer_name) is not None:
            return False
        self.dict['customer_index'] += 1
        new_customer = Customer(customer_name, self.dict['customer_index'])
        self.dict['customers'][customer_name] = new_customer.dict
        self.save()
        return True

    def new_customer_from_path(self, customer_index, customer_name, in_subfolder=False):
        if self.dict['customers'].get(customer_name) is not None:
            return False
        if self.dict['customer_index'] < customer_index:
            self.dict['customer_index'] = customer_index
        if in_subfolder:
            subfolder = self.subfolder
        else:
            subfolder = None
        new_customer = Customer(customer_name, customer_index, subfolder=subfolder)
        self.dict['customers'][customer_name] = new_customer.dict
        self.save()
        return True

    def new_project(self, customer_name, project_name):
        if self.dict['customers'][customer_name]['projects'].get(project_name):
            return False
        self.dict['customers'][customer_name]['project_index'] += 1
        new_project = Project(project_name, customer_name, self.superfolder, self.dict)

        self.dict['customers'][customer_name]['projects'][project_name] = new_project.dict
        self.save()
        return new_project

    def new_project_from_path(self, customer_name, project_index, project_name):
        if self.dict['customers'][customer_name]['projects'].get(project_name):
            print(f'Project with name {project_name} already exists.')
            project_name = project_name + str(project_index)
        if self.dict['customers'][customer_name]['project_index'] < project_index:
            self.dict['customers'][customer_name]['project_index'] = project_index
        new_project = Project(project_name, customer_name, self.superfolder, self.dict)
        self.dict['customers'][customer_name]['projects'][project_name] = new_project.dict
        self.save()
        return new_project

    def reset_database(self):
        self.new_database()
        self.save()

    def customer_activity_change(self, customer_name):
        'Returns True if customer folder is found'
        customer = self.dict['customers'][customer_name]
        customer_folder_name = nr2str(customer['index']) + ' ' + customer['name']
        if os.path.exists(os.path.join(self.superfolder,
                                       self.dict['customers'][customer_name]['rel_folder'])):
            return True
        if self.dict['customers'][customer_name]['subfolder']:
            superfolder_customer = os.path.join(self.superfolder, customer_folder_name)
            if not os.path.exists(superfolder_customer):
                return False
            self.dict['customers'][customer_name]['subfolder'] = False
            self.dict['customers'][customer_name]['rel_folder'] = customer_folder_name
            self.save()
            return True
        else:
            folder = os.path.join(self.subfolder, customer_folder_name)
            if not os.path.exists(folder):
                return False
            self.dict['customers'][customer_name]['subfolder'] = True
            self.dict['customers'][customer_name]['rel_folder'] = os.path.join(self.subfolder, customer_folder_name)
            self.save()


class Configuration():

    def __init__(self):
        home = expanduser("~")
        self.path = os.path.join(home, '.promanCFG.json')

        self.dict, save_config = self.get_configure_file()
        print('config file', self.path)
        if save_config:
            self.save()
        self.database = Database(self)
        pass

    def get_configure_file(self):
        if os.path.exists(self.path):
            with open(self.path) as path:
                dict = json.load(path)
                if dict.get('extra_subfolder') is None:
                    dict['extra_subfolder'] = '! INAKTIVE KUNDEN & LEADS'
                    save_config = True
                else:
                    save_config = False
            return dict, save_config
        else:
            print('new config')
            save_config = True
            config = self.new_configuration()
            return config, save_config

    def new_configuration(self):
        home = expanduser("~")
        db_path = os.path.join(home, '.database.json')
        with open(self.path, 'w') as outfile:
            json.dump({}, outfile, indent=4)
        return {'superfolder': None,
                'import_folder': None,
                'extra_subfolder': '! INAKTIVE KUNDEN & LEADS',
                'database': db_path
                }

    def change_database_location(self, folder):
        src = self.database.path
        des = os.path.join(folder, 'database.json')
        self.dict['database'] = des
        self.save()
        self.database.path = des
        shutil.move(src, des)

    def save(self):
        with open(self.path, 'w') as outfile:
            json.dump(self.dict, outfile, indent=4)

    def set_superfolder(self,directory):
        self.dict['superfolder'] = directory
        self.database.superfolder = directory
        self.save()

    def set_subfolder(self,directory):
        self.dict['extra_subfolder'] = directory
        self.database.subfolder = directory
        self.save()

    def set_import_folder(self,directory):
        self.dict['import_folder'] = directory
        self.save()
        pass
