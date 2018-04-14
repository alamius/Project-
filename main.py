from random import choice, randint
from formatting import *
from testing import *
from sett import *
from check import *
from utils import *
    # isint,
    # isiterable,
    # flatcopy,
    # set_at,
    # get_int_input,
    # right_signs,
    # add_signs,
    # shift,
    # map
# test_formatting_f()
# test_formatting_ls()
# test_formatting_memory_str()
# test_formatting_print_arr()
# test_utils_all()
# test_check_check_executable()
# test_formatting_to_str()

# exit(0)

level = 0
rinput = None #means random input
routput = 0
chars_executed = 0
dbg = 0
level_indentation = "  "
perfect_progs = []
good_progs = []

memory = []
exe_level = 0
p = 0 #'pointer' to the current memory cell

used = [False]*memory_length #used memory_cells
used_index = 0

def load_gauss_table():
    gauss_table_file = open("gauss.table",'r')
    gauss_table = (gauss_table_file.read()).split('\n')[:-1]
    gauss_table_file.close()
    return gauss_table

gauss_table = load_gauss_table()

def get_table_gaussian():
    return int(gauss_table[randint(0, len(gauss_table)-1)])

def non_zero_get_table_gaussian():
    res = int(gauss_table[randint(0, len(gauss_table)-1)])
    while res == 0:
        res = int(gauss_table[randint(0, len(gauss_table)-1)])
    return res

#@test@file@main@func@non_zero_get_table_gaussian
# table = []
# for i in range(0, 20000):
#     table += [non_zero_get_table_gaussian()]
# for i in range(-20, 20):
#     print(i, ": ", "#"*int(table.count(i)/25), sep='')
# exit(0)

def generate(
    start=0,
    stop=len_of_code-1,
    pre_prog=['',[]]
):
    if(dbg >= 1):
        print("generate(", start, ", ", stop, ")", sep='') # print_arr(pre_prog)
    global level, used, used_index
    pre_code = pre_prog[0]
    pre_blocks=pre_prog[1]
    if(level == 0):
        if(dbg >= 3): print(
            "generate: deleting used, that was: ",
            memory_str(used, s1=2, s2=2, mode="bool")
        )
        used = [False]*memory_length #used memory_cells
        used_index = 0
    if(not (0 <= start <= stop <= len_of_code - 1)):
        print("generate: invalid ranges:", start, stop, len_of_code)
        input("result of generate: pre_prog ==" + print_arr(pre_prog) + "[ENTER]")
        return pre_prog
    if(start == stop):
        stop = start + 1
    counter = 0
    while(True):
        code = pre_code
        blocks = pre_blocks
        if(code == ''):
            code = " " * len_of_code
        if(len(blocks) < len(code)):
            blocks = pre_blocks + [std]*(len_of_code - len(pre_blocks))
        try:
            blocks = blocks[:len(code) + 5]
        except:
            blocks += [['',[]]]*5

        counter += 1
        if(counter > 100):
            if(dbg >= 1): print("generate:WARNING:No valid code was generated! RETURN(['-', []])")
            # try:
            if(dbg >= 2): print_arr(pre_prog)
            # except:
            #     None
            return ['-', []]
        i = start
        if(level == 0 and i == 0):
            code = set_at(code, i, 'i')
            try:
                blocks[i] = ['',[]]
            except IndexError:
                blocks += ['',[]]
            i += 1
        while(i < stop):
            cch = choice(random_str)
            if(
                (i >= 1 or level > 0)
                and not opposite(cch, code[i-1])
            ):
                code = set_at(code, i, cch)
            else:
                continue
            if(dbg >= 3): print("generate:", ls(level), "code["+str(i)+"] == '"+str(code[i])+"'")
            if(code[i] == '#'):
                if(level > 0 or randint(0, 100) < 20):
                    code = code[:code.index('#')]+'o' #just temporarily?
                    blocks=blocks[:len(code)]
                    break
                else:
                    continue
            if(
                code[i] in ['b', 's']
                and level >= max_level
            ):  continue
            blocks+=[['',[]]]
            if(dbg >= 3): print("generate: prog: ", print_arr([code, blocks], auto_print=False))
            if(dbg >= 4): input()
            i += 1

        if(check_executable(code, 0)):
            # print(ls(level),end='')
            # print("generated before check_and_clean: ")
            # print_arr([code, blocks])
            max_level_loc = level
            if(code_matches_blocks([code, blocks])):
                max_level_loc = 10
            prog = check_and_clean([code, blocks], max_level = max_level_loc)
            if(prog == False or prog == ['',[]]):
                if(dbg >= 3): print("generate: not accepted by check_and_clean!")
                continue
            # print_arr(prog, auto_print=True)
            code = prog[0]
            blocks = prog[1]
            break
        elif(dbg >= 3):   print("generate: not accepted by check_executable!")
    #generate successful
    code = code.strip(' ')
    blocks = blocks[:len(code)]
    if(level == 0):
        code += 'o'
        blocks+=[['',[]]]
    i = 0 #everything shall be checked, but only 'b's in range are rewritten
    while(i < stop and i < len(code)):
        # if(dbg >= 3): print("generate:", ls(level), code, blocks, i)
        if(code[i] == 'b' and start <= i <= stop):
            level += 1
            blocks[i] = generate()
            level -= 1
        elif(code[i] == 's' and start <= i <= stop):
            code = set_at(code, i, 'b')
            blocks[i] = random_shift()
        elif(code[i] != 'b'):
            try:
                blocks[i] = ['',[]]
            except IndexError:
                # print("generate:IndexError: i == ", i, ", length of blocks == ", len(blocks), sep='')
                print_arr(blocks, line_break='')
        i += 1
    if(level == 0):
        #against an ununderstood bug. sorry
        code = code[:code.index('o')+1]
    if(code.count('b') == 0):
        blocks = []
    else:
        blocks = blocks[:len(code)]
    if(False in flatcopy([code, blocks])):
        input("result of generate: prog ==" + print_arr([code, blocks]) + "[ENTER]")
        if(level > 0):
            return ['-', []]
        else:
            return ['io',[]]
    return [code, blocks]

