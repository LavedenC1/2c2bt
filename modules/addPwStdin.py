
def addPwStdin(command: str, sudo_password: str) -> str:
    new_cmd = command.replace("sudo", f" echo {sudo_password} | sudo -S")
    if new_cmd.startswith(" "):
        new_cmd = new_cmd[1:]
    return new_cmd
if __name__ == "__main__":
    command = "sudo apt update"
    print(addPwStdin(command))
    