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
# NO IMPORTS - csv -> csv reader
import pandas as pd
from datetime import datetime, timedelta
# Launch time, 8am

# SECTION A - Hash Table + Insert Function
# array_size = 10
# package_table = [None] * array_size
# truck_list = [[], [], []]
# truck_time = [datetime(1, 1, 1, hour=8), datetime(1, 1, 1, hour=8), datetime(1, 1, 1, hour=8)]



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
def route_sorting(): # Intial only. no new time adjustments
    global truck_list, package_table, truck_time
    distance_df = pd.read_csv('WGUPS Distance Table.csv', index_col=0)
    row_index_list = distance_df.index.tolist()
    row_columns_list = distance_df.columns.tolist()
    
    # Loop through all sets and place index values for row + col for each package
    for package in package_table:
        if package == None: continue
        for i in range(len(row_index_list)):
            if package.address in row_index_list[i]:
                package.distance_row_col[0] = i
                break
        for i in range(len(row_columns_list)):
            if package.address in row_columns_list[i]:
                package.distance_row_col[1] = i
                break

    # Resort based on distance from eachother
    
    def truck_sort(truck, relative_time):
        temp_array = []
              
        # Sorting truck cargo based on distance only
        last_compare_value = [0,0]
        for i in range(len(truck)):
            lowest_dist_value = 100
            lowest_index_value = None
            for k in range(len(truck)):
                # Measures least distance between each package
                distance = distance_df.iat[truck[k].distance_row_col[0], last_compare_value[1]]
                if str(distance) == 'nan':
                    distance = distance_df.iat[last_compare_value[0], truck[k].distance_row_col[1]]
                 # Setting lowest package distance
                if lowest_index_value == None or lowest_dist_value > distance:
                    lowest_index_value = k
                    lowest_dist_value = distance
                
            travel_calc_minutes = int((lowest_dist_value/18)*60)
            travel_time = timedelta(0, 0, 0, 0, int(travel_calc_minutes%60), int(travel_calc_minutes/60))
            truck[lowest_index_value].status = 'En Route'
            relative_time = relative_time + travel_time
            truck[lowest_index_value].delivery_time = relative_time.strftime('%H:%M %p')
            last_compare_value = truck[lowest_index_value].distance_row_col
            temp_array.append(truck.pop(lowest_index_value))

        # Change status to delivery; add in return to warehouse time?
        
        return temp_array, relative_time 
            
    for i in range(len(truck_list)):
        truck_list[i], truck_time[i] = truck_sort(truck_list[i], truck_time[i])

            

                


    # Loop through each truck
    # search with distance_df.loc[truck_list[i].address]


    # mark all packages as en route
    # time calculations
    return None        

# What was my final goal again....?





# Remove package_table_import with native CSV importer
# Remove all hash functions from above
# Remove truck_list
# Remove all time management with DateTime as Time import
# Move package_sorting into Truck class
# Move package_loading into Truck Classs



        
'''
DELIVERY: 
- Take CURRENT truck time with each time check for the following loop updates
- loops through all packages, applies "status = en route" AND "departure_time = [time]" [CURRENT TRUCK TIME]
- loops through schedule and applies "status = delivered" AND "delivered_time = [time]" [DISTANCE CALCULATED TIME] ->
    - Compare package.distant_row_col to previous, milage/18
'''
def delivery(truck):
    return truck

# ===========================
# 

    # array of all distance comparisons in a truck ???
# interface - speciifc package status at time -> all packages at time
# package all info print
# package - 2 time stamps - time of leave + arrival time
# replace all time with date_time() class


class HashTable:
    def __init__(self):
        self.table = [None] * 10
        return
    
    def insert(self, pid, object):
        key = self.hash_function(pid)
        if self.table[key] != None:
            self.resize()
        key = self.hash_function(pid)
        self.table[key] = object

    def resize(self):
            new_table = [None] * len(self.table)*2

            for i in range(len(self.table)):
                if package_table[i] == None: 
                    continue
                new_table[self.hash_function(self.table[i].pid, len(self.table)*2)] = self.table[i]
            
            self.table = new_table

    def hash_function(self, pid, size = None): # must return the PACKAGE itself
        if size == None: 
            size = len(self.table)
        return int(hash(pid) % size)

    def lookup(self, key):
        return self.table[self.hash_function(key)]

class DateTime:
    def __init__(self, hours, minutes):
        self.time = [hours, minutes]
        return
    def add(self, minutes):
        temp_minutes = minutes + self.time[1]
        self.time[0] += int(temp_minutes/60)
        self.time[1] = temp_minutes%60
    def __str__(self):
        return f'{self.time[0]}:{self.time[1]}'

