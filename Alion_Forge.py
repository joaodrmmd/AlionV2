import os
import subprocess
import webbrowser
import sys

# --- Funções para Comandos Específicos ---

def set_title(title):
    """Define o título da janela do console."""
    if os.name == 'nt': # Windows
        os.system(f"title {title}")

def clear_screen():
    """Limpa a tela do console de forma multiplataforma."""
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    """Exibe o banner principal com a nova arte ASCII colorida."""
    # Códigos de escape ANSI para a cor
    magenta = "\033[1;95m"
    reset = "\033[0m"
    
    # Usamos um "raw string" (r"""...""") para que os caracteres especiais
    # da arte ASCII não sejam interpretados pelo Python.
    ascii_art = r"""
 ░▒▓██████▓▒░░▒▓█▓▒░     ░▒▓█▓▒░░▒▓██████▓▒░░▒▓███████▓▒░         ░▒▓████████▓▒░▒▓██████▓▒░░▒▓███████▓▒░ ░▒▓██████▓▒░░▒▓████████▓▒░
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░     ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░         ░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░     ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░         ░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░
░▒▓████████▓▒░▒▓█▓▒░     ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░         ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░░▒▓█▓▒▒▓███▓▒░▒▓██████▓▒░
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░     ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░         ░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░     ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░         ░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░
░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓█▓▒░░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░         ░▒▓█▓▒░      ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░░▒▓████████▓▒░
"""
    print(f"{magenta}{ascii_art}{reset}")
    
def menu():
    """Exibe o menu de opções."""
    # Códigos de escape ANSI para as cores
    magenta = "\033[1;95m"
    cyan = "\033[1;96m"
    reset = "\033[0m"
    
    print("")
    print("")
    print(f"               {magenta}║{reset}                                       {magenta}║{reset}                                       {magenta}║{reset}")
    print(f"               {magenta}╠══{cyan}[1] Create Restore Point{reset}       {magenta}╠══{cyan}[5] Download QuickCPU{reset}          {magenta}╠══{cyan}[9] AMD Drivers{reset}")
    print(f"               {magenta}║{reset}                                       {magenta}║{reset}                                       {magenta}║{reset}")
    print(f"               {magenta}╠══{cyan}[2] Spotify Activation{reset}         {magenta}╠══{cyan}[6] Disk Cleanup{reset}               {magenta}╠══{cyan}[10] Discord Nitro - Windows{reset}")
    print(f"               {magenta}║{reset}                                       {magenta}║{reset}                                       {magenta}║{reset}")
    print(f"               {magenta}╠══{cyan}[3] KMS Activation{reset}             {magenta}╠══{cyan}[7] Ahoy!{reset}                      {magenta}╚══{cyan}[11] Github{reset}")
    print(f"               {magenta}║{reset}                                       {magenta}║{reset}")
    print(f"               {magenta}╚══{cyan}[4] Otimization{reset}                {magenta}╚══{cyan}[8] NVIDIA Drivers{reset}")
    print("\n" * 6)
    print(f"                                   {magenta}║{cyan} Developed by r3du0x® 2025 {magenta}║{cyan} Updated 3th of August (Alpha Ver.) {magenta}║{reset}")
    print("")

def run_powershell_command(command, as_admin=False, hidden=False):
    """Executa um comando PowerShell."""
    try:
        if as_admin:
            # -Verb RunAs solicita elevação de privilégios
            ps_command = f"Start-Process powershell -ArgumentList '-NoProfile -ExecutionPolicy Bypass -Command \"{command}\"' -Verb RunAs"
            subprocess.run(["powershell", "-Command", ps_command], check=True)
        else:
            # Constrói o comando para rodar normal ou oculto
            ps_args = ["powershell"]
            if hidden:
                ps_args.extend(["-WindowStyle", "Hidden"])
            ps_args.extend(["-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", command])
            subprocess.run(ps_args, check=True)
            
        print("\n✅ Comando executado com sucesso!")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Erro ao executar o comando: {e}")
    except FileNotFoundError:
        print("\n❌ Erro: 'powershell' não foi encontrado. Certifique-se de que está instalado e no PATH do sistema.")
    input("Pressione Enter para continuar...")

