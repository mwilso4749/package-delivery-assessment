# Launch time, 8am
total_mileage = 0


# Cycles through current package list. One loop to find specific truck requirements, second for FCFS package filler
# places package ID into Truck inner list
def package_truck_filtering():
    global package_table, truck_list

    def truck_loading(truck_number, package_index):
        truck_list[truck_number].append(package_table[package_index])
        package_table[package_index].current_truck = truck_number
        # package_table[package_number].status = 'En Route' --------- ADD WHEN DEPARTING TRUCK

    # loads first two trucks with time sensitive
    flip_tracker = 0
    for i in range(len(package_table)):
        if package_table[i] == None:
            continue
        if package_table[i].expected_time == None or package_table[i].status == "nan":
            continue
        if (
            package_table[i].status == "Delivered"
            or str(package_table[i].status)[0:7] == "Delayed"
        ):
            continue
        truck_loading(int(flip_tracker), i)
        if flip_tracker == 0:
            flip_tracker = 1
        else:
            flip_tracker = 0

    # Loads truck-specific packages
    for i in range(len(package_table)):
        if package_table[i] == None:
            continue
        if package_table[i].status[0:5] == "Truck":
            truck_number = int(package_table[i].status[-1:])
            # no collision or overflow handling
            truck_loading(truck_number - 1, i)

    # Loads package pairings
    # Loads initial pacakge
    temp_attached_packages = []
    for i in range(len(package_table)):
        if package_table[i] == None:
            continue
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
                if (
                    truck_list[package_table[indx].current_truck][i]
                    == package_table[indx]
                ):
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
def route_sorting():  # Intial only. no new time adjustments
    # Resort based on distance from eachother

    def truck_sort(truck, relative_time):
        temp_array = []

        # Sorting truck cargo based on distance only
        last_compare_value = [0, 0]
        for i in range(len(truck)):
            lowest_dist_value = 100
            lowest_index_value = None
            for k in range(len(truck)):
                # Measures least distance between each package
                distance = distance_df.iat[
                    truck[k].distance_row_col[0], last_compare_value[1]
                ]
                if str(distance) == "nan":
                    distance = distance_df.iat[
                        last_compare_value[0], truck[k].distance_row_col[1]
                    ]
                # Setting lowest package distance
                if lowest_index_value == None or lowest_dist_value > distance:
                    lowest_index_value = k
                    lowest_dist_value = distance

            travel_calc_minutes = int((lowest_dist_value / 18) * 60)
            travel_time = timedelta(
                0, 0, 0, 0, int(travel_calc_minutes % 60), int(travel_calc_minutes / 60)
            )
            truck[lowest_index_value].status = "En Route"
            relative_time = relative_time + travel_time
            truck[lowest_index_value].delivery_time = relative_time.strftime("%H:%M %p")
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


# Remove all time management with DateTime as Time import
# Move package_sorting into Truck class
# Move package_loading into Truck Classs
# Move package_truck_filtering into Truck (static?)
# TRACK TOTAL MILEAGE GLOBAL VARIABLE


"""
DELIVERY: 
- Tack current DRIVER time, add distance between packages/18 into driver.time; use with status setting
- loops through all packages, applies "status = en route" AND "departure_time = [time]" [DRIVER.TIME]
- loops through schedule and applies "status = delivered" AND "delivered_time = [time]" [DRIVER.TIME + CALCULATED TIME FROM LAST PACKAGE] ->
    - Compare package.distant_row_col to previous, milage/18
"""


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

    def insert(self, pid, object):
        key = self.hash_function(pid)
        if self.table[key] != None:
            self.resize()
        key = self.hash_function(pid)
        self.table[key] = object

    def resize(self):
        new_table = [None] * len(self.table) * 2

        for i in range(len(self.table)):
            if package_table[i] == None:
                continue
            new_table[self.hash_function(self.table[i].pid, len(self.table) * 2)] = (
                self.table[i]
            )

        self.table = new_table

    def hash_function(self, pid, size=None):  # must return the PACKAGE itself
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
        self.time[0] += int(temp_minutes / 60)
        self.time[1] = temp_minutes % 60

    def __str__(self):
        return f"{self.time[0]}:{self.time[1]}"


