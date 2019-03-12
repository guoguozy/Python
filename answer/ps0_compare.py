"""
Author     : 郭梓煜  数据科学与计算机学院
Student ID : 17341046
mail       : 893050234@qq.com

"""
import math
num1 = input("Enter number x:")
num2 = input("Enter number y:")

# print("X**y = %s\nlog(x)=%s\n" % (int(num1)**int(num2),math.log(int(num1),2)))

result1 = int(num1)**int(num2)
result2 = math.log(int(num1))

print("x**y = {}\nlog(x) = {}".format(result1, result2))
print("x**y = {1}\nlog(x) = {0}".format(result2, result1))
print("x**y = {a}\nlog(x) = {b}".format(b=result2, a=result1))
