#Parametric form of recurrsion
def sumn(i : int, ans :int):
    if (i < 1):
        return ans
    return sumn(i - 1, ans + i)
n = 5
print("Sum  = ",sumn(n,0))


        #OR

def sumn(i : int, ans :int):
    if (i < 1):
        print(ans)
        return
    sumn(i - 1, ans + i)
n = 5
print("sumType-: ")
sumn(n,0) 