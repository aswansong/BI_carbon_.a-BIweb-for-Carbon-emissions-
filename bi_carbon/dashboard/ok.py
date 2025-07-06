n = int(input())
l = []
if n == 1:
    print(1)
elif n == 2:
    print(2)
elif n ==3:
    print(3)
else:
    for i2 in range(0,n//2+1):
        for i3 in range(0,n//3+1):
            if n == 2*i2+3*i3:
                l.append(2**i2*3**i3)
l.sort(reverse=True)
print(l[0])



