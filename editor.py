import bisect

from connection import initialize_connection
from netcommands import run_dmi, run_ip, ping_ok


wsh = initialize_connection()


class Node:
    def __init__(self, machine, asset):
        self.machine = machine
        self.asset = asset
        
    def pull_board(self):
        # Board details
        output = run_dmi(self.machine)
        self.make = output[0]
        self.model = output[1]
        self.serial = output[2]
        self.uuid = output[3]
        
    def pull_ip(self):
        self.ip = run_ip(self.machine)


def new_build(machine, asset):
    new_entry = []
    new_node = Node(machine, asset)
    
    if ping_ok(new_node.machine):
        print("Pulling Board details and IP")
        new_node.pull_board()
        new_node.pull_ip()
        
        new_entry.extend([new_node.machine, 'spare', 'A-6', \
        '', new_node.asset, '', '', new_node.ip, new_node.make, \
            new_node.model, new_node.serial, new_node.uuid])
    else:
        print("Something's wrong with the network. Won't add Board details")
        new_entry.extend([new_node.machine, 'spare', 'A-6', \
        '', new_node.asset])
        
    last_spare_row_number = wsh.find('spare')[-1].row
    wsh.update_row(last_spare_row_number + 1, new_entry)


def new_rebuild(old, rebuild):
    cells_list = wsh.find(old)
    
    if len(cells_list) > 1 or len(cells_list) < 1:
        print("It's either no such machine, or it's duplicated. Go manual")
        
    elif len(cells_list) == 1:
        row_number = cells_list[0].row
        if ping_ok(rebuild):
            print("Updating IP...")
            ip = run_ip(rebuild)
            
            wsh.update_value("A{}".format(row_number), rebuild)
            wsh.update_value("H{}".format(row_number), ip)
            
        else:
            print("Something's wrong with the network. Won't update IP...")
            wsh.update_row(row_number, [rebuild,])


def new_deploy(machine, user, location):
    # THIS function assumes that only dt-NN machines will be deployed
    cells_list = wsh.find(machine)
    
    if len(cells_list) > 1 or len(cells_list) < 1:
        print("It's either no such machine, or it's duplicated. Go manual")
        
    elif len(cells_list) == 1:
        deploy_row_number = cells_list[0].row
        # copy the row with the machine you want to deploy
        deploy_from_row = wsh.get_row(deploy_row_number)
        # find last item of dt-list
        length_of_column = wsh.find('ws', cols=(1,1))[0].row
        # get all rows
        all_rows = wsh.get_all_values()
        # get the slice from the first item to the last in the dt-list    
        dt_rows = all_rows[1:length_of_column - 1]
        
        # Find where to insert new row to maintain sorted order
        index = find_index_to_insert(dt_rows, deploy_from_row)
        dt_rows.insert(index, deploy_from_row)
        # Add 1 more row to the end of dt-list to not overlap on ws-list
        wsh.insert_rows(length_of_column - 1)
        wsh.update_values('A2', dt_rows)
        
        # Delete the row that we were deploying from
        # NB: Index shifted after adding a new row
        wsh.delete_rows(deploy_row_number + 1)
        
        # Update ip, user, loc values in the deployed row
        deployed_row = wsh.find(machine)[0].row
        
        if ping_ok(machine):
            ip = run_ip(machine)
            print("Updating IP...")
            wsh.update_value("H{}".format(deployed_row), ip)
        else:
            print("Something's wrong with the network. Won't update IP...")
        
        wsh.update_value("B{}".format(deployed_row), user)
        wsh.update_value("C{}".format(deployed_row), location)
        

def new_move(machine, user, location):
    update_row = wsh.find(machine)[0].row
    wsh.update_value("B{}".format(update_row), user)
    wsh.update_value("C{}".format(update_row), location)

################################# HELPERS

def find_index_to_insert(sorted_list, deploy_row):
    list_of_ints = []
    
    for i in range(0, len(sorted_list)):
        list_of_ints.append(int(sorted_list[i][0].split('-', 1)[1]))   
    
    result = bisect.bisect(list_of_ints, int(deploy_row[0].split('-', 1)[1]))
    
    return result
