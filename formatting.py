from utils import isint

def ls(level): #level_spacing
    return ("  " * level)

def f(val, min_length=3, max_length=-1):
    string = str(val)
    if(max_length > -1 and len(string) > max_length):
        string = string[0:max_length]
    if(min_length > -1 and len(string) < min_length):
        string = " " * (min_length - len(string)) + string
    return string

def memory_str(memory, p=-1, executing_char='', sep="|", marker='', s1=2, s2=3, mode="", filter_0=True):
    result = ""
    # executing_char = f(executing_char, 1, 1)
    for i in range(len(memory)):
        cell = memory[i]
        if(mode == "int" and isint(cell)):
            cell = int(cell)
        elif(mode == "bool" and type(cell) == type(True) or mode == "boolean"):
            if(cell == False):
                cell = "F"
            else:
                cell = "T"
        if(i == p % len(memory)):
            result += f(marker + executing_char, s1, s1) + f(str(cell), s2, s2) + sep
        else:
            if(memory[i] == 0 and filter_0 and not executing_char=='o'):
                result += " "*(s1+s2) + sep
            else:
                result += f(cell, s1+s2, s1+s2) + sep
    return result

def pa_ls(lvl, line_break): #print_array_level_spacing
    if(not '\n' in line_break):
        return ""
    else:
        return "  " * lvl

def print_arr(
    arr,
    lvl=0,
    max_level=10,
    str_quote=True,
    type_print=False,
    line_break='',
    auto_print=True,
    dbg=0
):
    if(dbg >= 3): print("print_arr(", arr, ")", sep='')
    lb = line_break
    result = ""
    if(lvl > max_level):
        result += pa_ls(lvl, lb) + "max_level" + line_break
        if(auto_print):
            print(result)
        return result
    if(type(arr) == type([])):
        i = 0
        std_counter = 0
        result += pa_ls(lvl, lb) + '[' + line_break
        while(i < len(arr)):
            if(arr[i] == ['', []]):
                std_counter += 1
                try:
                    if(arr[i+1] == ['', []]):
                        i+=1
                        continue
                except:
                    i+=1
                    continue
                result += pa_ls(lvl+1, lb) + "[std]*" + str(std_counter) + line_break
                if(not '\n' in line_break and i+1 < len(arr)):
                    result += ', '
            else:
                # if(std_counter > 0):
                #     result += pa_ls(lvl+1, lb) + "[std]*" + str(std_counter) + line_break
                #     if(not '\n' in line_break and i+1 < len(arr)):
                #         result += ', '
                std_counter = 0
                if(dbg >= 4): print('print_arr: arr[',i,']: ', arr[i],", lvl == ", lvl, sep='')
                result += print_arr(arr[i], lvl=lvl + 1, line_break=line_break)
                if(not '\n' in line_break and i+1 < len(arr)):
                    result += ', '
            i += 1
        if(std_counter > 0):
            result += pa_ls(lvl+1, lb) + "[std]*" + str(std_counter) + line_break
        result += pa_ls(lvl, lb) + ']' + line_break
    else:
        if(type(arr) == type("")):
            result += pa_ls(lvl, lb) + "'" + str(arr) + "'" + line_break
        else:
            result += pa_ls(lvl, lb)       + str(arr)       + line_break

    if(auto_print and lvl == 0):
        print(result)
    return result

def to_str(prog, level=0, dbg=0):
    if(dbg >= 4): print("to_str(", prog, ")", sep='')
    code = prog[0]
    blocks = prog[1]
    result = ""
    i = 0
    while(i < len(code)):
        if(
            code[i] != '' and
            not code[i] == '#' and
            not code[i] == 'b' and
            code[i] in '+-<>[]bs#io'
        ):
            result += code[i]
        elif(code[i] == 'b'):
            result += '['
            result += to_str(blocks[i], level+1)
            result += ']'
        i += 1
    return result
