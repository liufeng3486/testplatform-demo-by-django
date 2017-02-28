class Test():
    def __init__(self):
        print "init"
        self.log = open("./upload/test1.txt","w")
    def start(self):
        print 2
        self.log.write("www")
        self.log.close()
        return "TEST1"
