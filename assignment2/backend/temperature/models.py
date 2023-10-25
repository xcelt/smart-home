from django.db import models


def tempDefault():
    tempDefault = 22

def increaseTemp(tempDefault):
    for int in tempDefault:
        increase=int+1
        increase.save()
    return increase
    

def decreaseTemp(tempDefault):
    for int in tempDefault:
        decrease=int-1
        decrease.save()
    return decrease
