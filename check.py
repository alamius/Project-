from random import randint
from sett import memory_length

def check_executable(code, level, dbg=0):
    if(type(code) != type('')):
        print("check_executable: no string input as code!, input == '", code, "'", sep='')
        raise TypeError #invalid argument
    if(dbg >= 4): print("check_executable(", code, ")", sep='')
    adding = 0
    moving = 0
    blckng = 0
    i = 0
    while(i < len(code)):
        if(code[i] == '+'):
                    if(moving == 0):
                        adding  += 1
        if(code[i] == '-'):
                    if(moving == 0):
                        adding  -= 1
        if(code[i] == '>'):
                    moving      += 1
        if(code[i] == '<'):
                    moving      -= 1
        if(code[i] in ['b', 's']):
                    blckng      += 1
        i += 1
    moving %= memory_length
    result = bool(
        (
            level == 0
            # and moving == 0
            and (
                blckng >= 1
                or randint(0, 100) < 1
            )
        ) or (
            level > 0
            and adding <= -1
            and moving == 0
            and (
                len(code) > 0
                or randint(0, 100) < 5
            )
        )
    )
    if(dbg >= 2 and result or dbg >= 3):
        print(
            "check_executable: ",
            "level == ", level,
            ", adding == ", adding,
            ", moving == ", moving,
            ", blocks == ", blckng,
        sep='')
    return result

def opposite(char1, char2):
    return bool(
        char1 == '+' and char2 == '-' or
        char1 == '-' and char2 == '+' or
        char1 == '>' and char2 == '<' or
        char1 == '<' and char2 == '>'
    );

def code_matches_blocks(prog):
    code = prog[0]
    blocks = prog[1]
    for i in range(len(code)):
        if(code[i] in ['b', 's'] and blocks[i] == ['',[]]):
            return False
    return True
    
