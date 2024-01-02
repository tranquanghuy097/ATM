import services.commands as commands


class TransactionController:
    def __init__(self, command: commands.BaseCommand) -> None:
        self.__command = command

    def execute(self):
        return self.__command.execute()
