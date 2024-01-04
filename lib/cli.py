# UI - menu formatting, user input handling

import typer
from rich.console import Console
from rich.prompt import Prompt, IntPrompt, Confirm

# Import helper functions to access Song/Singer classes
from helpers import (
    add_song_to_playlist,
    remove_song_from_playlist,
    load_song,
    view_all_playlist,
    view_all_library,
    view_library_by_id,
    view_library_by_title,
    view_library_by_artist,
    view_library_by_genre,
    add_song_to_library,
    remove_song_from_library,
    exit_program,
    song_id_exists_in_singers,
    song_id_exists_in_songs,
)

from models.song import (
    CONN,
    CURSOR,
    error_style,
    callout_style,
    update_style,
)

app = typer.Typer()
console = Console()

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
        ("4", "View all", "Your Playlist"),
        ("5", "View all", "Song Library"),
        ("6", "View by id", "Song Library"),
        ("7", "View by title", "Song Library"),
        ("8", "View by artist", "Song Library"),
        ("9", "View by genre", "Song Library"),
        ("10", "Add new song", "Song Library"),
        ("11", "Delete song", "Song Library"),
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
            view_all_playlist()
        elif choice == 5:
            view_all_library()
        elif choice == 6:
            library_by_id_command()
        elif choice == 7:
            library_by_title_command()
        elif choice == 8:
            library_by_artist_command()
        elif choice == 9:
            library_by_genre_command()
        elif choice == 10:
            add_new_command()
        elif choice == 11:
            remove_new_command()
        elif choice == 0:
            exit_program()
            break
        else:
            console.print(
                "Invalid choice. Try again!",
                style="color(2)",
            )


# Handle user input for editing Your Playlist


def add_song_command():
    while True:
        song_id = Prompt.ask("Enter song ID")

        if song_id_exists_in_singers(song_id):
            console.print(
                "Song ID already exists. Please enter a different one.",
                style=error_style,
            )
        else:
            break

    singer_name = Prompt.ask("Who is singing? ")
    add_song_to_playlist(song_id, singer_name)


def remove_song_command():
    singer_name = Prompt.ask("Take this name off the list")
    confirmation = Confirm.ask(f"Confirm to remove {singer_name}")
    if confirmation:
        remove_song_from_playlist(singer_name)
    else:
        console.print("Canceled", style=update_style)


# Handle user input for editing Song Library


def add_new_command():
    title = Prompt.ask("Enter title")
    artist = Prompt.ask("Enter artist")
    genre = Prompt.ask("Enter genre")
    lyrics = Prompt.ask("Enter lyrics")
    add_song_to_library(title, artist, genre, lyrics)


def remove_new_command():
    song_id = Prompt.ask("Enter song ID")
    confirmation = Confirm.ask(f"Confirm to remove {song_id}")

    if confirmation and song_id_exists_in_songs(song_id):
        remove_song_from_library(song_id)
    else:
        console.print(
            "Song ID doesn't exist. Please enter a different one.", style=error_style
        )


# Handle user inputs for song library search


def library_by_id_command():
    _id = Prompt.ask("Enter song id")
    view_library_by_id(_id)


def library_by_title_command():
    title_input = Prompt.ask("Enter song title")
    title = title_input.title()
    view_library_by_title(title)


def library_by_artist_command():
    artist_input = Prompt.ask("Enter artist name")
    artist = artist_input.title()
    view_library_by_artist(artist)


def library_by_genre_command():
    genre_input = Prompt.ask("Enter genre")
    genre = genre_input.title()
    view_library_by_genre(genre)


if __name__ == "__main__":
    app()
