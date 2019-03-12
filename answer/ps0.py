'''
solution for ps0, just for fun
'''

import math


class PowerDescriptor:
    def __get__(self, instance, owner):
        return instance.x**instance.y


class Calculate:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    power = PowerDescriptor()

    @property
    def logarithm(self):
        return math.log2(self.x)


x = int(input("Enter number x:"))
y = int(input("Enter number y:"))

calculate = Calculate(x, y)

print("x**y = {power}\nlog(x) = {logarithm}".format(power=calculate.power,
                                                    logarithm=calculate.logarithm))
