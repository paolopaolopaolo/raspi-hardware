import RPi.GPIO as GPIO

# Decorators

def main_loop(func):
	def wrapper(*args, **kwargs):
		try:
			func(*args, **kwargs)
		except KeyboardInterrupt:
			GPIO.cleanup()
	return wrapper


# Small Util functions

def prev_index(index, array, cycle=False):
	if index == 0:
		if cycle:
			return len(array) - 1
		return index
	else:
		return index - 1


def next_index(index, array, cycle=False):
	if index == len(array) - 1:
		if cycle:
			return 0
		return index
	else:
		return index + 1


def random_next_index(index, array):
	last_index = index
	while index == last_index:
		index = randrange(0, len(array))
	return index