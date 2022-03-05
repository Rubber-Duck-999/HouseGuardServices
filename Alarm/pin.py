class Pin:
	def __init__(self):
		self.pin_entry = [
			[0, 1, False],
			[0, 10, False],
			[0, 100, False],
			[0, 1000, False]
		]

	def get_value(self):
		value = 0000
		for number in self.pin_entry:
			value = value + number[0] * number[1]
		return str(value)

	def set_value(self, value):
		index = 0
		value_not_set = True
		while index < len(self.pin_entry) and value_not_set:
			if self.pin_entry[index][2] == False:
				self.pin_entry[index][0] = value
				value_not_set = False
			self.pin_entry[index][2] = True
			index = index + 1

	def clear(self):
		index = 0
		while index < len(self.pin_entry):
			self.pin_entry[index][0] = 0
			self.pin_entry[index][2] = False
			index = index + 1