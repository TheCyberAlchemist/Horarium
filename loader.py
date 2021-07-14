from threading import Thread
import os

def println(stri,*args):
	# parent_process = os.fork()
	# print("asd",stri)
	if stri=="t1":
		print("hlello bou")
	else:
		print("hello")
		return "return"

t1 = Thread(target=println, args=("t1",))
t2 = Thread(target=println, args=("t2",))

t1.start()
t2.start()
t1.join()
print(t2.join())
# r,w = os.pipe()
