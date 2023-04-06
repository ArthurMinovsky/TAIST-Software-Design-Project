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
* Software system consists of three software stacks for detecting cars by parking ID collection data (ID, Status, Time), and Mobile UI to show the parking ID in LINE application.
![System overview](https://user-images.githubusercontent.com/126540644/230456586-e4a93e9e-c0b7-4112-bcd7-eb2aad36203d.png)
* The sequence, when customer come in store parking system.
![Sequence_CarIN](https://user-images.githubusercontent.com/126540644/230457082-fd6e6091-83ec-4345-82cc-cbdd0258c38c.png)
And when customer come out.
![Sequence_CarIOUT](https://user-images.githubusercontent.com/126540644/230458240-ae6a112d-ce13-4136-9448-164988d0534d.png)
* The sequence, when the owner wants to access the data.
![Sequence_Owner](https://user-images.githubusercontent.com/126540644/230458614-71e84a5a-eec2-4105-99ca-50f35fe7a3e1.png)


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
domain for webhook: parkbot.online

### LIFF UI development
