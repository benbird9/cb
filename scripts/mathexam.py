import random

print "Welcome Yu Lanqing for math exam today!! \n"
raw_input("Press any key to start....")

error = 0


def genExpr():
    expr = ''
    if z % 4 == 0:
        expr = str(z) + '+' + str(x) + '*' + str(y)
    elif z % 4 == 1:
        expr = str(z) + '+' + str(mul_value) + '/' + str(x)
    elif z % 4 == 2:
        expr = str(z + x * y) + '-' + str(x) + '*' + str(y)
    elif z % 4 == 3:
        expr = str(z + x * y) + '-' + str(mul_value) + '/' + str(x)
    return expr


for x in range(0, 80):


    expr = genExpr()

    # var = int(raw_input(expr + '='))
    # if var == eval(expr):
    #     print 'Good Job, :) '
    # else:
    #     print "Wrong, :("
    #     error = error + 1
print 'total error:' + str(error)
