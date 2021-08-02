# Замена символов на цифры
for k in range(1, 31):
    with open(f"{k}", "rt") as f:
        data = f.readlines()

    new_data = []
    for i in range(len(data)):
        new_data.append([])
        for j in range(len(data[i]) - 1):
            if data[i][j] == ".":
                new_data[i].append("0")
            elif data[i][j] == "@":
                new_data[i].append("1")
            elif data[i][j] == "#":
                new_data[i].append("2")
            elif data[i][j] == "%":
                new_data[i].append("3")
            elif data[i][j] == "~":
                new_data[i].append("4")
            elif data[i][j] == "-":
                new_data[i].append("5")
        if i != len(data) - 1:
            new_data[i].append("\n")        

    with open(f"{k}.txt", "wt") as f:
        for i in range(len(new_data)):
            f.writelines(new_data[i])


# Уменьшение количества символов в каждой строке и столбце вдвое
for k in range(1, 31):
    with open(f"{k}.txt", "rt") as f:
        data = f.readlines()

    new_data = []
    for i in range(0, len(data), 2):
        new_data.append([])
        for j in range(0, len(data[i]) - 1, 2):
            new_data[int(i / 2)].append(data[i][j])
        if i != len(data) - 2:
            new_data[int(i / 2)].append("\n")

    with open(f"{k}.txt", "wt") as f:
        for i in range(len(new_data)):
            f.writelines(new_data[i])

# Очищение верхней строки для отображения счёта и времени
for k in range(1, 31):
    with open(f"{k}.txt", "rt") as f:
        data = f.readlines()
    
    new_data = []
    for i in range(len(data)):
        new_data.append([])
        for j in range(len(data)):
            if i == 0:
                new_data[0].append("0")
            else:
                new_data[i].append(data[i][j])
        if i != len(data) - 1:
            new_data[i].append("\n") 

    with open(f"{k}.txt", "wt") as f:
        for i in range(len(new_data)):
            f.writelines(new_data[i])