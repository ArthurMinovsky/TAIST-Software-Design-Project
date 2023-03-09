# G4: Department Store Smart Parking System : )

## Objectives
* Assemble harware component for controlling parking gate
* Applied Internet of Things Concept to improve parking system
* Integate Artificial Intelligenct to make smart parking system

## Scope
1. Concepts: 
   * Department Store Smart Parking System

## User stories and acceptance criteria
1. As a **customer**, I want to **get a parking stall without driving around the parking lot** so that **I can save time and energy looking for one**.
   * Scenario: **Parking Availability**, given **Parking stall is available**, when **the car pulls up in front of the gate**, then **the parking stall number is assigned (Push Style), and the gate opens**.
   * Scenario: **customer visits**, given **FULL parking stall**, when **the customer will be notified that the parking is full, and the gate will not open**.
2. As an **owner**, I want to **see how many cars are in the parking lot** so that **I can understand the current status**.
	* Scenario: **Density**, given **RFID tags are assigned**, when **checked**, then **the percentage occupied is displayed**.
	* Scenario: **Income**, given **parked cars' activity**, when **checked**, then **the total income from the beginning of the months up to now and last month are reported**.
2. As an **owner**, I want to **know historical data of how long and how many customers used the parking lot** so that **I can analyze the data for prediction**.
	* Scenario: **Utilization**, given **the percentage of stall occupied is calculated**, when **the number is low**, **then the space can be allocated for other purposes**.

## Software architecture
### System Structure:
* Software system consists of three software stacks for detecting cars by IR sensor, parking ID collection data (ID, Status, Time), and Mobile UI to show the parking ID in LINE application.
![Overall ALL](https://user-images.githubusercontent.com/126540644/223935601-0f33ba08-4e95-4eff-b86b-0d2414c28090.jpg)
* The sequence to access the Mac Address of Customer.
![Sequence 1](https://user-images.githubusercontent.com/126540644/223780041-dd91a8f1-43d2-4b0d-a072-fa7597b572a6.jpg)
* The sequence, when customer come in store parking system.
![Sequence 2](https://user-images.githubusercontent.com/126540644/223780460-c247bd78-e674-4200-99ff-71300c1725c3.jpg)
And when customer come out.
![Sequence 3](https://user-images.githubusercontent.com/126540644/223780699-d2758c63-581d-430a-8f73-7cb4527ddf0b.jpg)
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
