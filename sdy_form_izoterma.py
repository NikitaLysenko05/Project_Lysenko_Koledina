# импорт бибилиотек
import numpy as np
import pandas as pd


def stex_matrix_to_sdy(file_stex_matrix, path_sdy):
    # считывание файла со стехиометрической матрицей
    # data = pd.read_csv(file_path, sep=" ")
    data = pd.read_excel(file_stex_matrix)
    col = []
    for i in range(data.columns.shape[0] - 1):
        col.append(data.columns[i])

    # print("Стехиометрическая матрица \n", data)
    # w - вектор столбец скоростей
    w = []
    schet = 1
    # Заполняем вектор столбец, учитываем последний столбец с обратимостью
    # Смотрим на порядок идущих друг за другом обратимостей, если реакция обратима, то переменную счетчик добавляем 1
    for i in range(len(data)):
        w_str = '('
        if data.iloc[i][data.shape[1] - 1] == 1:
            for j in range(data.shape[1] - 1):
                if data.iloc[i][j] < 0:
                    # w_str += data.columns[j] + '**' + str(abs(data.iloc[i][j])) + '*'
                    # доп уравнение по количеству вещества
                    w_str += '(' + data.columns[j] + '/Q)' + '**' + str(abs(data.iloc[i][j])) + '*'
                    # доп уравнение по количеству вещества
            w_str = 'k' + str(i + schet) + '*' + w_str
            w_str = w_str[0:len(w_str) - 1] + ')-('
            schet += 1
            for j in range(data.shape[1] - 1):
                if data.iloc[i][j] > 0:
                    # w_str += data.columns[j] + '**' + str(data.iloc[i][j]) + '*'
                    # доп уравнение по количеству вещества
                    w_str += '(' + data.columns[j] + '/Q)' + '**' + str(data.iloc[i][j]) + '*'
                    # доп уравнение по количеству вещества
            w_str = w_str[0:len(w_str) - 1] + ')'
            w_str = w_str[0:w_str.find('-') + 2] + 'k' + str(i + schet) + '*' + w_str[w_str.rfind('('):len(w_str)]
            w_str = '(' + w_str + ')'
        elif data.iloc[i][data.shape[1] - 1] == 0:
            for j in range(data.shape[1] - 1):
                if data.iloc[i][j] < 0:
                    # w_str += data.columns[j] + '**' + str(abs(data.iloc[i][j])) + '*'
                    # доп уравнение по количеству вещества
                    w_str += '(' + data.columns[j] + '/Q)' + '**' + str(abs(data.iloc[i][j])) + '*'
                    # доп уравнение по количеству вещества
            w_str = w_str[0:len(w_str) - 1] + ')'
            w_str = 'k' + str(i + schet) + '*' + w_str
            w_str = '(' + w_str + ')'
        w.append([w_str])

    f_w = open(path_sdy + 'W_izoterma.txt', 'w')  # открытие в режиме записи, если нет такого файла, то создаается
    for i in range(len(w)):
        f_w.write(w[i][0] + '\n')
    for i in range(len(col)):
        f_w.write(col[i])
        f_w.write(' ')
    # Преобразуем стехиометрическую матрицу и вектор столбец
    w = np.reshape(w, (len(w), 1))
    data = data.to_numpy().transpose()
    # print(type(data[0][0]), type(w[0][0]))
    # print(data, '\n')
    # print(w)
    # Составляем СДУ, столбец с обратимостью не учитываем
    sdy_file = []
    for i in range(len(data) - 1):
        for j in range(len(w[0])):
            result = ''
            for k in range(len(w)):
                if data[i][k] != 0:
                    if data[i][k] > 0:
                        result += str(data[i][k]) + '*' + w[k][j] + '+'
                    else:
                        result = result[0:len(result) - 1]
                        result += str(data[i][k]) + '*' + w[k][j] + '+'
            result = result[0:len(result) - 1]
            sdy_file.append(result)


    # +Доп уравнение по количеству вещества
    Q_eq = ''
    for i in range(len(sdy_file)):
        Q_eq += sdy_file[i] + '+'
    Q_eq = Q_eq[0:len(Q_eq) - 1]
    # +Доп уравнение по количеству вещества

    ###########################################################################

    # Запись в файл, в файле присутствует система СДУ и последней строкой продукты, участвующие в реакциях
    f = open(path_sdy + 'sdy_izoterma.txt', 'w')  # открытие в режиме записи, если нет такого файла, то создаается
    for i in range(len(sdy_file)):
        f.write(sdy_file[i] + '\n')
    ####################
    # f.write(T_eq + '\n')
    f.write(Q_eq + '\n')
    ####################
    for i in range(len(col)):
        f.write(col[i])
        f.write(' ')
    f.write('\n')


# stex_matrix_to_sdy(r'ПАУ\stex_matrix_pay.xlsx')