def redirect_input(prompt="intput: "):
    if(not random_input):
        return get_int_input(prompt) #user input
    if(rinput == None):
        return randint(min_input, max_input) #random input
    return rinput #preset input

def redirect_output(var, string="output: "):
    if(random_input):
        routput = var
    else:
        print(string, f(var, 10), sep='')

def execute(prog):
    if(dbg >= 3): print("execute(", print_arr(prog, line_break=''), ")")
    code = prog[0]
    blocks = prog[1]
    global chars_executed, memory, exe_level, p, routput
    if(exe_level == 0):
        memory = [0]*memory_length
        p = 0
    i = 0
    while(i < len(code)):
        if(dbg >= 3): print("execute:", f(code, 30, 30), "[", i, "] >> ", sep='', end='')
        if(dbg >= 3): print(" " * exe_level + 'l' + " " * (5 - exe_level), end='')
        if(dbg >= 3): print(" { ", memory_str(memory, p, executing_char=code[i]), " }{", f(p), "}, counter == ", chars_executed, sep='', end='\n')
        # if(dbg >= 3 and chars_executed % 100 == 99): input()
        if(code[i] == '-'): memory[p % memory_length] -= 1
        elif(code[i] == '+'): memory[p % memory_length] += 1
        elif(code[i] == '<'): p -= 1
        elif(code[i] == '>'): p += 1
        elif(code[i] == 'b'):
            if(dbg >= 4): print("execute: memory[", f(p % memory_length), "] == ", memory[p % memory_length], sep='')
            exe_level += 1
            while(memory[p % memory_length] > 0):
                if(memory[p % memory_length] <= 0):
                    #blocks always decrement, so negativ input would be useless
                    print("execute:KILL: memory[p] == ", memory[p], " while calling for decremental block", sep='')
                    routput = max_output

                    exe_level = 0
                    1/0 #kill
                if(dbg >= 4): print("execute:     ", print_arr(blocks, auto_print=False), "[", i, "] == ", blocks[i])
                try:
                    execute(blocks[i])
                except ZeroDivisionError:
                    1/0
            exe_level -= 1
        if(code[i] == 'i'): memory[p % memory_length] = redirect_input()
        if(code[i] == 'o'): redirect_output(memory[p % memory_length])
        if(code[i] in "+-<>[]iobs#"):
            chars_executed += 1
        if(chars_executed >= max_chars_execute):
            # print("execute:KILL: counter == ", chars_executed, sep='')
            routput = max_output

            exe_level = 0
            1/0 #kill
        i += 1
    if(exe_level == 0 and dbg >= 3): print("execute:   { "+memory_str(memory, p, executing_char='o'), "} counter ==", chars_executed)
    routput = memory[p % memory_length]

