import typer
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

app = typer.Typer()


def display_title_card():
    typer.echo("*" * 58)
    typer.echo(
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
            {typer.style("a Python CLI project by @eburdekin", fg=typer.colors.CYAN, bold=True)}
                      """
    )


@app.callback(invoke_without_command=True)
def main():
    display_title_card()
    menu()


@app.command()
def menu():
    while True:
        typer.echo("Choose an option:")
        typer.echo("1. Load next song")
        typer.echo("2. Pause current song")
        typer.echo("3. Add song to queue")
        typer.echo("4. Remove song from queue")
        typer.echo("5. View queue by song")
        typer.echo("6. View queue by singer")
        typer.echo("7. View all songs")
        typer.echo("8. View songs by artist")
        typer.echo("9. View songs by genre")
        typer.echo("0. Exit")

        choice = typer.prompt("Enter the number of your choice (0-9):", type=int)
        if choice == 1:
            load_next_song()
        elif choice == 2:
            pause_current_song()
        elif choice == 3:
            add_song_command()
        elif choice == 4:
            remove_song_command()
        elif choice == 5:
            view_queue_command()
        elif choice == 6:
            view_up_next_command()
        elif choice == 7:
            view_all_songs()
        elif choice == 8:
            artist = typer.prompt("Enter artist name:")
            view_songs_by_artist(artist)
        elif choice == 9:
            genre = typer.prompt("Enter genre:")
            view_songs_by_genre(genre)
        elif choice == 0:
            exit_command()
            break
        else:
            typer.echo("Invalid choice. Please enter a number between 0 and 9.")


@app.command()
def load_next_song():
    typer.echo("Loading next song.")


@app.command()
def pause_current_song():
    typer.echo("Pausing current song.")


@app.command()
def add_song_command():
    song_id = typer.prompt("Enter song ID: ")
    singer_name = typer.prompt("Who is singing?: ")
    add_song(song_id, singer_name)


@app.command()
def remove_song_command(singer_name: str = typer.Argument(...)):
    remove_song(singer_name)


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
