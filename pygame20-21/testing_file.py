

"""
liste1 = [(1,2), (10,4)]

for a, b in enumerate(liste1):
    print(a)
    print(b)


a = 28/10

print(int(a))



sheet_name = "super_thomas"

file_name = "".join((sheet_name, ".png"))

print(file_name)

"""

liste = ["albert", "beate", "beate", "catrine"]

for i, navn in sorted(enumerate(liste), reverse = True):
    print(i)
    if navn == "beate":
        liste.pop(i)

print(liste)