def test_main_execute():
    prog = [
        "ib>--o",
        [
            ['',[]],
            [
                "-->++<",
                []
            ]+
            [['',[]]]*4
        ]
    ]
    execute(prog)
    print(memory_str(memory, p=p, marker='*'))

# test_main_execute()
# exit(0)

# def wrap(var, min_range=0, max_range=memory_length):
#     if(min_range == max_range):
#         return min_range
#     if(min_range > max_range):
#         min_range, max_range = max_range, min_range
#     while(var < min_range):
#         var += (max_range - min_range)
#     while(var > max_range):
#         var -= (max_range - min_range)
#     return var

def get_fitness(prog, precision=20):
    if(dbg >= 2):
        print("get_fitness(", print_arr(prog, line_break=''), ")", sep='')
    global random_input, chars_executed, rinput, memory
    prev_random_input = random_input
    random_input = True
    varianz = 0
    differences = 0
    i = min_input
    while(i < min_input + precision):
        rinput = i
        memory = [0] * memory_length
        chars_executed = 0
        if(dbg >= 3): print("get_fitness:", ls(level), "i == ", f(i, 2), ", memory: ", memory_str(memory, -1), sep='')
        if(dbg == 2): print('+', end='|')
        try:
            execute(prog)
        except ZeroDivisionError:
            return 0
        normal = formula(rinput)
        d = abs(routput - normal)
        differences += d
        varianz += d**2
        if(dbg >= 2): print('\n', "get_fitness: i == ", f(rinput), " o == ", f(routput), " d == ", f(d), " D == ", f(differences), " V == ", f(varianz), sep='')
        i += 1
    if(dbg == 3): print()
    deviation = differences / precision
    std_deviation = (varianz / precision)**0.5
    if(dbg >= 3): print("get_fitness: std deviation == sqrt(", varianz, " / ", precision, ") == ", std_deviation, sep='')
    random_input = prev_random_input
    try:
        if(True or fitness_mode == "length"):
            l_part = (
                len(to_str(prog)) - 0 #number that is subtracted might be an expected minimal string length
            )/300
        else:
            l_part = 0
        return round(
            100/(
                std_deviation + l_part
            )
        , 5)
    except ZeroDivisionError: #ideal std_deviation and length: both 0
        print("get_fitness:Ideal program with deviation of 0: ", print_arr(prog, auto_print=False))
        inp = input(
            "[ENTER] for it to be kept for shortening, [x] to go on, removing this from the population"
        ).upper()
        # return -1
        if inp == 'X':
            1/0 #kill
        else:
            'A'[2] #killing differently => kept in population

#@test@file@utils@func@shift
# print(shift([0, 2, 1], [-1, 1, 2]))
# exit(0)

def random_shift():
    rights = []
    adds = [-abs(non_zero_get_table_gaussian())]
    i = 0
    while(i < 20 and randint(0, 100) > 40):
        rights += [randint(1, 4)]
        adds += [non_zero_get_table_gaussian()]
    return shift(rights, adds)

def random_copy():
    result = ['c<c',[['',[]], ['',[]], ['',[]]]]
    rights = [-1]
    first = abs(non_zero_get_table_gaussian())
    adds = [-first, +first]
    i = 0
    while(i < 20 and randint(0, 100) > 40):
        rights += [randint(1, 4)]
        adds += [non_zero_get_table_gaussian()]
    result[1][0] = shift(rights, adds)
    # result[0] += '<'
    result[1][2] = shift([1], [-first, +first])
    return result

