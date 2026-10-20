from pathlib import Path
import os
def crtfile():
    try:
        name = input("please enter the file name:-")
        path = Path(name)
        if not path.exists():
            with open(path,"w") as fs:
                data = input("whatever you want to write in your file:-")
                fs.write(data)
            print("file created successfully")
        else:
            print("file name already exists")
    except Exception as err:
        print(f"an error occurred a{err}")


def readfile():
    try:
        name = input("please enter the file name:-")
        path = Path(name)
        if path.exists():
            with open(path,"r") as fs:
                content = fs.read()
                print(f"your file content is \n {content}")
        else:
            print("no such file exists")
    except Exception as err:
        print(f"an error occurred as {err}")
def updfile():
    try:    
        name = input("Please tell the file name:-")
        path = Path(name)

        if path.exists():
            print("operations")
            print("Press 1. For renaming the file")
            print("Press 2. For appending content in the file")
            print("Press 3. For overwriting the file")

            choice = int(input("Enter your option:-"))

            if choice == 1:
                newname = input("Please enter the new name:-")
                new_path = Path(newname)
                if not new_path.exists():
                    path.rename(new_path)
                    print("file renamed succcessfully")
                else:
                    print("file name already exists")
            elif choice == 2:
                with open(path, "a") as fs:
                    data = input("what do you want to append")
                    fs.write(" \n"+data)
                    print("successfully appended")

            elif choice == 3:
                        with open(path, "w") as fs:
                            data = input("what do you want to overwrite")
                            fs.write(" \n"+data)
                            print("successfully overwritten")
    except Exception as err:
        print(f"an error occurred as {err}")
             
        
def dltfile():
    try:
        name = input("Please enter the file name:-")
        path = Path(name)
        if path.exists():
            path.unlink()
            print("file deleted successfully ")
        else:
            print("no such file exists")
    except Exception as err:
        print(f"an error occurred as {err}")





print("Press 1 for creating a file")
print("Press 2 for reading a file")
print("Press 3 for updating a file")
print("Press 4 for deleting a file")
a = int(input("Please choose a response:-"))

if a == 1:
    crtfile()
if a == 2:
    readfile()
if a == 3:
    updfile()
if a == 4:
    dltfile()

