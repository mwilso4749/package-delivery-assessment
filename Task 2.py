# Launch time, 8am
total_mileage = 0


# Cycles through current package list. One loop to find specific truck requirements, second for FCFS package filler
# places package ID into Truck inner list


# Takes truck package list, sorts by distance from warehouse, then closest after each package
# Time calculated and set into delivery status
# CORRECTION: based on time driver gets into truck. Wait to call function until driver is allocated???
# MUST be in order of time incrementation


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


def delivery(truck, driver):
    global total_mileage
    for i in range(len(truck.payload)):
        truck.payload[i].status_changes.append(["En Route", driver.time])

    for i in range(len(truck.payload)):
        total_mileage += truck.payload_distance[i]
        driver.time.add_minutes(int((truck.payload_distance[i] / 18) * 60))
        truck.payload[i].status_changes.append(["Delivered", driver.time])

    total_mileage += truck.payload_distance[-1]
    driver.time.add_minutes(int((truck.payload_distance[-1] / 18) * 60))
    truck.payload = []
    truck.payload_distance = []


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
            if self.table[i] == None:
                continue
            new_table[self.hash_function(self.table[i].pid, len(self.table) * 2)] = (
                self.table[i]
            )

        self.table = new_table

    def hash_function(self, pid, size=None):  # must return the PACKAGE itself
        if size == None:
            size = len(self.table)
        return hash(pid) % size

    def lookup(self, key):
        return self.table[self.hash_function(key)]


class DateTime:
    def __init__(self, hours, minutes):
        self.time = [hours, minutes]

    def __str__(self):
        minutes = str(self.time[1])
        if len(minutes) == 1:
            minutes = "0" + minutes
        return f"{self.time[0]}:{minutes}"

    def add_minutes(self, minutes):
        temp_minutes = minutes + self.time[1]
        self.time[0] += int(temp_minutes / 60)
        self.time[1] = temp_minutes % 60

    def after(self, time):
        if self.time[0] == time.time[0]:
            return self.time[1] > time.time[1]
        return self.time[0] > time.time[0]


class Truck:
    def __init__(self):
        self.payload = []
        self.payload_distance = []

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

                distance = table[self.payload[k].distance_coords[0]][
                    last_compare_value[1]
                ]
                if distance == "":
                    distance = table[last_compare_value[0]][
                        self.payload[k].distance_coords[1]
                    ]
                distance = float(distance)

                # Setting lowest package distance
                if lowest_index_value == None or lowest_dist_value > distance:
                    lowest_index_value = k
                    lowest_dist_value = distance
            self.payload_distance.append(lowest_dist_value)
            last_compare_value = self.payload[lowest_index_value].distance_coords
            temp_array.append(self.payload.pop(lowest_index_value))

        # Add final distance from last address to HUB
        distance = float(table[temp_array[-1].distance_coords[0]][0])
        if str(distance) == "":
            distance = table[0, temp_array[-1].distance_coords[1]]
        self.payload_distance.append(distance)

        self.payload = temp_array

    @staticmethod
    def package_loading(truck_list, table):  # Hashtable + truck list?
        hash_table = table
        table = table.table

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
            if (
                table[i].get_status() == "Delivered"
                or str(table[i].specifications)[0:7] == "Delayed"
            ):
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
            if table[i].specifications[0:5] == "Truck":
                truck_number = int(table[i].specifications[-1:])
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
        if temp_attached_packages != []:
            pivot = table[temp_attached_packages.pop()]  # THIS NEEDS CHECKING #######
            for package_id in temp_attached_packages:
                index = hash_table.hash_function(package_id)

                # remove all packages from respective truck
                if table[index].current_truck != None:
                    for i in range(len(truck_list[table[index].current_truck].payload)):
                        if (
                            truck_list[table[index].current_truck].payload[i]
                            == table[index]
                        ):
                            truck_list[table[index].current_truck].payload.pop(i)
                            break

                # match tracking to pivot
                table[index].current_truck = pivot.current_truck

                # add all trucks to pivot truck
                truck_loading(pivot.current_truck, index)

        for i in range(len(table)):
            if table[i].current_truck == None:
                for k in range(len(truck_list)):
                    if len(truck_list[k].payload) < 16:
                        truck_loading(k, i)
                        break


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


class Driver:
    def __init__(self, time: DateTime):
        self.time = time


