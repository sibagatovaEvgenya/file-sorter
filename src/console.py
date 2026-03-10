"""Модуль консольного менеджера"""
from rich import get_console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn


class ConsoleManager:
    """

    Консольный менеджер

    Attributes:
        _console: экземпляр консольного приложения
        _silent(bool): флаг отключения вывода в консоль

        Notes:
            Если передан аргумент silent - текст в консоль выводиться не будет
    """
    def __init__(self, silent: bool) -> None:
        """
        Инициализация консольного менеджера
        Args:
            silent: флаг отключения вывода в консоль
        """
        self._console = get_console()
        self._silent: bool = silent

    @property
    def progress(self) -> Progress:
        """
        Контекст прогресса выполнения

        Returns:
            (Progress): контекстный менеджер для отслеживания прогресса

        Examples:
            >>> console_manager: ConsoleManager = ConsoleManager()
            >>> with console_manager.progress as progress:
            ... task = progress.add_task("[cyan] Сортировка...", total=10, current_file="")
            ...
            ... for i, value in enumerate(range(10)):
                ... progress.update(task, advance=1, current_file=f"[yellow]{value}[/yellow]")


        """
        return Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            TextColumn("[dim]{task.fields[current_file]}"),
            console=self._console,
            transient=False,
            refresh_per_second=10,
        )

    def show_welcome(self, path: str | None = None) -> None:
        """

        Показать приветственное сообщение

        Args:
            path: (str | None): путь к каталогу сортировки

        Examples:
            >>> console_manager: ConsoleManager = ConsoleManager()
            >>> console_manager.show_welcome("C:/1/2/3")

        """
        self._print(
            Panel.fit(
                "[bold green] Сортировщик файлов [/bold green] \n\n Утилита для сортировки файлов по типам в папке"
                + ("\n\n Путь: [bold cyan]" + path + "[/bold cyan]" if path else ""),
                border_style="green",
            )
        )

    def print_log(self, message: str) -> None:
        """
        Вывести информационное сообщение

        Args:
            message(str): текст сообщения

        Examples:
            >>> console_manager: ConsoleManager = ConsoleManager()
            >>> console_manager.print.log("Информация")

        """
        self._print(f"[yellow]{message}[/yellow]")

    def print_error(self, message: str) -> None:
        """
               Вывести сообщение об ошибке

               Args:
                   message(str): текст сообщения

               Examples:
                   >>> console_manager: ConsoleManager = ConsoleManager()
                   >>> console_manager.print.error("Ошибка!")

               """
        self._print(f"[red]{message}[/red]")


    def _print(self, message: str | Panel) -> None:
        """
        Вывод сообщения в консоль

        Args:
            message(str): текст сообщения

        """
        if self._silent:
            return

        self._console.print(message)
