import threading


def except_handler(args):
    print(args.exc_type)


threading.excepthook = except_handler

def gen_error():
    print(1/0)

t = threading.Thread(target=gen_error)
t.start()

