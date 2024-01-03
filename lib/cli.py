import typer
from rich.console import Console
from rich.prompt import Prompt, IntPrompt

from machine import (
    load_song,
    pause_song,
    add_song,
    remove_song,
    exit_program,
    get_all_songs,
    get_songs_by_title,
    get_songs_by_artist,
    get_songs_by_genre,
    view_queue,
    view_up_next,
)

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
        ("4", "Next up by song", "Your Playlist"),
        ("5", "Next up by singer", "Your Playlist"),
        ("a", "View all", "Song Library"),
        ("b", "View by title", "Song Library"),
        ("c", "View by artist", "Song Library"),
        ("d", "View by genre", "Song Library"),
        ("e", "Add new song", "Song Library"),
        ("f", "Delete song", "Song Library"),
        ("0", "Exit\n", "Exit"),
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

        choice = IntPrompt.ask("Enter selection (0-9)")
        if choice == 1:
            add_song_command()
        elif choice == 2:
            remove_song_command()
        elif choice == 3:
            load_next_song()
        elif choice == 4:
            view_queue_command()
        elif choice == 5:
            view_up_next_command()
        elif choice == 6:
            view_all_songs()
        elif choice == 7:
            title = Prompt.ask("Enter song title")
            view_songs_by_title(title)
        elif choice == 8:
            artist = Prompt.ask("Enter artist name")
            view_songs_by_artist(artist)
        elif choice == 9:
            genre = Prompt.ask("Enter genre")
            view_songs_by_genre(genre)
        elif choice == 0:
            exit_command()
            break
        else:
            console.print(
                "Invalid choice. Please enter a number between 0 and 9.",
                style="color(2)",
            )


@app.command()
def add_song_command():
    song_id = Prompt.ask("Enter song ID")
    singer_name = Prompt.ask("Who is singing?")
    add_song(song_id, singer_name)


@app.command()
def remove_song_command():
    singer_name = Prompt.ask("Take this name off the list")
    remove_song(singer_name)
    # console.print(f"{singer_name} removed from queue!", style=update_style)


@app.command()
def load_next_song():
    load_song()


@app.command()
def pause_current_song():
    pause_song()


@app.command()
def view_queue_command():
    view_queue()


@app.command()
def view_up_next_command():
    view_up_next()


@app.command()
def view_all_songs():
    get_all_songs()


@app.command()
def view_songs_by_title(title: str = typer.Argument(...)):
    get_songs_by_title(title)


@app.command()
def view_songs_by_artist(artist: str = typer.Argument(...)):
    get_songs_by_artist(artist)


@app.command()
def view_songs_by_genre(genre: str = typer.Argument(...)):
    get_songs_by_genre(genre)


@app.command()
def exit_command():
    exit_program()


if __name__ == "__main__":
    app()
