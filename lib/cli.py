# UI - menu formatting, user input handling and validation

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

PINK = "color(5)"
CYAN = "color(6)"


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
    console.print("          a Python CLI project by @eburdekin", style=CYAN)


# Automatically run main() upon app load
@app.callback(invoke_without_command=True)
def main():
    display_title_card()
    menu()


def format_menu():
    options = [
        ("1", "Load next song", "Your Playlist"),
        ("2", "Add song", "Your Playlist"),
        ("3", "Remove song", "Your Playlist"),
        ("4", "View all", "Your Playlist"),
        ("5", "View all", "Song Library"),
        ("6", "View by title", "Song Library"),
        ("7", "View by artist", "Song Library"),
        ("8", "View by genre", "Song Library"),
        ("9", "View by id", "Song Library"),
        ("10", "Add new song", "Song Library"),
        ("11", "Delete song", "Song Library"),
    ]

    menu_text = ""
    current_header = ""
    for option, description, header in options:
        if header != current_header:
            menu_text += f"\n[{PINK}]{header}[/{PINK}]\n"
            current_header = header
        menu_text += f"[{CYAN}]{option}[/{CYAN}]. {description}\n"

    return menu_text


@app.command()
def menu():
    while True:
        console.print(format_menu())
        console.print(f"[bold {CYAN}]0[/bold {CYAN}]. [{PINK}]Exit[/{PINK}]\n")

        choice = IntPrompt.ask("What'll it be?")
        if choice == 1:
            load_song()
        elif choice == 2:
            add_song_to_playlist_command()
        elif choice == 3:
            remove_song_from_playlist_command()
        elif choice == 4:
            view_all_playlist()
        elif choice == 5:
            view_all_library()
        elif choice == 6:
            library_by_title_command()
        elif choice == 7:
            library_by_artist_command()
        elif choice == 8:
            library_by_genre_command()
        elif choice == 9:
            library_by_id_command()
        elif choice == 10:
            add_song_to_library_command()
        elif choice == 11:
            remove_song_from_library_command()
        elif choice == 0:
            exit_program()
            break
        else:
            console.print(
                "Invalid choice. Try again!",
                style="color(2)",
            )


# Handle user input for editing Your Playlist


def validate_non_empty(value):
    return value.strip() != "", "Input cannot be blank."


def validate_url(url):
    return (
        url.startswith("https://www.youtube.com/watch?v="),
        "URL must be a YouTube video.",
    )


def prompt_with_validation(prompt_text, validation_function):
    while True:
        user_input = Prompt.ask(prompt_text)
        is_valid, error_message = validation_function(user_input)
        if is_valid:
            return user_input
        else:
            console.print(error_message, style=error_style)


def add_song_to_playlist_command():
    song_id = prompt_with_validation("Enter song ID to add", validate_non_empty)

    if song_id_exists_in_singers(song_id):
        console.print(
            "Song ID already exists. Please enter a different one.",
            style=error_style,
        )
    else:
        singer_name = prompt_with_validation("Who is singing?", validate_non_empty)
        add_song_to_playlist(song_id, singer_name)


def remove_song_from_playlist_command():
    singer_name = Prompt.ask("Take this name off the list")
    confirmation = Confirm.ask(f"Confirm to remove {singer_name}")

    if confirmation:
        remove_song_from_playlist(singer_name)
    else:
        console.print("Canceled", style=update_style)


# Handle user input for editing Song Library


def add_song_to_library_command():
    title = prompt_with_validation("Enter title", validate_non_empty)
    artist = prompt_with_validation("Enter artist", validate_non_empty)
    genre = prompt_with_validation("Enter genre", validate_non_empty)
    lyrics = prompt_with_validation("Enter lyrics", validate_non_empty)
    url = prompt_with_validation("Enter URL", validate_url)

    add_song_to_library(title, artist, genre, lyrics, url)


def remove_song_from_library_command():
    song_id = Prompt.ask("Enter song ID to delete")
    confirmation = Confirm.ask(f"Confirm to delete song #{song_id} from Song Library")

    if confirmation:
        if song_id_exists_in_songs(song_id):
            remove_song_from_library(song_id)
        else:
            console.print(
                f"Song #{song_id} doesn't exist. Please enter a valid ID.",
                style=error_style,
            )
    else:
        console.print(f"Canceled, song #{song_id} not removed.", style=update_style)


# Handle user inputs for song library search


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


def library_by_id_command():
    _id = Prompt.ask("Enter song id")
    view_library_by_id(_id)


if __name__ == "__main__":
    app()
