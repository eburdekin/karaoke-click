# lib/cli.py

from KaraokeMachine import KaraokeMachine


def main():
    machine = KaraokeMachine()

    while True:
        menu()
        choice = input("> ")
        if choice == "0":
            machine.exit_program()
        elif choice == "1":
            machine.load_song()
        else:
            print("Invalid choice")


def menu():
    print("*" * 50)
    print("Welcome to the Karaoke Machine! Please choose an option:")
    print("0. Exit the program")
    print("1. Load next song")
    print("*" * 50)


if __name__ == "__main__":
    main()
