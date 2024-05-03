import only_main_lib as lib
import os
import psutil

print("import main")
# lib.foo()

if __name__ == '__main__':
    print(f"{psutil.Process(os.getpid()).name()} - {__name__}")
    lib.foo()
