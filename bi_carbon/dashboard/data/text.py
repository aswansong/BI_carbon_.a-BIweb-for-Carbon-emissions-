D = 917*10**6
G = 0.2631
r = 0.034189
n = 3
p=0
for i in range(1,n+1):
    p += (D*((1+G)**n))/((1+r)**n)

print(p)












