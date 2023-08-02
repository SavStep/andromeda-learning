import time
def kalk(a,b):
    res = a * b
    summa = a + b
    if res >= 1000:     
        print(res)
    elif res <= 1000:
        print(summa)
a = int(input("введи число:"))
b = int(input("введи число:"))
print("ждите,операция выполняется . . .")
time.sleep(2.5)
print("готово!")
time.sleep(0.5)
kalk(a,b)    

k = 0
for i in range(0,11):
    x_sum = k + i
    print(f"предыдушее число - {k}, текушее - {i}, сумма - {x_sum}")
    k = i

