# Добавление стены для базы для каждого уровня
for k in range(1, 31):
    with open(f"{k}.txt", "rt") as f:
        data = f.readlines()

    new_data = []

    for i in range(len(data)):
        new_data.append([])
        for j in range(len(data[i])):
            new_data[i].append(data[i][j])

    for i in range(len(new_data)):
        for j in range(len(new_data[i]) - 1):
            if i == 10 and 3 < j <= 8:
                new_data[i][j] = "0"
            if i == 11 and 4 < j <= 7:
                new_data[i][j] = "2"
            if i == 11 and (j == 4 or j == 8):
                new_data[i][j] = "0"
            if i == 12 and (j == 5 or j == 7):
                new_data[i][j] = "2"
            if i == 12 and (j == 4 or j == 6 or j == 8):
                new_data[i][j] = "0"  
             

    with open(f"{k}.txt", "wt") as f:
        for i in range(len(new_data)):
            f.writelines(new_data[i])
