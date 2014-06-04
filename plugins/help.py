from plugin import Plugin

class Help(Plugin):

    def onLoad(self):
        self.commands = self.bot.commands
        self.call = self.bot.call
        # commands
        self.addCommand('help', self.help_func, 'Show commandlist')
        self.addCommand('reload', self.reload_func, 'Reload plugins')

    def help_func(self, params, client_id, client_name):
        if len(params) == 0:
            helpstring = []
            helpstring.append('--list of commands--')
            helpstring.append('Syntax: \'command\' -> \'helpstring\'')
            for cmd in self.commands:
                cmddict = self.commands[cmd]
                helpstring.append('%s -> %s' % (cmd, cmddict['help']))
            helpstring.append('\n\nUse %shelp \'command\' to get help about a specific command!' % self.call)
            self.sendTextmessageClient(client_id, '\n'.join(helpstring))
        else:
            command = params[0]
            if command in self.commands:
                self.sendTextmessageClient(client_id, 'Help about %s:\n%s' % (command, self.commands[command]['help']))
            else:
                self.sendTextmessageClient(client_id, 'Invalid command! Try \'%shelp\' for a list of commands!' % self.call)

    def reload_func(self, params, client_id, client_name):
        self.bot.reloadPlugins()
        self.sendTextmessageClient(client_id, 'Reloaded plugins!')