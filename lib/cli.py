# lib/cli.py

from machine import load_song, add_song, exit_program

CYAN = "\033[96m"
# CYAN_BOLD = "\033[96;1m"
RESET = "\033[0m"


def main():
    title_card_displayed = False

    while True:
        if not title_card_displayed:
            display_title_card()
            title_card_displayed = True

        menu()
        choice = input("> ")
        if choice == "1":
            load_song()
        elif choice == "2":
            add_song()
        elif choice == "10":
            exit_program()
        else:
            print("Invalid choice")


def menu():
    print("Please choose an option:")
    print("1. Load next song")
    print("2. Add song")
    print("10. Exit the program")


def display_title_card():
    print("*" * 58)
    print(
        f"""
██╗  ██╗ █████╗ ██████╗  █████╗  ██████╗ ██╗  ██╗███████╗
██║ ██╔╝██╔══██╗██╔══██╗██╔══██╗██╔═══██╗██║ ██╔╝██╔════╝
█████╔╝ ███████║██████╔╝███████║██║   ██║█████╔╝ █████╗  
██╔═██╗ ██╔══██║██╔══██╗██╔══██║██║   ██║██╔═██╗ ██╔══╝  
██║  ██╗██║  ██║██║  ██║██║  ██║╚██████╔╝██║  ██╗███████╗
╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝
                                                         
 ███╗   ███╗ █████╗  ██████╗██╗  ██╗██╗███╗   ██╗███████╗ 
 ████╗ ████║██╔══██╗██╔════╝██║  ██║██║████╗  ██║██╔════╝ 
 ██╔████╔██║███████║██║     ███████║██║██╔██╗ ██║█████╗   
 ██║╚██╔╝██║██╔══██║██║     ██╔══██║██║██║╚██╗██║██╔══╝   
 ██║ ╚═╝ ██║██║  ██║╚██████╗██║  ██║██║██║ ╚████║███████╗ 
 ╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝╚══════╝    
   
{"*" * 58}            
           {CYAN}♫ a Python CLI project by @eburdekin ♫{RESET}                                                                                                                              
              """
    )


if __name__ == "__main__":
    main()
