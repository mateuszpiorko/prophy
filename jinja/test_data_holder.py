import os
import pytest
from data_holder import DataHolder as dh

def test_of_sorter():
    dic = {"CONST_A": "CONST_B", "CONST_B": "5", "CONST_C": "4"}
    l = ['CONST_B', 'CONST_A', 'CONST_C']
    assert l == dh().sort_list(dic)

def test_of_sorter_2():
    dic = {"C_A" : "C_B", "C_B" : "C_C", "C_C" : "5"}
    l = ['C_C', 'C_B', 'C_A']

    assert l == dh().sort_list(dic)

def test_of_sorter_3():
    dic = {"C_A1" : "C_B", "C_A2" : "C_B" , "C_B" : "5"}
    l = ['C_B', 'C_A2', 'C_A1']
    assert l == dh().sort_list(dic)

def test_of_sorter_4():
    dic = {"C_C" : "5", "C_B":"C_C", "C_A1":"C_B", "C_A2":"C_B"}
    l = ['C_C', 'C_B', 'C_A2', 'C_A1']
    assert l == dh().sort_list(dic)

def test_of_sorter_5():
    dic = {  "C_C" : "C_A + C_B" , "C_A":"5", "C_B":"3"}
    l = ['C_B', 'C_A', 'C_C']
    assert l == dh().sort_list(dic)

def test_of_sorter_6():
    dic = {"C_C" : "C_A + C_B" , "C_A":"5", "C_B":"3"}
    l = ['C_B', 'C_A', 'C_C']
    assert l == dh().sort_list(dic)

def test_of_sorter_7():
    dic = {"C_A":"5", "C_B":"3", "C_C" : "C_A + C_B"}
    l = ['C_B', 'C_A', 'C_C']
    assert l == dh().sort_list(dic)

def test_of_ecev_of_file():
    from dic import dic

    sort = dh().sort_list(dic)

    f = "";

    for x in sort:
        f += x + " = " + dic[x] + "\n"

    try:
        exec f
    except NameError, e:
        pytest.fail(e)