#@test@file@main@func@random_shift
# for i in range(0, 20):
#     print(random_shift())
# exit(0)

#@test@file@main@func@random_copy
# for i in range(0, 20):
#     print(random_copy())
# exit(0)

#comparison function
def formula(i):
    # return (i % 2 == 0)*100+(i % 2 == 1)*50
    # return i % 2 #i+[--]+o
    return i * i
    # return i / 15 #i--[-------->>>>---->>>>---->+>>--<<<<<<<<<<<]>--o
    # return i / 5 #i--[----->+<]>o

preset_progs = [
    [
        'i-<++b-b>o',
        [
            ['',[]],
            ['',[]],
            ['',[]],
            ['',[]],
            ['',[]],
            [
                '>+<-',
                []
            ],
            ['',[]],
            [
                '-',
                []
            ],
            ['',[]],
            ['',[]]
        ]
    ]
]

def close_bracket(string, i):
    bracket_counter = 0
    while(i < len(string)):
        if(string[i] == '['):
            bracket_counter += 1
        elif(string[i] == ']'):
            bracket_counter -= 1
        if(bracket_counter == 0):
            return i
        i += 1
    return None

#@test@file@main@func@close_bracket# string = "++[--[-+]--+]<>"
# i = 2
# print(string[i])
# print(string[close_bracket(string, i)])
# exit(0)

def make_prog(string):
    if(dbg >= 2): print("make_prog('", string, "')", sep='')
    code = ''
    blocks = []
    length = len(string);
    i = 0;
    finish = False;
    codes_pos = 0;
    while(i < length and not finish):
        nc = string[i]
        if(not nc in '+-<>[]b#io'):
            i += 1
            continue
        if(nc == '['):
            end_pos = close_bracket(string, i)
            Slice = string[i+1:end_pos]
            i = end_pos
            code += 'b'
            if(dbg >= 3):
                print(
                    "make_prog: string[", i, "] == ", nc,
                    " => code[", f(codes_pos), "] == ", code[codes_pos],
                sep='')
            blocks += [make_prog(Slice)]
        else:
            if(nc == ']' or nc == '#'):
                break
            code += nc
            if(dbg >= 3):
                print(
                    "make_prog: string[i] == ", nc,
                    " => code[", f(codes_pos), "] == ",
                    code[codes_pos],
                sep='')
            if('[' in string or 'b' in string):
                blocks += [['',[]]]
        codes_pos += 1
        i += 1
    code += '#'
    if(dbg >= 3):
        print("make_prog: result by print_arr: ")
        print_arr([code, blocks])
    return [code, blocks]

def deep_copy(arr):
    if(type(arr) != type([])):
        return arr
    else:
        result = []
        for e in arr:
            result += [deep_copy(e)]
        return result

# test = [
#     [
#         'a', 5
#     ],
#     3,
#     'ABC'
# ]
# print_arr(test)
# t_c = deep_copy(test)
# print_arr(test)
# print_arr(t_c)
# exit(0)

