def send_command(self, command_package: list) -> list:
    '''
    Sends a command package
    '''
    self._write(command_package)
    raw_response = self._read()
    return raw_response