# Finsh out and replace truck_list
class Truck:
    def __init__(self):
        self.payload = []
        self.current_time = DateTime(8,00) # Used for delivery and 
    def package_loading(self, package):
        return
    def package_sorting(self):
        # sort by each pacakge distance to eachother
        return


#NEEDS CLEANUP BADLY
# deadline isnt matched right
# move deadline into expected time
# drop state from import call
# set expected time to DateTime class; None otherwise
class Package:
    # Table Import Order: PID, Address, City, State, Zip, Deadline, Weight, Status
    # def __init__(self, pid, address, deadline, city, zip, expected_time, weight, status = 'Warehouse'): #INCORRECT
    def __init__(self, pid, address, city, zip, deadline, weight, status = 'Warehouse'):
        # add en route time stamp
        # input for time print request different function
        
        self.pid = int(pid)
        self.address = address
        self.city = city
        self.zip = zip
        self.deadline = deadline # convert into DateTime with str splits
        self.weight = weight
        self.status = str(status)

        # ===============================================
        
        self.expected_time = []

        # 2d array, holds status and time of IMPLEMENTATION
        self.address_changes = [[address, DateTime(8,00)]]

        # 2d array, holds address and TIME OF IMPLEMENTATION
        self.status_changes = [[status, DateTime(8,00)]] 
        # [DEPRICATED] departure_time -> JUST USE status_changes[["en route", (THIS TIME!!)]] -> function call to retrieve departure time
        # [DEPRICATED] delivery_time -> JUST USE status_changes[["delivered", (THIS TIME!!)]] -> function call to retrieve delivery time
        
        self.current_truck = None
        self.attached_packages = []
        self.distance_coords = [None, None]

        if deadline == "EOD": self.deadline = None

        self.package_attachment()

    # Fills out attached_packages with packages required to be shipped together
    def package_attachment(self):
        if self.status[0:7] == 'Package':
            self.attached_packages = self.status.split("; ", ": ")
            while 'Package' in self.attached_packages:
                self.attached_packages.remove('Package')
            for i in range(len(self.attached_packages)): self.attached_packages[i] = int(self.attached_packages[i])
            self.attached_packages.append(self.pid)

    # Formats status with time for the print statement
    def status_formatting(self):
        if self.status == None:
            return

        if self.status == 'Delivered' or self.status == 'Delayed' or self.status == 'En Route':
            return f" :: Status: {self.status} - {self.delivery_time}"

        return f" :: Status: {self.status}"

    # Change to Datetime class
    def status_update(self, status, time = [None, None]):
            if time != [None, None]:
                self.delivery_time = time
            self.status = status

    # add if check to change address of one package to old before a time
    def __str__(self): # , adjusted_address = self.address, adjusted_status = self.status, adjusted_time = self.time
        return f"Package ID: {self.pid} :: Address: {self.address} :: Deadline: {self.deadline} :: City: {self.city} :: Zip: {self.zip} :: Weight: {self.weight}{self.status_formatting()}"

    # add function to take time, then package (default to all) and post all reports at that time
    @staticmethod
    def time_lookup(time, table: HashTable, pid = None):       
        if pid != None:
            # time_calculation(time, pid)
            return

        for i in range(40):
            # print(time_calculation(time, hashlookup(i+1)))
            return

        def time_calculation(inner_time, package): # returns the adjusted string with corrected information
            # check through package status_changes array
            # inverted check- if time of implementation (status_changes[1]) > time, continue
            # return status from status_changes[0] with print statement
            # ======
            # REPEAT FOR ADDRESS (address_changes)
            return
        return


class CSV:
    def __init__(self, file):
        self.col_label = []
        self.row_label = []
        self.table = []
        self.table_loading(file)

    def table_loading(self, file):
        with open(file) as f:
            # Column label array created
            self.col_label = f.readline().strip().split(',')

            # Places index 0 into row labels, rest into 2d table array
            for line in f:
                temporary = line.strip().split(',')
                self.row_label.append(temporary.pop(0))
                self.table.append(temporary)
        




# print(lookup(14))

# package_truck_filtering()
# route_sorting()


# print(lookup(14))
# print(truck_time[0].strftime('%H:%M %p'))



#for loop inserting all packages into table instance with temp_package_table.insert(package)

# Delivery
# Truck switch into deliver after truck 1 returns


# print(Package.time_lookup(DateTime(8,30), temp_package_table))


distance_file = CSV('WGUPS Distance Table.csv')
package_file = CSV('WGUPS Package File.csv')
package_table = HashTable()


# for i in range package_file.table --------- (row_labels[i+1])
    # table = package_file.table
    # package_table.insert(package_file.row_label[i], new package(table[i][0], table[i][1], etc.....)) - [SKIP table[i][3]]




for col in distance_file.col_label:
    print(col, end=", ")



# where do I place the package location function to ad col and row info into each packge. truck? package class? (makes package class too reliant) 
# maybe just a funciton to call