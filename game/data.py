import xmltodict
import requests
import math


class Maps(object):

	nodes = {}
	ways = []
	origin = None
	width = 0
	height = 0

	SIG_PLACES = 3;
	GRID_SIZE = 0.001;

	def __init__(self, *args, **kwargs):
		super(Maps, self).__init__(*args, **kwargs)


	def float_floor_to_precision(self, value, precision):
		for i in range(precision):
			value *= 10
		value = math.floor(value)
		for i in range(precision):
			value /= 10
		return value


	def fetch_grid(self, coords):
		lat = self.float_floor_to_precision(coords[0], self.SIG_PLACES)
		lng = self.float_floor_to_precision(coords[1], self.SIG_PLACES)

		return self.fetch_area([
			lat - self.GRID_SIZE,
			lng - self.GRID_SIZE,
			lat + self.GRID_SIZE,
			lng + self.GRID_SIZE
		])

	def fetch_area(self, bounds):
		print bounds
		self.width = (bounds[2] - bounds[0]) / 2
		self.height = (bounds[3] - bounds[1]) / 2
		self.origin = (
			bounds[0] + self.width,
			bounds[1] + self.height
		)
		print "Fetching maps..."
		response = requests.get("http://www.openstreetmap.org/api/0.6/map?bbox=%f,%f,%f,%f" % (
				bounds[0],
				bounds[1],
				bounds[2],
				bounds[3]
			)
		)
		print "... got 'em."
		osm_dict = xmltodict.parse(response.text.encode('UTF-8'))
		try:
			for node in osm_dict['osm']['node']:
				self.nodes[node['@id']] = node

			for way in osm_dict['osm']['way']:
				waypoints = []
				for node_id in way['nd']:
					node = self.nodes[node_id['@ref']]
					waypoints.append((float(node['@lat']), float(node['@lon'])))
				self.ways.append(waypoints)
		except:
			print response.text

	def fetch_by_coordinate(self, coords, range):
		return self.fetch_area((
			coords[0] - range,
			coords[1] - range,
			coords[0] + range,
			coords[1] + range
		))

	def transpose_ways(self, dimensions, offset, flip_y=True):
		width = dimensions[0]
		height = dimensions[1]
		w_coef = width / self.width / 2
		h_coef = height / self.height / 2
		transways = []
		for way in self.ways:
			transway = []
			for waypoint in way:
				lat = waypoint[1] - self.origin[0]
				lng = waypoint[0] - self.origin[1]
				wp = [
					(lat * w_coef) + offset[0],
					(lng * h_coef) + offset[1]
				]
				if flip_y:
					wp[1] *= -1
					wp[1] += offset[1] * 2
				transway.append(wp)
			transways.append(transway)
		return transways
