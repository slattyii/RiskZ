import time

def Delay(seconds):
	try:
		return time.sleep(1)
	except Exception:
		return