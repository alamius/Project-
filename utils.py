
def isset(array, i):
    try:
        array[i]
        return True
    except IndexError:
        return False

def isint(val):
    try:
        int(val)
        return True
    except (TypeError, ValueError):
        return False

def set_at(string, i, char):
    string = string[0:i] + char + string[i+1:]
    return string

def get_int_input(prompt, error_message="This is no valid input. Use integers like -2, 0, 5!"):
    while(True):
        inputt = input(prompt)
        if(isint(inputt)):
            return int(inputt)
        else:
            print(error_message)

def right_signs(n):
    if(n > 0):
        return ">" * n
    elif(n < 0):
        return "<" * -n
    else:
        return ""

def add_signs(n):
    if(n > 0):
        return "+" * n
    elif(n < 0):
        return "-" * -n
    else:
        return ""

def shift(rights=[1], adds=[-1, 2]):
    result = ""
    result += add_signs(adds[0])
    i = 0
    while(i < len(rights)):
        # print("shift[", i, "]: ", rights[i],", ", adds[i-1], sep='')
        result += right_signs(rights[i])
        result += add_signs(adds[i+1])
        i += 1
    result += "<" * sum(rights)
    return [result,[]]

def isiterable(object):
    try:
        object[0]
        return True
    except:
        return False

def flatcopy(arr):
    result = []
    if(type(arr) == type([])):
        for obj in arr:
            result += flatcopy(obj)
    else:
        result += [arr]
    return result

def map(x, start1, stop1, start2, stop2):
    return ((x-start1)/(stop1-start1))*(stop2-start2)+start2
