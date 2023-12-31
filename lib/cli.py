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
    console.print("          a Python CLI project by @eburdekin", style="bold color(6)")


@app.callback(invoke_without_command=True)
def main():
    display_title_card()
    menu()


def format_menu():
    options = [
        ("1", "Add song to queue"),
        ("2", "Load next song"),
        ("3", "Pause current song"),
        ("4", "View queue by song"),
        ("5", "View queue by singer"),
        ("6", "View all songs"),
        ("7", "View songs by title"),
        ("8", "View songs by artist"),
        ("9", "View songs by genre"),
        ("0", "Exit\n"),
    ]

    menu_text = "\n".join(
        [f"{option}. {description}" for option, description in options]
    )
    return menu_text


@app.command()
def menu():
    while True:
        console.print("\nChoose an option:", style="color(5)")
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
    console.print(f"Song #{song_id} added to queue!", style=update_style)


@app.command()
def remove_song_command():
    singer_name = Prompt.ask("Take this name off the list")
    remove_song(singer_name)
    console.print(f"{singer_name} removed from queue!", style=update_style)


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
