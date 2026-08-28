a = float(input("what is the length of your zander in centimeters? " ))
if float(a) <= 42:
    print(f"You should release your zander, the fish is {42 - float(a)} centimeters below the limit")
else:
    print("You can keep your zander")