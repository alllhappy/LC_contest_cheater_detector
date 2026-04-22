import pyfiglet

CHARS=75
def printWelcome():
    print('#'.center(CHARS,'#'))
    print()
    print(pyfiglet.figlet_format("WELCOME",font="big",))
    print(pyfiglet.figlet_format("TO",font="big"))
    print(pyfiglet.figlet_format("LEETCODE",font="big"))
    print(pyfiglet.figlet_format("CONTEST",font="big"))
    print(pyfiglet.figlet_format("CHEATER",font="big"))
    print(pyfiglet.figlet_format("DETECTOR",font="big"))
    print('#'.center(CHARS,'#'))
    print("\n")


def printExit():
    print('#'.center(CHARS,'#'))
    print("\n")
    print(pyfiglet.figlet_format("BYE BYE",font="big"))
    print('#'.center(CHARS,'#'))
    print("\n")