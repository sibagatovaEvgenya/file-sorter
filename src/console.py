from rich import get_console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

class ConsoleManager:
    def __init__(self, silent: bool) -> None:
        self._console = get_console()
        self._silent: bool = silent

    @property
    def progress(self) -> Progress:
        return Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            TextColumn("[dim]{task.fields[current_file]}"),
            console=self._console,
            transient=False,
            refresh_per_second=10
        )

    def show_welcome(self, path: str | None = None) -> None:
        self._print(
            Panel.fit(
                "[bold green] Сортировщик файлов [/bold green] \n\n Утилита для сортировки файлов по типам в папке"
                + ("\n\n Путь: [bold cyan]" + path + "[/bold cyan]" if path else ""),
                border_style="green"
            )
        )

    def print_log(self, message: str) -> None:
        self._print(f"[yellow]{message}[/yellow]")

    def print_error(self, message: str) -> None:
        self._print(f"[red]{message}[/red]")

    def print_success(self, message: str) -> None:
        self._print(f"[green]{message}[/green]")

    def _print(self, message: str | Panel) -> None:
        if self._silent:
            return

        self._console.print(message)