class Truck:
    def __init__(self):
        self.payload = []
        self.current_time = DateTime(8, 00)  # Used for delivery and

    def package_sorting(self, distance_table):  # distance table
        # sort by each pacakge distance to eachother
        table = distance_table.table
        temp_array = []

        # Sorting truck cargo based on distance only
        last_compare_value = [0, 0]
        for i in range(len(self.payload)):
            lowest_dist_value = 100
            lowest_index_value = None
            for k in range(len(self.payload)):
                # Measures least distance between each package
                distance = table[
                    self.payload[k].distance_coords[0], last_compare_value[1]
                ]
                if str(distance) == "":
                    distance = table[
                        last_compare_value[0], self.payload[k].distance_coords[1]
                    ]
                # Setting lowest package distance
                if lowest_index_value == None or lowest_dist_value > distance:
                    lowest_index_value = k
                    lowest_dist_value = distance
            last_compare_value = self.payload[lowest_index_value].distance_coordinates
            temp_array.append(self.payload.pop(lowest_index_value))
        self.payoad = temp_array

    @staticmethod
    def package_loading(truck_list, table):  # Hashtable + truck list?

        def truck_loading(truck_number, package_index):
            truck_list[truck_number].payload.append(table[package_index])
            table[package_index].current_truck = truck_number

        # loads first two trucks with time sensitive
        flip_tracker = 0
        for i in range(len(table)):
            if table[i] == None:
                continue
            if table[i].deadline == None:
                continue
            if table[i].status == "Delivered" or str(table[i].status)[0:7] == "Delayed":
                continue
            truck_loading(int(flip_tracker), i)
            if flip_tracker == 0:
                flip_tracker = 1
            else:
                flip_tracker = 0

        # Loads truck-specific packages
        for i in range(len(table)):
            if table[i] == None:
                continue
            if table[i].status[0:5] == "Truck":
                truck_number = int(table[i].status[-1:])
                # no collision or overflow handling
                truck_loading(truck_number - 1, i)

        # Loads package pairings
        # Loads initial package
        temp_attached_packages = []
        for i in range(len(table)):
            if table[i] == None:
                continue
            # Loops and collects a single list of all attached packages
            temp_attached_packages.extend(table[i].attached_packages)

        # Loops to match all paired packages to same truck
        temp_attached_packages = list(set(temp_attached_packages))
        pivot = table[temp_attached_packages.pop()]  # THIS NEEDS CHECKING #######
        for package_id in temp_attached_packages:
            index = table.hash_function(package_id)

            # remove all packages from respective truck
            if table[index].current_truck != None:
                for i in range(len(truck_list[table[index].current_truck].payload)):
                    if truck_list[table[index].current_truck][i] == table[index]:
                        truck_list[table[index].current_truck].payload.pop(i)
                        break

            # match tracking to pivot
            table[index].current_truck = pivot.current_truck

            # add all trucks to pivot truck
            truck_loading(pivot.current_truck, index)


class CSV:
    def __init__(self, file):
        self.col_label = []
        self.row_label = []
        self.table = []
        self.table_loading(file)

    def table_loading(self, file):
        with open(file) as f:
            # Column label array created
            self.col_label = f.readline().strip().split(",")

            # Places index 0 into row labels, rest into 2d table array
            for line in f:
                temporary = line.strip().split(",")
                self.row_label.append(temporary.pop(0))
                self.table.append(temporary)

            self.col_label.pop(0)
            self.row_label.pop(0)


# Used to track time between truck and return. Calculate from leave time + distance + return distance to hub /18,
# save time before switching trucks. use that time when starting next truck
class Driver:
    def __init__(self, time):
        self.time = time


