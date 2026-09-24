# def new_func():
#     resp={'messages':(1,2,3,4,5,6)}
#     for v in resp['messages']:
#         print (v)
        
# new_func()

def is_even(numero: int ):
    if numero % 2 != 0:
        return False
    else: return True

print(is_even(8))

mylist=["apple", "banana"]
newmystr=3* mylist[0]+"banana"
print(newmystr)