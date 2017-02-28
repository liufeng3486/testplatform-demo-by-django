
path = "D:\\work\\vpal_test_mock\\src\\main\\webapp\\beifu\\zhiyang\\"

import os

for root, dirs, files in os.walk(path):
    print("Root = ", root, "dirs = ", dirs, "files = ", files)

for i in files:
    if i[-4:]==".jsp":
        print i[:-4]

