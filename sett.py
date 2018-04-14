#settings

len_of_code = 20
max_level = 3
memory_length = 8 #30
min_input = 100
max_input = 1000
max_output = 2**24
random_input = False

#            add 1 | subtr 1|mov left|right  |open block|finish|shift
random_str = '+'*7 + '-'*5 + '<'*15 + '>'*22 + 'b'*2 + '#'*5 + "s"*5
random_str1 = '+'*7 + '-'*5 + '<'*15 + '>'*22 + 'b'*5 + '#'*5 #extracted from square aglorithm ('[,]' == 'b,#')
random_str2 = "+++---<<>>b#"

max_chars_execute = 1e5
mutation_percent = 10
cutting_percent = 10
pushing_percent = 10
good_progs_cap_fitness = 1000
fitness_mode = "length" #with "length", the length of the code is factored in. otherwise only the standard deviation counts
# fitness_mode = ""

std = ['',[]]
