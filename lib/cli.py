# lib/cli.py
import click
from machine import (
    load_song,
    add_song,
    remove_song,
    exit_program,
    get_all_songs,
    get_songs_by_artist,
    get_songs_by_genre,
    view_queue,
    view_up_next,
)

# CYAN = "\033[96m"
CYAN_BOLD = "\033[96;1m"
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
            print("1 entered")
        elif choice == "2":
            print("2 entered")
        elif choice == "3":
            song_id = input("Enter song id: ")
            singer_name = input("Who is singing?: ")
            add_song(song_id, singer_name)
        elif choice == "4":
            singer_name = input("Who to remove?: ")
            remove_song(singer_name)
        elif choice == "5":
            view_queue()
        elif choice == "6":
            view_up_next()
        elif choice == "7":
            get_all_songs()
        elif choice == "8":
            # Get user input for the song title
            artist = input("Enter artist name: ")
            get_songs_by_artist(artist)
        elif choice == "9":
            # Get user input for the song title
            genre = input("Enter genre: ")
            get_songs_by_genre(genre)
        elif choice == "0":
            exit_program()
        else:
            print("Invalid choice")


def menu():
    print("Choose an option:")
    print("x. Load next song")
    print("x. Pause current song")
    print("3. Add song to queue")
    print("4. Remove song from queue")
    print("5. View queue by song")
    print("6. View queue by singer")
    print("7. View all songs")
    print("8. View songs by artist")
    print("9. View songs by genre")
    print("0. Exit")


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
           {CYAN_BOLD}a Python CLI project by @eburdekin{RESET}                                                                                                                              
              """
    )


if __name__ == "__main__":
    main()
