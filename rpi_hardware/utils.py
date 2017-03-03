# Decorators

def main_loop(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except KeyboardInterrupt:
            GPIO.cleanup()
    return wrapper

if __name__ == '__main__':
	pass