def mutate(prog, cutting_only=False):
    code = prog[0]
    blocks=prog[1]
    global level
    i = 1
    while(i + 5 < len_of_code):
        j = i + randint(1, 3)
        if(randint(0, 100) < 1 and not cutting_only):
            prog = generate()
            if(False in flatcopy(prog)):
                print("GOT IT: 468!")
                input()
            # code = prog[0]
            # blocks = prog[1]
            return prog
        elif(randint(0, 100) < 50 and not cutting_only):
            try:
                if(dbg >= 1):
                    print("mutate:", ls(level),"pre:", print_arr([code,blocks], auto_print=False, line_break=''), sep='')
                    print("mutate: pre: ", to_str([code, blocks]))
                if(not 'b' in code[i:j] or randint(0, 100) > 5):
                    prog = generate(start = i, stop = j, pre_prog = [code, blocks])
                    if(False in flatcopy(prog)):
                        print("GOT IT: 481!")
                        input()
                    code = prog[0]
                    blocks = prog[1]
                elif(code[i] == 'b'):
                    level += 1
                    if(dbg >= 2): print("mutate: block changed from: ", print_arr(blocks[i], auto_print=False), sep='')
                    blocks[i] = mutate(blocks[i])
                    if(dbg >= 2): print("mutate: block changed to: ", print_arr(blocks[i], auto_print=False), sep='')
                    level -= 1
                    if(False in flatcopy(blocks)):
                        print("GOT IT: 492!")
                        input()
            except IndexError:
                None
        elif(randint(0, 100) < pushing_percent and i < len(code) - 1 and not cutting_only):
            nc = choice(random_str)
            if(not nc in ['b', 's', '#']):
                code = code[:i] + nc + code[i:]
                blocks = blocks[:i] + [['',[]]] + blocks[i:]
        elif(randint(0, 100) < cutting_percent and i > 1 and j < len(code) - 1):
            try:
                if(dbg >= 1):
                    print("mutate:", ls(level),"pre:", print_arr([code,blocks], auto_print=False, line_break=''), sep='')
                    print("mutate: pre: ", to_str([code,blocks]))
                if(not 'b' in code[i:j] or randint(0, 100) > 5):
                    code = code[:i] + code[j+1:]
                    blocks = blocks[:i] + blocks[j+1:]
                    prog = [code, blocks]
                elif(code[i] == 'b'):
                    level += 1
                    if(dbg >= 2): print("mutate: block changed from: ", print_arr(blocks[i], auto_print=False), sep='')
                    blocks[i] = mutate(blocks[i], cutting_only=True)
                    if(dbg >= 2): print("mutate: block changed to: ", print_arr(blocks[i], auto_print=False), sep='')
                    level -= 1
                    if(False in flatcopy(blocks)):
                        print("GOT IT: 468!")
                        input()
            except IndexError:
                None
        i += 1
    if(dbg >= 3):
        print("mutate: ")
        print_arr(code)
    return [code, blocks]

square = "i[->+ >+  >>+  <<<<]>[- >[-  >>>>>+  <<<<<]  >>[-   <+  <+  >>]   <[-  >+  <] <<] >>>>>>o"
# dbg = 1
# sq = make_prog(square)

# print_arr(sq)
# print(to_str(sq))
# try:
#     execute(sq)
# except ZeroDivisionError:
#     None
# print("in", chars_executed, "steps!")
# print()

# exit(0)

# sq_c = deep_copy(sq)
# sq_c = mutate(sq_c)
# print_arr(sq_c)
# print(to_str(sq_c))
# chars_executed = 0
# try:
#     execute(sq_c)
# except ZeroDivisionError:
#     None
# print("in", chars_executed, "steps!")
# exit(0)

def check_and_clean(prog, level = 0, max_level = max_level):
    if(dbg >= 4): print("check_and_clean(", code, ", ", level, ")", sep='')
    global used, used_index
    if(level == 0):
        used_index = 0
        used = [False] * memory_length
    if(dbg >= 3): print("check_and_clean: prep ",f(memory_str(used, marker="*", s1=2, s2=2, mode="bool"), 90, 90), " " + " " * level + 'l', sep='')
    pre_used = deep_copy(used)
    pre_u_i = used_index
    code = deep_copy(prog[0])
    blocks = deep_copy(prog[1])
    adding = 0
    moving = 0
    blckng = 0
    i = 0
    while(i < len(code)):
        use = used_index % memory_length
        if(code[i] == '+'):
                    used[use] = True
                    if(moving == 0):
                        adding  += 1
        if(code[i] == '-'):
                    used[use] = True
                    if(moving == 0):
                        adding  -= 1
        if(code[i] == '>'):
                    used_index  += 1
                    moving      += 1
        if(code[i] == '<'):
                    used_index  -= 1
                    moving      -= 1
        if(code[i] == 'i'):
                    used[use] = True
        if(not used[use] and code[i] == 'o'):
                    if(dbg >= 2): print("check_and_clean: exit:'o'")
                    used = deep_copy(pre_used)
                    used_index = pre_u_i
                    return False
        if(not used[use] and code[i] in ['b', 's']):
                    if(dbg >= 2): print("check_and_clean: remove:'bs'")
                    code = set_at(code, i, ' ')
                    blocks[i] = ['',[]]
        elif(code[i] in ['b', 's']):
                    if(dbg >= 3): print("check_and_clean: entering block [", print_arr(blocks[i], auto_print=False), "] at ", i, " in ", code, sep='')
                    if(level+1 < max_level+1):
                        blocks[i] = check_and_clean(blocks[i], level+1)
                        if(blocks[i] == ['',[]] or blocks[i] == False):
                            code = set_at(code, i, " ")
                            blocks[i] = ['',[]]
                    if(code[i] != " "):
                        used[use] = False
                        blckng      += 1
        use = used_index % memory_length
        if(dbg >= 2): print(
            "check_and_clean: ",
            f("'"+code+"'", 25, 25), "["+f(i, 3)+"] == ",
            code[i]+" => ", f("", 5, 5),
            f(memory_str(used, p=use, executing_char=code[i], marker="*", s1=2, s2=2, mode="bool"), 60, 60),
            " " + " " * level + 'l',
        sep='')
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
            "check_and_clean: ",
            "level == ", level,
            ", adding == ", adding,
            ", moving == ", moving,
            ", blocks == ", blckng,
        sep='')
    if(result):
        if(dbg >= 3): print(
            "check_and_clean: ",
            "used_cells of check_executable: \n",
            f(memory_str(used, p=use, marker="*", s1=2, s2=4), 89, 89),
            " '", code, "'",
        sep='')
        return [code, blocks]
    else:
        used = deep_copy(pre_used)
        used_index = pre_u_i
        return False #['',[]]