# NEEDS CLEANUP BADLY
# Remove status and address. Only contain address_changes and status_changes
class Package:
    def __init__(self, pid, address, city, zip, deadline, weight, status="Warehouse"):
        # add en route time stamp
        # input for time print request different function

        self.pid = int(pid)
        # self.address = address - [DEPRICATED] use address_changes[-1][0]
        self.city = city
        self.zip = zip
        self.deadline = deadline  # convert into DateTime with str splits
        self.weight = weight
        # self.status = str(status) - [DEPRICATED] use status_changes[-1][0]

        # ===============================================

        self.expected_time = []

        # 2d array, holds status and time of IMPLEMENTATION
        self.address_changes = [[address, DateTime(8, 00)]]

        # 2d array, holds address and TIME OF IMPLEMENTATION
        self.status_changes = [[status, DateTime(8, 00)]]
        # [DEPRICATED] departure_time -> JUST USE status_changes[["en route", (THIS TIME!!)]] -> function call to retrieve departure time
        # [DEPRICATED] delivery_time -> JUST USE status_changes[["delivered", (THIS TIME!!)]] -> function call to retrieve delivery time

        self.current_truck = None  # in __str__ must have +1 to be readable
        self.attached_packages = []
        self.distance_coords = [None, None]  # [row, col]

        if deadline == "EOD":
            self.deadline = None

        self.package_attachment()

    def get_status(self):
        return self.status_changes[-1][0]

    def get_address(self):
        return self.address_changes[-1][0]

    # Fills out attached_packages with packages required to be shipped together
    def package_attachment(self):
        if self.status[0:7] == "Package":
            self.attached_packages = self.status.split("; ", ": ")
            while "Package" in self.attached_packages:
                self.attached_packages.remove("Package")
            for i in range(len(self.attached_packages)):
                self.attached_packages[i] = int(self.attached_packages[i])
            self.attached_packages.append(self.pid)

    # Formats status with time for the print statement
    def status_formatting(self):
        if self.status == None:
            return

        if (
            self.status == "Delivered"
            or self.status == "Delayed"
            or self.status == "En Route"
        ):
            return f" :: Status: {self.status} - {self.delivery_time}"

        return f" :: Status: {self.status}"

    # Change to Datetime class
    def status_update(self, status, time=[None, None]):
        if time != [None, None]:
            self.delivery_time = time
        self.status = status

    # add if check to change address of one package to old before a time
    def __str__(self):
        # , adjusted_address = self.address, adjusted_status = self.status, adjusted_time = self.time
        return f"Package ID: {self.pid} :: Address: {self.address} :: Deadline: {self.deadline} :: City: {self.city} :: Zip: {self.zip} :: Weight: {self.weight}{self.status_formatting()}"

    # add function to take time, then package (default to all) and post all reports at that time
    @staticmethod
    def time_lookup(table: HashTable, pid=None):
        time = None
        while True:
            try:
                input_time = input('Time to report (formatted "X:XX"): ')
                input_time = input_time.split(":")
                time = DateTime(int(input_time[0], int(input_time[1])))
                break
            except:
                print("Invalid time or format.")

        if pid != None:
            # time_calculation(time, pid)
            return

        for i in range(40):
            # print(time_calculation(time, hashlookup(i+1)))
            return

        def time_calculation(
            inner_time, package
        ):  # returns the adjusted string with corrected information
            # check through package status_changes array
            # inverted check- if time of implementation (status_changes[1]) > time, continue
            # return status from status_changes[0] with print statement
            # ======
            # REPEAT FOR ADDRESS (address_changes)
            return

        return

    # VALIDATE!!
    # Loop through all sets and place index values for row + col for each package
    @staticmethod
    def package_coordinate_loader(table: CSV):
        for package in table:
            if package == None:
                continue
            for i in range(len(table.row_label)):
                if package.address in table.row_label[i]:
                    package.distance_coords[0] = i
                    break
            for i in range(len(table.col_label)):
                if package.address in table.col_label[i]:
                    package.distance_coords[1] = i
                    break


# TODO:
# - move package_loading into truck class [STATIC FUNCTION]
# - move package_sorting into truck class
# - complete package.package_coordinate_loader
# - complete package.time_lookup
# - fix package.status_update...?
# - fix package.__str__
# - fix package.status_formatting with corrected variable setup and DateTime
# - add global total_mileage to each delivery (distance value)


##########################################
# MAIN OUTLINE:
##########################################

# LOOP while package not all delivered (one run instead?)

driver1, driver2 = Driver(DateTime(8, 00)), Driver(DateTime(8, 00))

distance_file = CSV("WGUPS Distance Table.csv")
package_file = CSV("WGUPS Package File.csv")
package_table = HashTable()

# Load packages into the hashtable
# Load packages with their table coordinates
# Run package association function

truck_list = [Truck(), Truck(), Truck()]
Truck.package_loading(truck_list, package_table)  # truck package loading function

# LOOP truck package sorting(truck)
# delivery(truck1, driver1)
# delivery(truck2, driver2)
# delivery(truck3, drive 1)
