"""
This task is the implementation phase of the WGUPS Routing Program.

The Western Governors University Parcel Service (WGUPS) needs to determine an efficient route and delivery distribution for 
their daily local deliveries (DLD) because packages are not currently being consistently delivered by their promised deadline. 
The Salt Lake City DLD route has three trucks, two drivers, and an average of 40 packages to deliver each day. Each package has 
specific criteria and delivery requirements that are listed in the attached “WGUPS Package File.”

Your task is to determine an algorithm, write code, and present a solution where all 40 packages will be delivered on time 
while meeting each package’s requirements and keeping the combined total distance traveled under 140 miles for all trucks. 
The specific delivery locations are shown on the attached “Salt Lake City Downtown Map,” and distances to each location are 
given in the attached “WGUPS Distance Table.” The intent is to use the program for this specific location and also for many 
other cities in each state where WGU has a presence. As such, you will need to include detailed comments to make your code 
easy to follow and to justify the decisions you made while writing your scripts.

The supervisor should be able to see, at assigned points, the progress of each truck and its packages by any of the variables 
listed in the “WGUPS Package File,” including what has been delivered and at what time the delivery occurred.

"""

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



Reset:
Bundle by time slots. No- increment time variable?  


"""
import pandas as pd
# Launch time, 8am

# SECTION A - Hash Table + Insert Function
array_size = 10
package_table = [None] * array_size
truck_list = [[], [], []]

def hash_func(pid):
    return hash(pid) % array_size

def insert(pid, address, deadline, city, zip, expected_time, weight, status):
    key = hash_func(pid)
    if package_table[key] != None:
        resize()

    # change to flat array? no object?
    package_table[key] = Package(pid, address, deadline, city, zip, expected_time, weight, status)

def resize():
    global array_size, package_table

    array_size = array_size * 2
    temporary_table = [None] * array_size
    for i in range(int(array_size/2)):
        if package_table[i] == None: 
            continue
        temporary_table[hash_func(package_table[i].pid)] = package_table[i]

    package_table = temporary_table

# SECTION B - Lookup Function with Package ID: Connects to class .toString()
def lookup(pid):
    global package_table
    return f"{package_table[hash_func(pid)]}"


# Cycles through current package list. One loop to find specific truck requirements, second for FCFS package filler
# places package ID into Truck inner list
def package_truck_filtering(): # Just an initial...?
    global package_table, truck_list
    
    def truck_loading(truck_number, package_index):
        truck_list[truck_number].append(package_table[package_index])
        package_table[package_index].current_truck = truck_number
        # package_table[package_number].status = 'En Route' --------- ADD WHEN DEPARTING TRUCK
    
    # loads first two trucks with time sensitive
    flip_tracker = 0
    for i in range(len(package_table)):
        if package_table[i] == None: continue
        if package_table[i].expected_time == None or package_table[i].status == 'nan': continue
        if package_table[i].status == "Delivered" or str(package_table[i].status)[0:7] == 'Delayed': continue
        truck_loading(int(flip_tracker), i)
        if flip_tracker == 0: flip_tracker = 1
        else: flip_tracker = 0

    # Loads truck-specific packages
    for i in range(len(package_table)):
        if package_table[i] == None: continue
        if package_table[i].status[0:5] == 'Truck':
            truck_number = int(package_table[i].status[-1:])
            # no collision or overflow handling
            truck_loading(truck_number-1, i)

    # Loads package pairings
    # Loads initial pacakge
    temp_attached_packages = []
    for i in range(len(package_table)):
        if package_table[i] == None: continue
        # loop through all packges for attached_packages
        # combine all arrays, store into smallest number
        # call function below with new array
        
        # Only checks one instance of a package pair list. not different sets
        temp_attached_packages.extend(package_table[i].attached_packages)


    # Loops to match all paired packages to same truck
    temp_attached_packages = list(set(temp_attached_packages))
    pivot = package_table[temp_attached_packages.pop()]
    for package in temp_attached_packages:
        indx = hash_func(package)

        # remove all packages from respective truck
        if package_table[indx].current_truck != None: 
            for i in range(len(truck_list[package_table[indx].current_truck])):
                if truck_list[package_table[indx].current_truck][i] == package_table[indx]:
                    truck_list[package_table[indx].current_truck].pop(i)
                    break
            
        # match tracking to pivot
        package_table[indx].current_truck = pivot.current_truck

        # add all trucks to pivot truck
        truck_loading(pivot.current_truck, indx)

            # break? cut out all current iteration of checked numbers


    return None

# Takes truck package list, sorts by distance from warehouse, then closest after each package
# Time calculated and set into delivery status
# CORRECTION: based on time driver gets into truck. Wait to call function until driver is allocated???
# MUST be in order of time incrementation
def route_sorting():
    global truck_list
    distance_df = pd.read_csv('WGUPS Distance Table')
    
    # mark all packages as en route
    # time calculations
    return None        

# What was my final goal again....?


def package_table_import(file):
    df = pd.read_csv(file)
    for i in range(len(df)):
        insert(df.iloc[i].iat[0], df.iloc[i].iat[1], df.iloc[i].iat[2], df.iloc[i].iat[3], df.iloc[i].iat[4], df.iloc[i].iat[5], df.iloc[i].iat[6], df.iloc[i].iat[7])



        




class Package:
    def __init__(self, pid, address, deadline, city, zip, expected_time, weight, status = 'Warehouse'):
        self.pid = int(pid)
        self.address = address
        self.deadline = deadline
        self.city = city
        self.zip = zip
        self.expected_time = expected_time
        self.weight = weight
        self.status = str(status)
        self.delivery_time = [None, None]
        self.current_truck = None
        self.attached_packages = []
        if expected_time == "EOD": self.expected_time = None
        if status == 'nan': self.status = None
        self.package_attachment()

    def package_attachment(self):
        if self.status[0:7] == 'Package':
            self.attached_packages = self.status.split(", ")
            while 'Package' in self.attached_packages:
                self.attached_packages.remove('Package')
            for i in range(len(self.attached_packages)): self.attached_packages[i] = int(self.attached_packages[i])
            self.attached_packages.append(self.pid)

        
    
    def status_formatting(self):
        if self.status == None:
            return

        if self.status == 'Delivered' or self.status == 'Delayed' or self.status == 'En Route':
            return f"\nStatus: {self.status} - {self.delivery_time}"

        return f"\nStatus: {self.status}"

    def status_update(self, status, time = [None, None]):
            if time != [None, None]:
                self.delivery_time = time
            self.status = status

    def __str__(self):
        return f"=========================================\nPackage ID: {self.pid}\nAddress: {self.address}\nDeadline: {self.deadline}\nCity: {self.city}\nZip: {self.zip}\nWeight: {self.weight}{self.status_formatting()}\n========================================="

    
# class Truck:
#     def __init__(self):
#         self.packages = [None] * 16
#         self.
        
###################### Main #######################






package_table_import('WGUPS Package File.csv')
# print(lookup(14))

package_truck_filtering()

# for package in package_table[hash_func(14)].attached_packages:
#     print(package)

for truck in truck_list:
    print("=======Truck=======")
    for i in range(len(truck)):
        print(truck[i].pid)