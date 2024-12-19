# from django.test import TestCase


# def sq_decorator(function):

#     def wrapper():
#         resnav = function() 
#         # print(caps)
#         return resnav * resnav
    
#     return wrapper 


# def minus_decorator(function):

#     def wrapper():
#         resnav = function()  
#         return resnav -  2
    
#     return wrapper 

# def uppercase_decorator(function):

#     def wrapper():
#         resn = function()
#         caps = resn.upper()
#         # print(caps)
#         return caps
    
#     return wrapper 


# def split_string(function):
#     def wrapper():
#         fngr = function()
#         vare = fngr.split()

#         return  vare
    
#     return wrapper

# @split_string 
# @uppercase_decorator 
# def say_hi():
#     varn = 'hello there'
#     # print(varn)
#     return varn



# def say_himen():
#     varn = 'hello there'
#     # print(varn)
#     return varn

# varns = say_hi()

# print("varns",varns)


# varnse = say_himen()

# print("varnseeee",varnse)




# @minus_decorator 
# @sq_decorator
# def say_hiaew():
#     varn = 5 
#     # print(varn)
#     return varn

# varnsaq = say_hiaew()

# print("varnsaq",varnsaq)


# def say_hiaewsevt():
#     varn = 5  
#     return varn

# varnsaqsvt = say_hiaewsevt()

# print("varnsaqsvtttttt",varnsaqsvt)


# import random

# print(random.randrange(1,13,2))


# num = 5
# # If given number is greater than 1
# if num > 1:
#     # Iterate from 2 to n // 2
#     fde = (num//2)+1
#     print("fde ",fde)
#     for i in range(2, fde):
#         print("ial",i)
#         # If num is divisible by any number between
#         # 2 and n / 2, it is not prime
#         if (num % i) == 0:
#             print(num, "is not a prime number")
#             break
#     # else:
#     print(num, "is a prime number")
# else:
#     print(num, "is not a prime number")

# print(2**4)


# def get_indices(element, lst):
#     indices = []
#     for i in range(len(lst)):
#         if lst[i] == element:
#             indices.append(i)
#     return indices


# arres = [83,85,87,84,86]

# print(arres)
# ide = 84
# indem = arres.index(ide)
# print("pehla index",indem)
# dhfd = 2

# arres.remove(ide)

# print(arres)


# arres.insert(dhfd,ide)

# print(arres)

# # del arres[indem]

# element = 3
# indices = get_indices(ide, arres)

# for ihh in indices:
#     if ihh != dhfd:
#         del arres[ihh]


# print(arres)

fh = [1,2,3]

bg = [1,3]


print(list(set(fh) - set(bg)))

