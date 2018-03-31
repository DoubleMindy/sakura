#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Crypto.Hash import keccak
'''
 ВОПРОСЫ:
 Хороша ли RawSHAKE?
 Как выбрать B?
 Чем дополнять последний блок? (нулями?)
 Метка для последних блоков выбирается странно в примерах.
 Что делать при m = 0? Как выбирать j?
'''


# Внутренняя функция RawSHAKE128 для построения древовидного режима (Keccak[c=256)(M||11))
def inner_func(mes):
    keccak_hash = keccak.new(digest_bits=256)
    mes = bytes(mes, 'utf-8') + b'11'
    keccak_hash.update(mes)
    return keccak_hash.hexdigest()


# Разбиение на пары:
def chunks(x, n):
    for i in range(0, len(x), n):
        yield x[i:i + n]


# Построение самого дерева через внутреннюю функцию:
def m_tree(x):
    sub_t = []
    for i in chunks(x, 2):
        if len(i) == 2:
            h = inner_func(i[0])+inner_func(i[1])
        else:
            h = i[0]
        sub_t.append(h)
    if len(sub_t) == 1:
       return sub_t[0]
    else:
       return m_tree(sub_t)


msg = "INFORMATION THEORY,TIMOKHIN ILYA 151"
B = 4  # Как выбрать B?
M = [msg[i:i+B] for i in range(0, len(msg), B)]
while len(M[-1]) < B:
    M[-1] += '0'  # Чем дополнить?
l = 0
D = []
res_tree = []
m_prev = len(M)
j_prev = len(bin(m_prev)[2:])
# Простановка первых нескольких меток:
for i in range(0, 2**(j_prev-1)):
    p = bin(i)[2:]
    label = (j_prev - len(p)) * '0' + p
    D.append(label)
m_cur = 2
while m_cur > 1:
    l += 1
    m_cur = m_prev - 2**(j_prev-1)
    # Случай m < 1:
    if m_cur < 1:
        D.append('1')
        break
    j_cur = len(bin(m_cur)[2:])
    s_1 = 2**(j_prev - 1)
    s_2 = s_1 + 2**(j_cur - 1) - 1
    index = 0
    for i in range(s_1, s_2+2):
        if l >= j_cur:
            label = '1' * l
        else:
            p = bin(index)[2:]
            label = '1' * l + (j_cur - len(p)) * '0' + p
        D.append(label)
        index += 1
    m_prev = m_cur
    j_prev = j_cur

print(msg)
res_dict = dict(zip(M, D))
print(res_dict)
print("Result is: ", m_tree(list(res_dict.keys())))

