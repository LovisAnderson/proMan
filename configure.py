import json
from customer_project import Customer, Project
import shutil
from pathlib import Path
from util import nr2str


class Database():
    def __init__(self, configuration):
        self.path = Path(configuration.dict['database'])
        self.dict = self.load_database()
        self.superfolder = configuration.dict['superfolder']
        self.subfolder = configuration.dict["extra_subfolder"]

    def load_database(self):
        if self.path.exists():

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

    def reactivate_customer(self, customer_name):
        """
        Method checks if customer has a folder in subfolder. If yes it returns True and False otherwise
        Otherwise it looks if customer has a folder in subfolder
        """
        customer = self.dict['customers'][customer_name]

        customer_folder_name = nr2str(customer['index']) + ' ' + customer['name']

        if self.dict['customers'][customer_name]['subfolder']:

            self.dict['customers'][customer_name]['subfolder'] = False
            self.dict['customers'][customer_name]['rel_folder'] = customer_folder_name
            self.save()
            if (Path(self.superfolder) / f'{self.subfolder}/{customer_folder_name}').exists():
                # If the folder does not exist it has been moved by hand and the corresponding entry in database has
                # not yet been updated
                return True
        else:
            folder = Path(self.superfolder) / f'{self.subfolder}/{customer_folder_name}'
            if folder.exists():
                return True
        return False


class Configuration:

    def __init__(self, debug=False):
        self.debug = debug
        if not debug:
            self.path = Path.home() / '.promanCFG.json'
        else:
            self.path = Path(__file__).parent / 'promanCFG_debug.json'
        self.dict, save_config = self.get_configure_file()
        print('config file', self.path)
        if save_config:
            self.save()
        self.database = Database(self)
        pass

    def get_configure_file(self):
        if self.path.exists():
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
        if not self.debug:
            home = Path.home()
            db_path = home / '.database.json'
        else:
            db_path = Path(__file__).parent / 'database_debug.json'
        with open(self.path, 'w') as outfile:
            json.dump({}, outfile, indent=4)
        return {'superfolder': None,
                'import_folder': None,
                'extra_subfolder': '! INAKTIVE KUNDEN & LEADS',
                'database': str(db_path)
                }

    def change_database_location(self, folder):
        src = self.database.path
        des = Path(folder) / src.name
        self.dict['database'] = str(des)
        self.save()
        self.database.path = des
        shutil.move(src, des)

    def save(self):
        with open(self.path, 'w') as outfile:
            json.dump(self.dict, outfile, indent=4)

    def set_superfolder(self, directory):
        self.dict['superfolder'] = directory
        self.database.superfolder = directory
        self.save()

    def set_subfolder(self, directory):
        self.dict['extra_subfolder'] = directory
        self.database.subfolder = directory
        self.save()

    def set_import_folder(self, directory):
        self.dict['import_folder'] = directory
        self.save()
        pass

    def create_database_from_path(self, startpath):
        startpath = Path(startpath)
        subfolder_full_path = startpath / self.dict["extra_subfolder"]
        for i, dir_to_iter in enumerate([subfolder_full_path, startpath]):
            if i == 0 and not subfolder_full_path.exists():
                continue
            for dir in dir_to_iter.iterdir():
                if not dir.is_dir():
                    continue
                in_subfolder = i == 0

                customer_index = dir.name[:3]
                customer_name = dir.name[4:]

                if customer_index.isdigit():
                    customer_in_database = self.database.dict['customers'].get(customer_name)
                    if customer_in_database is None:
                        self.database.new_customer_from_path(int(customer_index),
                                                             customer_name,
                                                             in_subfolder=in_subfolder)
                    else:
                        in_db_index = customer_in_database['index']
                        if customer_index != in_db_index:
                            raise CustomerActiveInactiveException(
                                f'Der Kunde {customer_name} wurde mehrmals gefunden mit verschiedenen Indices:'
                                f' {customer_index} und {in_db_index}')

                        self.database.dict['customers'][customer_name]['subfolder'] = in_subfolder
                    for subdir in dir.iterdir():
                        if not subdir.is_dir() or len(subdir.name) < 9:
                            continue
                        project_index = subdir.name[4:7]
                        project_name = subdir.name[8:]
                        if project_index.isdigit() and subdir.name[:3] == self.database.dict['customers'][customer_name]['index']:
                            self.database.new_project_from_path(customer_name,
                                                                int(project_index),
                                                                project_name,
                                                                )
        print("number customers: ", len(self.database.dict["customers"]))


class CustomerActiveInactiveException(Exception):
    pass