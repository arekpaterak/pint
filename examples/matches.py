i: int = 1 

if i > 10:
    print("if")

match i:
    case 10:
        print("case")
    case 0:
        print("another case")
    case _:
        print("default")