def test(string):
    prog = make_prog(string)
    times = get_int_input(prompt = "how many times testing the code: ")
    dbg = 3
    for i in range(times):
        execute(prog)
    dbg = 0

def visualize(prog, i_rng=[0, 100, 1], o_rng=[0, 100], turtle=True):
    if turtle:
        from turtle import goto, ht, speed, delay, pencolor, pu, pd
    global random_input, chars_executed, rinput
    prev_random_input = random_input
    random_input = True
    po, pn = 0, 0
    for i in range(i_rng[0], i_rng[1], i_rng[2]):
        chars_executed = 0
        rinput = i
        try:
            execute(prog)
        except ZeroDivisionError:
            None
        o = map(routput, o_rng[0], o_rng[1], 0, 150)
        n = map(formula(i), o_rng[0], o_rng[1], 0, 150)
        if not turtle:
            print(
                ' '*int(min(o, n)) +
                '|'*(n < o)+'#'*(o <= n) +
                ' '*int(abs(o - n)) +
                '|'*(n > o)+'#'*(o >= n),
                "prog(", i, ") == ", routput,
                "F(",i,") == ",formula(i)
            )
        if turtle:
            pu()
            goto(i, po)
            pd()
            pencolor(100, 0, 0)
            goto(i, o)
            pu()
            goto(i, pn)
            pd()
            pencolor(0, 100, 0)
            goto(i, n)
        po = o
        pn = n
    random_input = prev_random_input

def generation(progs=[]):
    global perfect_progs, good_progs
    nprogs = []
    fit = []
    i = 0
    while(i < 10):
        try:
            nprogs += [deep_copy(progs[i])]
        except IndexError:
            nprogs += [generate()]
        if(dbg >= 1): print("generation: progs[", f(i, 2), "]: ", to_str(nprogs[i]), sep='')
        # print_arr(progs[i])
        try:
            fit += [get_fitness(nprogs[i])]
            if(fit[i] > good_progs_cap_fitness):
                fit[i] = -1
                good_progs += [nprogs[i]]
        except ZeroDivisionError:
            fit += [-1]
            perfect_progs += [nprogs[i]]
        except IndexError:
            fit += [100/len(to_str(prog))]
            fitness_mode = "length"
            good_progs += [nprogs[i]]

        print_arr(nprogs[i])
        i += 1
    if(dbg >= 1): print("generation: fitness list:", fit)
    return [nprogs, fit]

