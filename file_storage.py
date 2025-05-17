
def write_to_file(d, name = "storage.j"):
    with open(name, "w") as file:
        for key, value in d.items():
            file.write(f"{key}: {value}\n")


def read_from_file(file_name = "storage.j"):
    d = {}
    with open(file_name, "r") as file:
        line = file.readline()
        while line != None and line != "":
            stuff = line.split()
            key = stuff[0][:-1]
            val = stuff[1]
            d[key] = val
            line = file.readline()
    return d


# write_to_file({"justin": 18, "simon": 15})
# n = read_from_file()
# print(n)

# n["simon"] = 16

# write_to_file(n)
