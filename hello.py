def my_multi(fn1, fn2):
    myres1 = fn1 * fn2
    return myres1


myres1 = my_multi(10, 8)
print(myres1)
if myres1 > 30:
    myres1 = my_multi(3, 20)
    print(myres1)
else:
    print(10)

dupli_value = {1, 2, 3, 4, 5}
uniq_val = set(dupli_value)

print(dupli_value)
print(uniq_val)
