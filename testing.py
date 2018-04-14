#ALL TESTS FOR ALL ABSOLVED FUNCTIONS IN ORDER ACCORDING TO THEIR FILE
#EXPAMPLE:
#file [NAME].py
#@test@file@NAME
#function def [FUNC]
#@test@file@FILE@func@FUNC

#@test@file@formatting
#@test@file@formatting@func@f
def test_formatting_f():
    from formatting import f
    print("testing: f", f(  123,   5, 7))
    print("testing: f", f( 1234,   5, 7))
    print("testing: f", f(12345,   5, 7))
    print("testing: f", f(123456,  5, 7))
    print("testing: f", f(1234567, 5, 7))
    print("testing: f", f(12345678,5, 7))
#@test@file@formatting@func@ls
def test_formatting_ls():
    from formatting import ls
    level = 5
    print("testing: ls, level == ", level)
    print("testing: ls:'", ls(level), "'", sep='')
#@test@file@formatting@func@memory_str
def test_formatting_memory_str():
    from formatting import memory_str
    print("testing: memory_str",
        memory_str(
            [1, 1, 3, 0, 1, 0, 0, -2],
            p=2,
            executing_char='E',
            sep='|',
            marker='*',
            s1=3,
            s2=5,
            mode="bool",
            filter_0=True
        )
    )
#@test@file@formatting@func@to_str
def test_formatting_to_str():
    from formatting import to_str
    print(to_str(
        [
            "ib>--o",
            [
                ['',[]],
                [
                    "-->+++<",
                    [
                        ['',[]],
                        ['',[]],
                        ['',[]],
                        ['',[]]
                    ]
                ] + [['',[]]*4]
                # ['',[]],
                # ['',[]],
                # ['',[]],
                # ['',[]]
            ]
        ],
        level=0,
        dbg=4
    ))

#@test@file@utils@func@ALL!
def test_utils_all():
    from utils import isint, set_at, get_int_input
    print("testing: isint:", isint([5]))
    print("testing: set_at:", set_at("ABS!", 2, "C"))
    print("testing: get_int_input:", get_int_input(prompt="GIVE ME IINNTT!!", error_message="FUCK YOU, INT I TOLD!"))

# #@test@file@utils@func@set_at
# def test_utils_set_at():
#     from utils import set_at
    # print("testing: set_at:", set_at("ABS!", 2, "C"))

#@test@file@formatting@func@print_arr
def test_formatting_print_arr():
    from formatting import print_arr, pa_ls
    print_arr(
        [
            [
                'a', 5
            ],
            3,
            'ABC',
            ['',[]],
            ['',[]],
            ['',[]]
        ],
        lvl=0,
        max_level=10,
        str_quote=True,
        type_print=False,
        line_break='',
        auto_print=True,
        dbg=4
    )

#@test@file@check@func@check_executable
def test_check_check_executable():
    from check import check_executable
    code = "+>-<-->"
    level = 1
    dbg = 4
    result = check_executable(
        code=code,
        level=level,
        dbg=dbg
    )
    print("-"*120)
    print("check_executable(", code, ", ", level, ", ", dbg, ") == ", result, sep='')
    print("-"*120)
    code = "->-<-->"
    level = 0
    dbg = 4
    result = check_executable(
        code=code,
        level=level,
        dbg=dbg
    )
    print("-"*120)
    print("check_executable(", code, ", ", level, ", ", dbg, ") == ", result, sep='')
    code = "->b<-->"
    level = 0
    dbg = 4
    result = check_executable(
        code=code,
        level=level,
        dbg=dbg
    )
    print("-"*120)
    print("check_executable(", code, ", ", level, ", ", dbg, ") == ", result, sep='')
