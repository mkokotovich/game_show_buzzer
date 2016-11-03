import sys
import urllib2
import getopt

server = "192.168.86.200"

team = "default_team"

try:                                
    opts, args = getopt.getopt(sys.argv[1:], "t:s:", ["team=","server="])
except getopt.GetoptError:
    sys.exit(2)

for opt, arg in opts:
    if opt in ("-t", "--team"):
        team = arg
    elif opt in ("-s", "--server"):
        server = arg

print "Using team: {} and server: {}".format(team, server)
print "Press enter to buzz"

url="http://{}/buzz?team={}".format(server, team)


while True:
    x = raw_input()
    response = urllib2.urlopen(url)
    html = response.read()
    print "Buzzed!"
