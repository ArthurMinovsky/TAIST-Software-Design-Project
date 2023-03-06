# TAIST Software Design Project Group : )

## Objectives
* Assemble harware component for controlling parking gate
* Applied Internet of Things Concept to improve parking system
* Integate Artificial Intelligenct to make smart parking system

## Scope
1. Concepts: 
   * Department Store Smart Parking System

## User stories and acceptance criteria
1. As a **customer**, I want to **get a parking stall without driving around the parking lot** so that **I can save time and energy looking for one**.
   * Scenario: **customer visits**, given **there is a parking stall**, when **the car pulls up in front of the gate**, then **the parking stall number is assigned (Push Style), and the gate opens**.
   * Scenario: **customer visits**, given **there is NO parking stall**, when **the car pulls up in front of the gate, then there will be a sign saying ‘FULL’, and the gate will not open**.
2. As an **owner**, I want to **see how many cars are in the parking lot** so that **I can understand the current status**.
	* Scenario: **Density**, given **RFID tags are assigned**, when **checked**, then **the percentage occupied is displayed**.
	* Scenario: **Income**, given **the duration of parked cars**, when **checked**, then **the realized and unrealized income is reported**.
	>Realized income is when the customer has already paid the fee for their duration parked and out of the system. <br />
	>Unrealized income is when the customer is still in the system, and the calculation is done through the duration parked up until now.
3.	As an **owner**, I want to **know historical data of how long and how many customers used the parking lot** so that **I can analyze the data for prediction**.
	* Scenario: **Utilization**, given **the percentage of stall occupied is calculated**, when **the number is low**, **then the space can be allocated for other purposes**.
	* Scenario: **Advance Booking**, given **the statistic of stall occupied is determined**, when **the customer wants to know space availability in advance**, then **I can tell whether there will be available space or not**.
	* Scenario: **Operation Management**, given **there are databases of customer behavior when the statistic of customer behavior is determined**, then **the department can adjust their operation like opening/closing time, employees hired, and facility investment accordingly**.

## Software architecture
### System Structure:
* Design overall system for Department Store Smart Parking.
![Overall System](https://user-images.githubusercontent.com/126540644/223204760-86a943d7-bf67-4603-afd4-6a59f919b429.jpg)
* The sequence, when customers come into the store parking.
![Customer Sequence](https://user-images.githubusercontent.com/126540644/223205104-3406ccb1-c148-4132-89e2-daf10518be38.jpg)
* The sequence, when the owner wants to access the data.
![Owner Sequence](https://user-images.githubusercontent.com/126540644/223205325-608ffcdf-0561-419f-ae5c-59cdd54b173f.jpg)

### ESP32 tag:

### ESP32 scanner:

### LINE bot:

### AI:

### LIFF UI: 

## System requirements
### Things layer:

### Gateway layer:

### Server layer:

### Service layer:

### UI layer:

## Software implementation
### Firmware development

### LINE bot development

### LIFF UI development
