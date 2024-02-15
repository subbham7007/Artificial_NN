# tO find fACTorial via RECURRSION
def factorial(n,ans):
    if (n == 1):
        print(ans)
        return
    factorial(n -1, ans * (n))

#Change n based on your choice    
n = 5
factorial(n,1)