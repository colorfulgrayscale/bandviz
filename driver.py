#List Example
pals = list()
pals.append( "chris" )
pals.append( "sandy" )
pals.append( "josie" )
print "Items in List => " + str(pals), "List Length => " + str(len(pals))

print "\n"
#Dictionary Example: Great for placing key value pairs without knowing in advance what we will be putting in the dictionary
pal = dict()
pal['first'] = 'Chris'
pal['last']  = 'Aiv'
pal['email'] = 'chrisaiv@gmail.com'
pal['phone'] = '555-555-5555'
print pal

print "\n"

#Forgiving way to find an item within a dictionary
print pal.get("age", "Age not available")
print pal.get("phone", "Phone not available")

print "\n"

#Looping through a Dictionary
print "~~KEY : Value~~"
for key in pal:
	print key, ":", pal[key]
	
print "\n"

#Find out what capabilities are available in a particular Data Object
print dir(pals)