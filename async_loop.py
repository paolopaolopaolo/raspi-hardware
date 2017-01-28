import asyncio
import subprocess

if __name__ == '__main__':
	asyncio.get_child_watcher()
	process = asyncio.get_event_loop()
	subprocess.Popen("sudo python light_sensor.py record", shell=True)
	try:
		process.run_forever()
	finally:
		process.close()