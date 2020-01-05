import os
from pathlib import Path

from tmp.util import nr2str


class Customer:

    def __init__(self, name, customer_index, subfolder=None):
        customer_folder = nr2str(customer_index) + ' ' + name
        if subfolder is not None:
            rel_folder = os.path.join(subfolder, customer_folder)
        else:
            rel_folder = customer_folder
        self.dict = {'name': name,
                     'index': nr2str(customer_index),
                     'rel_folder': rel_folder ,
                     'projects': {},
                     'project_index': 0,
                     'subfolder': subfolder is not None
                     }

class Project:

    def __init__(self, project_name, customer_name, superfolder, database):

        customer_index = database['customers'][customer_name]['index']
        project_index = customer_index + '-' + nr2str(database['customers'][customer_name]['project_index'])
        customer_folder = database['customers'][customer_name]['rel_folder']
        project_folder_name = project_index + ' ' + project_name
        superfolder = Path(superfolder)
        self.dict = {'name': project_name,
                     'index': nr2str(project_index),
                     'customer_name': customer_name,
                     'customer_index': customer_index,
                     'folder': str(superfolder / customer_folder / project_folder_name)
                     }
