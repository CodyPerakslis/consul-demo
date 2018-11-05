from math import sqrt

def factorize(n):
    factors = []
    if n%2 == 0:
        count = 0
        while(n % 2 == 0):
            n //= 2
            count += 1
        factors.append((2,count))
    if n <= 1:
        return factors
    for i in range(3,int(sqrt(n)+1),2):
        if n % i == 0:
            count = 0
            while(n % i == 0):
                n //= i
                count += 1
            factors.append((i,count))
            if n == 1:
                return factors
    factors.append((n,1))
    return factors

while True:
    x = input()
    try:
        y = abs(int(x))
        print(factorize(y))
    except Exception as e:
        print(str(e))
