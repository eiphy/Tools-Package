def makefilter(a, c):
   def myfilter(x):
       if a < x < c:
           return True
   return myfilter

filter14 = makefilter(1, 8)

myList = [1, 2, 3, 4, 5, 6]
a = list(filter(filter14, myList))
print(a)