class Package:
    def __init__(self, pid, address, city, zip, deadline, weight, status="Warehouse"):
        self.pid = int(pid)
        self.city = city
        self.zip = zip
        self.deadline = deadline
        self.weight = weight
        self.specifications = ""

        # 2d array, holds status and time of IMPLEMENTATION
        self.address_changes = [[address, DateTime(8, 00)]]

        # 2d array, holds address and TIME OF IMPLEMENTATION
        if status == "":
            status = "Warehouse"
        if (
            "Delayed" in status
            or "Truck" in status
            or "Package" in status
            or "Incorrect" in status
        ):
            self.specifications = status
            status = "Warehouse"
        self.status_changes = [[status, DateTime(8, 00)]]

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
        if "Package" in self.specifications:
            temp = self.specifications.replace(": ", "; ").split("; ")
            self.attached_packages = temp
            while "Package" in self.attached_packages or '"' in self.attached_packages:
                self.attached_packages.remove("Package")
            for i in range(len(self.attached_packages)):
                self.attached_packages[i] = int(self.attached_packages[i])
            self.attached_packages.append(self.pid)

    # add if check to change address of one package to old before a time
    def __str__(self):
        def status_formatting():
            status = self.get_status()
            if status[0:9] == "Delivered" or status[0:8] == "En Route":
                return f" | Status: {status} - {self.status_changes[-1][1]} | On Truck: {self.current_truck + 1}"
            return f" | Status: {status}"

        return f"Package ID: {self.pid} | Address: {self.address_changes[-1][0]} | Deadline: {self.deadline} | City: {self.city} | Zip: {self.zip} | Weight: {self.weight}{status_formatting()}"

    # add function to take time, then package (default to all) and post all reports at that time
    @staticmethod
    def time_lookup(table: HashTable, pid=None):
        hash_table = table
        table = table.table

        def time_calculation(inner_time, package):
            address = ""
            status = ""
            truck = ""
            for i in range(len(package.address_changes)):
                if package.address_changes[i][1].after(inner_time):
                    continue
                address = package.address_changes[i][0]
                break

            for i in range(len(package.status_changes)):
                if package.status_changes[i][1].after(inner_time):
                    continue
                status = package.status_changes[i][0]
                if status[0:9] == "Delivered" or status[0:8] == "En Route":
                    status = f" | Status: {status} - {package.status_changes[i][1]} | On Truck: {package.current_truck + 1}"
                else:
                    status = f" | Status: {status}"
                break

            if package.current_truck != "":
                truck = f" | Truck: {package.current_truck + 1}"
            # String Formatting with TIME

            full_string = f"Package ID: {package.pid} | Address: {address} | Deadline: {package.deadline} | City: {package.city} | Zip: {package.zip} | Weight: {package.weight}{truck}{status}"
            return full_string

        time = None
        while True:
            try:
                input_time = input('Time to report (formatted "X:XX"): ')
                input_time = input_time.split(":")
                time = DateTime(int(input_time[0]), int(input_time[1]))
                break
            except:  # noqa: E722
                print("Invalid time or format.")
        barrier = f"===================================  {time}  ==================================="
        print(barrier)
        if pid != None:
            print(time_calculation(time, table[pid]))
        else:
            for i in range(40):
                temp = hash_table.lookup(i)
                print(time_calculation(time, temp))
        print(barrier)

    # Loop through all sets and place index values for row + col for each package
    @staticmethod
    def package_coordinate_loader(table, data_table: CSV):
        for package in table.table:
            if package == None:
                continue
            for i in range(len(data_table.row_label)):
                if package.address_changes[-1][0] in data_table.row_label[i]:
                    package.distance_coords[0] = i
                    break
            for i in range(len(data_table.col_label)):
                if package.address_changes[-1][0] in data_table.col_label[i]:
                    package.distance_coords[1] = i
                    break


def package_loading(table: HashTable, file: CSV):
    for i in range(len(file.table)):
        package_row = file.table[i]
        table.insert(
            int(file.row_label[i]),
            Package(
                int(file.row_label[i]),
                package_row[0],
                package_row[1],
                package_row[3],
                package_row[4],
                package_row[5],
                package_row[6],
            ),
        )


# TODO:
# - complete package.time_lookup
# - fix package.status_formatting with corrected variable setup and DateTime
# - add global total_mileage to each delivery (distance value)
# - add re-check for new address updates and distances/coordinates on table


##########################################
# MAIN OUTLINE:
##########################################

# LOOP while package not all delivered (one run instead?)

driver1, driver2 = Driver(DateTime(8, 00)), Driver(DateTime(8, 00))

distance_file = CSV("WGUPS Distance Table.csv")
package_file = CSV("WGUPS Package File.csv")
package_table = HashTable()
package_loading(package_table, package_file)  # Load packages into the hashtable


# Load packages with their table coordinates
Package.package_coordinate_loader(package_table, distance_file)

# Run package association function
for i in range(len(package_table.table)):
    package_table.table[i].package_attachment()


truck_list = [Truck(), Truck(), Truck()]
Truck.package_loading(truck_list, package_table)  # truck package loading function

for i in range(len(truck_list)):  # LOOP truck package sorting(truck)
    truck_list[i].package_sorting(distance_file)
delivery(truck_list[0], driver1)
# delivery(truck2, driver2)
# delivery(truck3, drive 1)


# STILL NEED TO HANDLE DELAYS AND ADDRESS CHANGES

Package.time_lookup(package_table)

print(package_table.lookup(14))

"""
DEBUGS:
- package print needs to go in order of PID not index
- Change status to be overridden with "En Route", "Warehouse", or "Delivered"
    - Store package attachment, truck specifics, and errors elsewhere to be saved
    - add address correction for delayed and address packages
- hash_table.lookup(0) NOT obtaining hash index of 0 properly?
- put delayed and address updates onto truck3 at the start
"""
