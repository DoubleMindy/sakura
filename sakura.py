#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Crypto.Hash import keccak


def sakura(msg):
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
                h = inner_func(i[0])
            sub_t.append(h)
        if len(sub_t) == 1:
            return sub_t[0]
        else:
            return m_tree(sub_t)

    B = 4  # Как выбрать B?
    M = [msg[i:i+B] for i in range(0, len(msg), B)]
    l = 0
    D = {}
    m_prev = len(M)
    j_prev = len(bin(m_prev)[2:])
    # Простановка первых нескольких меток:
    for i in range(0, 2**(j_prev-1)):
        p = bin(i)[2:]
        label = (j_prev - len(p)) * '0' + p
        D.update({M[i] : label})
    if m_prev == 2**(j_prev - 1):
        m_cur = 0
    else:
        m_cur = 2
    # Указатель позиции для добавления элемента в словарь:
    pointer = 2**(j_prev-1)
    # Проверка на избежание коллизий меток:
    checker = ''
    while m_cur > 1:
        l += 1
        m_cur = m_prev - 2**(j_prev-1)
        j_cur = len(bin(m_cur)[2:])
        s_1 = 2**(j_prev - 1)
        s_2 = s_1 + 2**(j_cur - 1) - 1
        index = 0
        for i in range(s_1, s_2 + 1):
            p = bin(index)[2:]
            if j_cur == 1:
                label = l * '1'
            else:
                label = '1' * l + (j_cur - len(p)) * '0' + p
                if (len(checker) <= len(label)) and (l > 1):
                    label = '1' * l + (j_cur - len(p) - 1) * '0' + p
            D.update({M[pointer]: label})
            index += 1
            if pointer + 1 < len(M):
                pointer += 1
        checker = M[pointer - 1]
        m_prev = m_cur
        j_prev = j_cur

    for k, v in D.items():
        print(k, ':', v)
    return m_tree(list(D.keys()))


if __name__ == "__main__":
    test = "Курсовая работа, теория информации (Тимохин Илья СКБ151)"
    print("Result is: ", sakura(test))

