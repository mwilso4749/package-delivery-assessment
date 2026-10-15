"""

C1. Student ID commented in
C2. Include comments in code to explain process and flow 

D1. 

Hash Table
- Package ID as key
- address
- deadline
- city
- zip code
- package weight
- delivery status (i.e., at the hub, en route, delivered, ...)
-     *you may need to create additional statuses
- actual delivery time

•  Each truck can carry a maximum of 16 packages, and the ID number of each package is unique.
•  The trucks travel at an average speed of 18 miles per hour and have an infinite amount of gas with no need to stop.
•  There are no collisions.
•  Three trucks and two drivers are available for deliveries. Each driver stays with the same truck as long as that truck is in service.
•  Drivers leave the hub no earlier than 8:00 a.m., with the truck loaded, and can return to the hub for packages if needed.
•  The delivery and loading times are instantaneous (i.e., no time passes while at a delivery or when moving packages to a truck at the hub). This time is factored into the calculation of the average speed of the trucks.
•  There is up to one special note associated with a package.
•  The delivery address for package #9, Third District Juvenile Court, is wrong and will be corrected at 10:20 a.m. WGUPS is aware that the address is incorrect and will be updated at 10:20 a.m. However, WGUPS does not know the correct address (410 S. State St., Salt Lake City, UT 84111) until 10:20 a.m.
•  The distances provided in the “WGUPS Distance Table” are equal regardless of the direction traveled.
•  The day ends when all 40 packages have been delivered.


"""
##############################################################################
"""
PLANNING
Arraylist of dictionaries using key lookup?

•   delivery address
•   delivery deadline
•   delivery city
•   delivery zip code
•   package weight
•   delivery status (i.e., delayed, at the hub, en route, or delivered), including the delivery time


Time variable


hash_table_load_from_csv func

time_sheet_generation func (handles truck-specific checks; 16 max per; change each package status)
    truck1 
        - load packages based on requirement first, then backfill
        - simple sort- find closest package address, then loop through and find next closest, sorting by distance
        - mark time starting at [0], add distance time to each pacakge expected time
    truck2
    truck3





"""
import pandas as pd

array_size = 10
package_table = [None] * array_size



def hash_func(pid):
    return hash(pid) % array_size

def insert(pid, address, deadline, city, zip, weight):
    key = hash_func(pid)
    if package_table[key] != None:
        resize()

    # change to flat array? no object?
    package_table[key] = Package(pid, address, deadline, city, zip, weight)

def resize():
    global array_size, package_table

    array_size = array_size * 2
    temporary_table = [None] * array_size
    for i in range(int(array_size/2)):
        if package_table[i] == None: 
            continue
        temporary_table[hash_func(package_table[i].pid)] = package_table[i]

    package_table = temporary_table


# Cycles through current package list. One loop to find specific truck requirements, second for FCFS package filler
# places package ID into Truck inner list
def package_truck_filtering():
    return None

# Takes truck package list, sorts by distance from warehouse, then closest after each package
# Time calculated and set into delivery status
# CORRECTION: based on time driver gets into truck. Wait to call function until driver is allocated???
def route_sorting():
    distance_df = pd.read_csv('WGUPS Distance Table')
    return None        

# What was my final goal again....?


def package_table_import(file):
    df = pd.read_csv(file)
    for i in range(len(df)):
        insert(df.iloc[i].iat[0], df.iloc[i].iat[1], df.iloc[i].iat[2], df.iloc[i].iat[3], df.iloc[i].iat[4], df.iloc[i].iat[5])



        



    
class Package:
    def __init__(self, pid, address, deadline, city, zip, weight):
        self.pid = pid
        self.address = address
        self.deadline = deadline
        self.city = city
        self.zip = zip
        self.weight = weight
        self.status = 'warehouse'
        



###################### Main #######################






package_table_import('WGUPS Package File.csv')
print("finished")