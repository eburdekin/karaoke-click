import typer
from rich.console import Console
from rich.prompt import Prompt, IntPrompt


from machine import (
    add_song,
    remove_song,
    load_song,
    view_queue,
    view_all_songs,
    get_songs_by_title,
    get_songs_by_artist,
    get_songs_by_genre,
    add_new,
    remove_new,
    exit_program,
)

from models.song import CONN, CURSOR

app = typer.Typer()
console = Console()

update_style = "color(6)"
pink = "color(5)"


def display_title_card():
    console.print("\n")
    console.print("*" * 58)
    console.print(
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
   
{"*" * 58}"""
    )
    console.print("          a Python CLI project by @eburdekin", style="color(6)")


@app.callback(invoke_without_command=True)
def main():
    display_title_card()
    menu()


def format_menu():
    options = [
        ("1", "Add song", "Your Playlist"),
        ("2", "Remove song", "Your Playlist"),
        ("3", "Load next song", "Your Playlist"),
        ("4", "View next up", "Your Playlist"),
        ("5", "View all", "Song Library"),
        ("6", "View by title", "Song Library"),
        ("7", "View by artist", "Song Library"),
        ("8", "View by genre", "Song Library"),
        ("9", "Add new song", "Song Library"),
        ("10", "Delete song", "Song Library"),
        ("0", "Exit", "Exit"),
    ]

    menu_text = ""
    current_header = ""
    for option, description, header in options:
        if header != current_header:
            menu_text += f"\n[color(5)]{header}[/color(5)]\n"
            current_header = header
        menu_text += f"[bold color(6)]{option}[/bold color(6)]. {description}\n"

    return menu_text


@app.command()
def menu():
    while True:
        console.print(format_menu())

        choice = IntPrompt.ask("What'll it be?")
        if choice == 1:
            add_song_command()
        elif choice == 2:
            remove_song_command()
        elif choice == 3:
            load_song()
        elif choice == 4:
            view_queue()
        elif choice == 5:
            view_all_songs()
        elif choice == 6:
            title_input = Prompt.ask("Enter song title")
            title = title_input.title()
            get_songs_by_title(title)
        elif choice == 7:
            artist_input = Prompt.ask("Enter artist name")
            artist = artist_input.title()
            get_songs_by_artist(artist)
        elif choice == 8:
            genre_input = Prompt.ask("Enter genre")
            genre = genre_input.title()
            get_songs_by_genre(genre)
        elif choice == 9:
            add_new_command()
        elif choice == 10:
            remove_new_command()
        elif choice == 0:
            exit_program()
            break
        else:
            console.print(
                "Invalid choice. Try again!",
                style="color(2)",
            )


def song_id_exists(song_id, conn):
    CURSOR.execute("SELECT COUNT(*) FROM singers WHERE song_id = ?", (song_id,))
    count = CURSOR.fetchone()[0]
    return count > 0


def add_song_command():
    while True:
        song_id = Prompt.ask("Enter song ID")

        if song_id_exists(song_id, CONN):
            print("Song ID already exists. Please enter a different one.")
        else:
            break

    singer_name = Prompt.ask("Who is singing? ")
    add_song(song_id, singer_name)


def remove_song_command():
    singer_name = Prompt.ask("Take this name off the list")
    remove_song(singer_name)
    # console.print(f"{singer_name} removed from queue!", style=update_style)


def add_new_command():
    title = Prompt.ask("Enter title")
    artist = Prompt.ask("Enter artist")
    genre = Prompt.ask("Enter genre")
    lyrics = Prompt.ask("Enter lyrics")
    add_new(title, artist, genre, lyrics)


def remove_new_command():
    song_id = Prompt.ask("Enter song ID")
    remove_new(song_id)


if __name__ == "__main__":
    app()
