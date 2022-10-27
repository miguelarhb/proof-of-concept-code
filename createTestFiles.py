import os

def delete_files():
    os.system("rm -r ./testFiles")

def generate_files(quantity, nbytes):
    os.system("mkdir ./testFiles")
    for i in range(quantity):
        filename = "./testFiles/testFile_" + str(i)
        with open('%s'%filename, 'wb') as f:
            f.write(os.urandom(nbytes))





