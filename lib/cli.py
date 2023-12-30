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


# title_card_displayed = False

# while True:
#     if not title_card_displayed:
#         display_title_card()
#         title_card_displayed = True

#     menu()


@app.command()
def menu():
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


@app.command()
def load_next_song():
    typer.echo("Loading next song.")


@app.command()
def pause_current_song():
    typer.echo("Pausing current song.")


@app.command()
def add_song_command(
    song_id: str = typer.Argument(...), singer_name: str = typer.Argument(...)
):
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