def select(progs, fitness):
    nprogs = []
    i = 0
    while(i < len(progs) // 2):
        fittest = fitness.index(max(fitness))
        nprogs += [deep_copy(progs[fittest])]
        nprogs += [deep_copy(progs[fittest])]
        fitness[fittest] = 0
        i += 1
    if(len(nprogs) < len(progs)):
        i = len(nprogs)
        while(i < len(progs)):
            nprogs += [generate()]
            i += 1
    return nprogs

# prog = [
#     'ib<--b>>>> >+b< <+>o',
#         [std]*1 +
#         [['------', []]] +
#         [std]*3 +
#         [[
#             '->-b>>>++b-<-< -<<-',
#                 [std]*3 +
#                 [[
#                     '>+b     << -b <<->>',
#                         [std]*2 +
#                         [['-', []]] +
#                         [std]*9 +
#                         [['>>>++++<<++<-<-<+>-', []]] +
#                         [std]*6
#                 ]] +
#                 [std]*5 +
#                 [[
#                     '+b--b>+>+<b++b-b->b',
#                         [std]*1 +
#                         [['-', []]] +
#                         [std]*2 +
#                         [['-', []]] +
#                         [std]*5 +
#                         [['-', []]] +
#                         [std]*2 +
#                         [['-', []]] +
#                         [std]*1 +
#                         [['-', []]] +
#                         [std]*2 +
#                         [['-', []]]
#                 ]] +
#                 [std]*9
#         ]] +
#         [std]*7 +
#         [['->>>>------->>>+<<<<<<<', []]] +
#         [std]*6
#    ]

if False:
    dbg = 3
    dbg = 0
    # check_executable(prog[0], 0)
    # check_and_clean(prog)
    # execute(prog)
    # print(to_str(prog))
    prog = mutate(prog)
    print_arr(prog, line_break='\n')
    print(to_str(prog))
    # input()
    visualize(prog)
    exit(0)

if False: #foldability
    #@test@file@main@func@generate
    dbg = 1
    # prog = generate()
    prog = [
        'ib<<+b>>>> >+b< <+>o',
            [std]*1 +
            [['------', []]] +
            [std]*3 +
            [['-----', []]] +
            [std]*7 +
            [['->>>>------->>>+<<<<<<<', []]] +
            [std]*7
    ]
    # print("+"*120)
    #print(check_executable(prog[0], 0, 4))
    #print("+"*120)
    # prog = check_and_clean(prog)
    print("+"*120)
    print("result →(l.701):")
    print_arr(prog)
    # print("+"*120)
    # np = generate(3, 3, prog)
    # print("+"*120)
    # print_arr(np)
    # print("+"*120)
    # exit(0)
    np = generate(3, 4, prog)
    print("+"*120)
    print("result →(l.710):")
    print_arr(np)
    print("+"*120)
    # exit(0)
    # np = generate(3, 5, prog)
    # print("+"*120)
    # print_arr(np)
    # print("+"*120)
    # exit(0)
    random_str = "+-<>b"
    np = generate(3, 6, prog)
    print("+"*120)
    print_arr(np)
    print("+"*120)
    exit(0)

if False:
    # prog = make_prog(square)
    prog = make_prog("i[---->+++<]>o")
    # dbg = 2
    # prog = generate()
    # prog = ['i<<+>+<<+bs<<<--o', [std]*9 + [['->>>>+++++++++++++<<<<', []]] + [std]*6]
    print("A"+"-"*120)
    # print_arr(prog, auto_print=True)
    check = check_and_clean(prog, 0)
    prog = check
    print("B"+"-"*120)
    # dbg = 1
    # print_arr(prog, auto_print=True)
    # print("-"*120)
    # dbg = 0
    execute(prog)
    print("C"+"-"*120)
    print(to_str(prog))
    print("D"+"-"*120)
    prog = mutate(prog)
    print("E"+"-"*120)
    print(to_str(prog))
    print("F"+"-"*120)
    # print(check_and_clean(prog[1][1], 1))
    # print("G"+"-"*120)
    # check = check_and_clean(prog[1][7], 1)
    # print(check)
    # if(not check): prog[1][2] = ['',[]]
    # print("H"+"-"*120)
    # dbg = 1
    # print_arr(prog, auto_print=True)
    # dbg = 3
    # print("I"+"-"*120)
    # print(to_str(prog))
    # print("J"+"-"*120)
    # random_input = False
    # rinput = 1
    # execute(prog)
    exit(0)

# random_str = "+++-<>ss#"
# dbg = 1
# prog = ['',[]]
# while(input() != "G"):
#     prog = generate()
#     print_arr((prog))
#     print(to_str(prog))
# print_arr(prog, auto_print=True)
# print(to_str(prog))
# execute(prog)
# exit(0)

# prog = generate()
# print_arr(prog, auto_print=True)
# execute(prog)
# fit = get_fitness(prog)
# print(fit)

# prog2 = preset_progs[0]
# print_arr(prog2, auto_print=True, line_break='')
# fit2 = get_fitness(prog2)
# print(fit2)
# exit(0)

# dbg  = 0
# string = "i+[--]+o"
# string = "i[---->++++++<]>o"
# string = "i-[->>++>>>>++++++++>>>>--->>>>--------------->>>------->>->>>>++++>>>+++++++++++++++<<<<<<<<<<<<<<<<<<<<<<<<<<]>>--[->++++++++<]>+o"
# test(string)
# exit(0)

# prog = make_prog("i--[-------->>>>---->>>>---->+>>--<<<<<<<<<<<]>--o")
# visualize(prog)
# exit(0)
# prog = make_prog(string)
# dbg = 3
# execute(prog)
dbg = 0
# input()
prog = generate()
fit = get_fitness(prog)
# prog2 = make_prog(string)
# prog2 = generate()
# fit2 = get_fitness(prog2)
print(
    "fitness(prog ",
    f(to_str(prog),100),
    ") == ",
    f(fit, 12), "  ",
    "#"*int(fit/100),
sep='')
# print("fitness(prog2 ", f(to_str(prog2),100), ") == ", f(fit2, 12), "  ", "#"*int(fit2/100), sep='')

while fit < 3000:
    dbg = 0
    # dbg = get_int_input("dbg mode: ")
    nprog = mutate(deep_copy(prog))
    # nprog2 = mutate(deep_copy(prog2))
    # for c in range(100):
        # i = randint(0, len(nprog[0]))
        # j = randint(0, len(nprog2[0]))
        # if(i < len(nprog[0]) and j < len(nprog2[0])):
        #     if(nprog[0][i] == 'b' and nprog2[0][j] == 'b'):
        #         j_bl = deep_copy(nprog2[1][j])
                # nprog2[1][j] = deep_copy(nprog[1][i])
                # nprog[1][i] = j_bl
    try:
        nfit = get_fitness(nprog)
        # nfit2 = get_fitness(nprog2)
    except ZeroDivisionError:
        #thrown bc of a perfect prog
        # print("ZeroDivisionError, had a perfect prog!")
        continue
    except IndexError:
        #thrown bc of a perfect prog and the users decision
        print("IndexError, fitness_mode == 'length'")
        fitness_mode = "length"
        fit = get_fitness(prog)
        nfit = get_fitness(nprog)
        # fit2 = get_fitness(prog2)
        # nfit2 = get_fitness(nprog2)

    if(nfit > fit):
        print("fitness(new prog ", f(to_str(nprog),100), ") == ", f(nfit, 12), "  ", "#"*int(nfit/100), sep='')
        prog = deep_copy(nprog)
        fit = nfit

    # if(nfit2 > fit2):
    #     print("fitness(new prog2", f(to_str(nprog2),100), ") == ", f(nfit2, 12), "  ", "#"*int(nfit2/100), sep='')
    #     prog = deep_copy(nprog2)
    #     fit2 = nfit2
    # input()

print(to_str(prog))
print_arr(prog)

exit(0)

progs = []
while(True):
    gen = generation(progs)
    progs = gen[0]
    fitness = gen[1]
    i = 0
    while i < len(progs):
        print("progs[", f(i), "]: ", f(to_str(progs[i]),50), ", fit == ", f(fitness[i],7), sep='')
        # print_arr(prog, auto_print=True)
        i += 1
    progs = select(progs, fitness)
    i = 0
    while(i < len(progs)):
        mutate(progs[i])
        i += 1
    input()
    # exit(0)
