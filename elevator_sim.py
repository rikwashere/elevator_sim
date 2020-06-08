import unicodecsv as csv
import random
import math
import sys

class Building:
	def __init__(self):
		self.floors = 10

class Elevator:
	def __init__(self, Building, capacity, i):
		self.max_capacity = capacity
		self.travel_time = 0
		self.id = i
	
		self.travel_time_floor = 2.5
		self.entry_time = 2.5
		self.exit_time = 2.5
		self.wait_time = 5
		self.trips = 0

		self.location = 0
		self.load = {floor: [] for floor in range(1, Building.floors + 1)}

	def travel(self):
		self.location += 1
		self.trips += 1
		self.travel_time += self.travel_time_floor

		while len(self.get_occupants()) > 0:
			if len(self.load[self.location]) > 0:
				print('Elevator is at floor <%i> with <%i> passengers. Travel time is %.2f seconds.' % (self.location, len(self.get_occupants()), self.travel_time))			
				print('\t%i passenger(s) want(s) to exit here.' % len(self.load[self.location]))
				for p in self.load[self.location]:
					print('\t\tPassenger <%i> has reached destination.' % p.position_in_queue)
					p.travel_time = self.travel_time
					p.report(building, self.max_capacity, self.trips)
					self.travel_time += self.exit_time

				self.load[self.location] = []
			else:
				# go up a floor
				self.location += 1
				self.travel_time += self.travel_time_floor			
		else:
			print('Elevator is empty. Returning to lobby.')
			print('Currently at floor <%i>. Travel time to lobby: <%.2f>' % (self.location, self.location * self.travel_time_floor))
			
			self.travel_time += self.location * self.travel_time_floor
			self.location = 0

	def get_occupants(self):
		passengers = []
		for floor in self.load:
			for p in self.load[floor]:
				passengers.append(p)

		return passengers
	
class Passenger():
	def __init__(self, building, i):
		self.origin_floor = 0
		self.destination = random.randrange(self.origin_floor + 1, building.floors + 1)
		self.waiting_time = 0
		self.travel_time = 0
		self.position_in_queue = i

	def report(self, building, capacity, trips):
		with open('data_out.csv', 'ab') as csv_out:
			writer = csv.writer(csv_out, delimiter=';')
			data = [capacity, building.floors, self.position_in_queue, self.destination, trips, self.travel_time]
			writer.writerow(data)
		
building = Building()
passengers = [Passenger(building, i) for i in range(1,51)]

for capacity in range(1,50):

	elevator = Elevator(building, capacity, '1')
	print('Loading passengers... (max. %i)' % elevator.max_capacity)

	for passenger in passengers:
		print('\tPassenger <%i> -> floor %i' % (passenger.position_in_queue, passenger.destination))
		elevator.travel_time += elevator.entry_time
		elevator.load[passenger.destination].append(passenger)
		print('\t\tElevator occupants: %i' % len(elevator.get_occupants()))

		if len(elevator.get_occupants()) == elevator.max_capacity:
			print('Elevator full. Travelling.')
			elevator.travel()
	else:
		elevator.travel()