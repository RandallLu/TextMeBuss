import datetime
import json
import pytz

def get_stop_ids(route_id):
	trip_info = get_trips(route_id)
	stop_ids = []
	# get all differnt stop_ids for a certain route_id
	with open("google_transit/stop_times.txt") as f:
		for line in f:
			parts = line.split(',')
			if (parts[0] in trip_info) and (parts[3] not in stop_ids):
				stop_ids.append(parts[3])
	return stop_ids

def populate_names(stop_ids):
	stop_name = {}
	count = 1;
	# populate stop ids with the name to ease the part of prompting user for input
	with open("google_transit/stops.txt") as f:
		for line in f:
			parts = line.split(',')
			if parts[0] in stop_ids:
				 stop_name[str(stop_ids.index(parts[0]))] = parts[0]+"-"+parts[1]
	return stop_name

def get_stop_list(route_id):
	return populate_names(get_stop_ids(route_id))

def get_trips(route_id):
	direction = {
		'n': "North",
		'e': "East",
		'w': "West",
		's': "South"
	}
	# dictionary with trip_ids as key and service_ids as values
	# service_ids indicate days of the week the bus operates
	trip_info = {}
	with open('google_transit/trips.txt') as f:
		for line in f:
			parts = line.split(',')
			if (route_id[-1].isalpha()):
				if (parts[0] == route_id[:-1]) and (parts[5] == direction[route_id[-1]]):
					trip_info[parts[2]] = parts[1]
			else:
				if (parts[0] == route_id):
					trip_info[parts[2]] = parts[1]
	return trip_info

def get_schedule(trip_info, stop_id):
	arrival_times = []

	# stop_times.txt has trip_id, arrival_time, departure_time(not used), stop_id, ...
	with open('google_transit/stop_times.txt') as f:
		tz = pytz.timezone("America/Los_Angeles")
		for line in f:
			parts = line.split(',')
			if (parts[0] in trip_info) and (parts[3] == stop_id):
				# service_parts[1] has format 0000000 with 0 indicating not operating and 1 otherwise
				service_parts = trip_info[parts[0]].split('-')
				running_days = service_parts[1]
				if running_days[datetime.datetime.now(tz).weekday()] == '1':
					arrival_times.append(parts[1])
	return sorted(arrival_times)

def get_next_arrivals(route_id, stop_id):
	arrival_times = get_schedule(get_trips(route_id), stop_id)
	ret_times = {}

	# time format '00:00:00'
	for time in arrival_times:
		tz = pytz.timezone("America/Los_Angeles")
		date = datetime.datetime.now(tz).strftime("%Y/%m/%d ")
		arrival = datetime.datetime.strptime(date + time, "%Y/%m/%d %H:%M:%S")
		current = datetime.datetime.now(tz)
		current = current.replace(tzinfo=None)

		if arrival > current and len(ret_times) == 0:
			# convert to datetime object
			estimate = datetime.datetime.min + (arrival - current)
			if estimate.hour > 0:
				break
			# strftime only works for datetimes with year >= 1900
			estimate = estimate.replace(year=1900)
			ret_times['first'] = estimate.strftime("%M")
		elif arrival > current and len(ret_times) == 1:
			estimate = datetime.datetime.min + (arrival - current)
			estimate = estimate.replace(year=1900)
			if estimate.strftime("%M") > ret_times['first']
				ret_times['second'] = estimate.strftime("%M")

	ret_times = json.dumps(ret_times)
	return json.loads(ret_times)
