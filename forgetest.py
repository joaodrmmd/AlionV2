# alion_tui_final.py
import subprocess
import webbrowser
import os
import platform

from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, SelectionList, Log, Static
from textual.worker import Worker, WorkerState
from textual.widgets.selection_list import Selection

# --- Tela Genérica para Executar Comandos (VERSÃO CORRIGIDA E ROBUSTA) ---
class ToolRunnerScreen(Screen):
    """
    Executa um comando em segundo plano, com checagem de plataforma e sintaxe corrigida.
    """
    def __init__(self, tool_name: str, command_to_run, is_windows_only: bool = True, **kwargs) -> None:
        super().__init__(**kwargs)
        self.tool_name = tool_name
        self.command_to_run = command_to_run
        self.is_windows_only = is_windows_only
        self.log_widget = Log(highlight=True, markup=True)

    def compose(self) -> ComposeResult:
        yield Header(name=f"Executando: {self.tool_name}")
        yield self.log_widget
        yield Footer()

    def on_mount(self) -> None:
        """Inicia a execução do comando em segundo plano."""
        self.log_widget.write_line(f"🚀 Iniciando '{self.tool_name}'...")
        # Checa se o comando é exclusivo do Windows antes de iniciar o worker
        if self.is_windows_only and platform.system() != "Windows":
            self.log_widget.write_line(f"[bold yellow]AVISO:[/bold yellow] O comando '{self.tool_name}' só pode ser executado no Windows.")
            self.log_widget.write_line("\n[yellow]Pressione ESC para voltar ao menu.[/yellow]")
            return
        
        # Inicia o worker para executar o comando
        self.run_worker(self.execute_command, exclusive=True)

    def on_worker_state_changed(self, event: Worker.StateChanged) -> None:
        """Monitora o estado do worker e exibe o resultado final."""
        if event.state == WorkerState.SUCCESS:
            self.log_widget.write_line("\n[bold green]✅ Concluído com sucesso![/bold green]")
        elif event.state == WorkerState.ERROR:
            self.log_widget.write_line(f"\n[bold red]❌ Ocorreu um erro durante a execução:[/bold red]")
            self.log_widget.write_line(f"[red]{event.worker.error}[/red]")
        
        if event.state in (WorkerState.SUCCESS, WorkerState.ERROR):
             self.log_widget.write_line("\n[yellow]Pressione ESC para voltar ao menu.[/yellow]")

    def execute_command(self) -> None:
        """Esta é a função que o worker executa."""
        command = self.command_to_run
        if callable(command):
            command_output = command()
            self.call_from_thread(self.log_widget.write_line, command_output)
            return

        process = subprocess.Popen(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", command],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        
        for line in iter(process.stdout.readline, ''):
            self.call_from_thread(self.log_widget.write_line, line.strip())
        
        process.stdout.close()
        return_code = process.wait()
        
        if return_code:
            raise subprocess.CalledProcessError(return_code, command)

    def on_key(self, event) -> None:
        if event.key == "escape":
            self.app.pop_screen()


# --- Funções Especiais ---
def open_github():
    webbrowser.open("https://github.com/joaodrmmd/AlionV2")
    return "Abrindo o link do GitHub no seu navegador..."

# --- Dicionário de Ferramentas (SINTAXE DE ADMIN CORRIGIDA) ---
# Usamos aspas simples no ArgumentList para evitar erros de aninhamento de aspas no PowerShell
TOOLS = {
    "1": {"name": "Create Restore Point", "desc": "Cria um ponto de restauração do sistema.", "command": "Start-Process powershell -Verb RunAs -ArgumentList '-Command \"Checkpoint-Computer -Description ''AlionV2 Restore Point'' -RestorePointType ''MODIFY_SETTINGS''\"'"},
    "2": {"name": "Spotify Activation", "desc": "Executa o script de ativação do Spotify.", "command": "irm https://spotx-official.github.io/run.ps1 | iex"},
    "3": {"name": "KMS Activation", "desc": "Ativação de produtos Microsoft via KMS.", "command": "irm https://get.activated.win | iex"},
    "4": {"name": "Optimization", "desc": "Executa o script de otimização de Chris Titus.", "command": "Start-Process powershell -Verb RunAs -ArgumentList '-Command \"irm https://christitus.com/win | iex\"'"},
    "5": {"name": "Download QuickCPU", "desc": "Baixa o QuickCPU para a pasta de Downloads.", "command": "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1')); choco install -y wget; wget -O \"$env:USERPROFILE\\Downloads\\QuickCpuSetup.zip\" 'https://www.coderbag.com/assets/downloads/cpm/currentversion/QuickCpuSetup64.zip' ; Start-Process explorer.exe $env:USERPROFILE\\Downloads"},
    "6": {"name": "Disk Cleanup", "desc": "Abre a Limpeza de Disco do Windows.", "command": "cleanmgr /sagerun:1"},
    "7": {"name": "Download Ahoy!", "desc": "Baixa o Ahoy! para a pasta de Downloads.", "command": "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1')); choco install -y wget; wget -O \"$env:USERPROFILE\\Downloads\\Ahoy.zip\" 'https://www.mediafire.com/folder/idotcbblq5o2l/Ahoy!' ; Start-Process explorer.exe $env:USERPROFILE\\Downloads"},
    "8": {"name": "NVIDIA Drivers", "desc": "Baixa o GeForce Experience.", "command": "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1')); choco install -y wget; wget -O \"$env:USERPROFILE\\Downloads\\Nvidia_Driver.exe\" 'https://us.download.nvidia.com/GFE/GFEClient/3.28.0.417/GeForce_Experience_v3.28.0.417.exe' ; Start-Process explorer.exe $env:USERPROFILE\\Downloads"},
    "9": {"name": "AMD Drivers", "desc": "Baixa o instalador dos drivers AMD.", "command": "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1')); choco install -y wget; wget -O \"$env:USERPROFILE\\Downloads\\AMD_Driver.exe\" 'https://drivers.amd.com/drivers/installer/24.10/whql/amd-software-adrenalin-edition-24.8.1-minimalsetup-240829_web.exe' ; Start-Process explorer.exe $env:USERPROFILE\\Downloads"},
    "10": {"name": "Discord Nitro - Vencord", "desc": "Baixa o instalador do Vencord.", "command": "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1')); choco install -y wget; wget -O \"$env:USERPROFILE\\Downloads\\VencordInstaller.exe\" 'https://github.com/Vencord/Installer/releases/latest/download/VencordInstaller.exe' ; Start-Process explorer.exe $env:USERPROFILE\\Downloads"},
    "11": {"name": "Github", "desc": "Abre o repositório do projeto no navegador.", "command": open_github, "windows_only": False},
}

# --- Tela do Menu Principal ---
class MainMenuScreen(Screen):
    def compose(self) -> ComposeResult:
        ascii_art = r"""
 ░▒▓██████▓▒░░▒▓█▓▒░     ░▒▓█▓▒░░▒▓██████▓▒░░▒▓███████▓▒░         ░▒▓████████▓▒░▒▓██████▓▒░░▒▓███████▓▒░ ░▒▓██████▓▒░░▒▓████████▓▒░
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░     ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░         ░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░     ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░         ░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░
░▒▓████████▓▒░▒▓█▓▒░     ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░         ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░░▒▓█▓▒▒▓███▓▒░▒▓██████▓▒░
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░     ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░         ░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░     ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░         ░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░
░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓█▓▒░░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░         ░▒▓█▓▒░      ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░░▒▓████████▓▒░
        """
        yield Static(ascii_art, id="banner")
        
        options = [
            Selection(f"[{key}] {tool['name']}", id=key, description=tool['desc'])
            for key, tool in TOOLS.items()
        ]
        yield SelectionList(*options, id="menu")
        yield Static("Developed by r3du0x® 2025", id="dev-footer")

    # MÉTODO NOVO E CORRETO
def on_selection_list_selection_selected(self, event: SelectionList.SelectionSelected):
    # O ID da seleção agora é acessado através de event.selection.id
    tool_id = event.selection.id
    selected_tool = TOOLS[tool_id]
    
    # Cria a tela de execução com as informações da ferramenta selecionada
    runner_screen = ToolRunnerScreen(
        tool_name=selected_tool["name"],
        command_to_run=selected_tool["command"],
        is_windows_only=selected_tool.get("windows_only", True)
    )
    self.app.push_screen(runner_screen)


# --- Aplicação Principal ---
class AlionV2App(App):
    TITLE = "AlionV2 Multi-tool - by r3du0x"
    CSS = """
    #banner { text-style: bold; color: #C850C0; width: 100%; text-align: center; margin: 1 0; }
    #menu { border: round #4158D0; margin: 1 4; width: auto; }
    #dev-footer { width: 100%; text-align: center; color: #FFCC70; margin-top: 1; }
    """
    BINDINGS = [("q", "quit", "Sair")]

    def on_mount(self) -> None:
        self.push_screen(MainMenuScreen())

if __name__ == "__main__":
    if platform.system() == 'Windows':
        os.system('') # Garante que as cores ANSI funcionem no terminal do Windows
    app = AlionV2App()
    app.run()