# --- Dicionário de Comandos ---
# Mapeia as escolhas do usuário para os comandos a serem executados
COMMANDS = {
    "1": lambda: run_powershell_command("Checkpoint-Computer -Description 'AlionV2 Restore Point' -RestorePointType 'MODIFY_SETTINGS'"),
    "2": lambda: run_powershell_command("$scriptURL='https://spotx-official.github.io/run.ps1'; $tempFile=[System.IO.Path]::Combine($pwd.Path, 'temp_script_' + (Get-Date -Format 'HH-mm-ss') + '_' + (Get-Random) + '.ps1'); (New-Object System.Net.WebClient).DownloadFile($scriptURL, $tempFile); & $tempFile; Remove-Item $tempFile -Force; Pause"),
    "3": lambda: run_powershell_command("irm https://get.activated.win | iex", hidden=True),
    "4": lambda: run_powershell_command("irm https://christitus.com/win | iex", hidden=True),
    "5": lambda: run_powershell_command("iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1')); choco install -y wget; wget -O \\\"$env:USERPROFILE\\Downloads\\QuickCPU.zip\\\" 'https://www.coderbag.com/assets/downloads/cpm/currentversion/QuickCpuSetup64.zip' ; Start-Process explorer.exe $env:USERPROFILE\\Downloads", as_admin=True),
    "6": lambda: run_powershell_command("Start-Process cleanmgr -ArgumentList '/sagerun:1' -Wait; Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.MessageBox]::Show('Disk cleanup is complete!', 'Notification')", hidden=True),
    "7": lambda: run_powershell_command("iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1')); choco install -y wget; wget -O \\\"$env:USERPROFILE\\Downloads\\Ahoy!.zip\\\" 'https://www.mediafire.com/folder/idotcbblq5o2l/Ahoy!' ; Start-Process explorer.exe $env:USERPROFILE\\Downloads", as_admin=True),
    "8": lambda: run_powershell_command("iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1')); choco install -y wget; wget -O \\\"$env:USERPROFILE\\Downloads\\Nvidia Driver.zip\\\" 'https://us.download.nvidia.com/GFE/GFEClient/3.28.0.417/GeForce_Experience_v3.28.0.417.exe' ; Start-Process explorer.exe $env:USERPROFILE\\Downloads", as_admin=True),
    "9": lambda: run_powershell_command("iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1')); choco install -y wget; wget -O \\\"$env:USERPROFILE\\Downloads\\AMD Driver.zip\\\" 'https://drivers.amd.com/drivers/installer/24.10/whql/amd-software-adrenalin-edition-24.8.1-minimalsetup-240829_web.exe' ; Start-Process explorer.exe $env:USERPROFILE\\Downloads", as_admin=True),
    "10": lambda: run_powershell_command("iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1')); choco install -y wget; wget -O \\\"$env:USERPROFILE\\Downloads\\DiscordNitro.zip\\\" 'https://github.com/Vencord/Installer/releases/latest/download/VencordInstaller.exe' ; Start-Process explorer.exe $env:USERPROFILE\\Downloads", as_admin=True),
    "11": lambda: webbrowser.open("https://github.com/joaodrmmd/AlionV2")
}

# --- Loop Principal ---

def main():
    """Função principal que executa o loop do menu."""
    # Garante que as cores ANSI funcionem no terminal do Windows
    if os.name == 'nt':
        os.system('') 
        
    set_title("AlionV2 Multi-tool - by r3du0x")
    
    while True:
        clear_screen()
        banner()
        menu()
        
        try:
            choice = input("Select a Number-> ")
            
            # Pega a função correspondente no dicionário
            action = COMMANDS.get(choice)
            
            if action:
                action() # Executa a função
            elif choice: # Se o usuário digitou algo, mas não é uma opção válida
                print(f"\nOpção '{choice}' inválida. Tente novamente.")
                input("Pressione Enter para continuar...")

        except (KeyboardInterrupt, EOFError): # Permite sair com Ctrl+C ou Ctrl+Z
            print("\n\nSaindo do programa. Até mais!")
            sys.exit(0)

if __name__ == "__main__":
    main()