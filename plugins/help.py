from plugin import Plugin

class Help(Plugin):

    def onLoad(self):
        self.commands = self.bot.registeredCommands
        self.call = self.bot.call
        # commands
        self.registerCommand('help', self.help_func, 'Show commandlist')
        self.registerCommand('reload', self.reload_func, 'Reload plugins')

    def help_func(self, params, clid, clname):

        if len(params) == 0:
            helpstring = []
            helpstring.append('-- list of commands --')
            helpstring.append('Syntax: \'command\' -> \'helpstring\'')
            for cmd in self.commands:
                cmd_dict = self.commands[cmd]
                helpstring.append('%s -> %s' % (cmd, self.commands[cmd][1]))
            helpstring.append('\n\nUse %shelp \'command\' to get help about a specific command!' % self.call)
            self.sendtextmessageClient(clid, '\n'.join(helpstring))
        else:
            command = params[0]
            if command in self.commands:
                self.sendtextmessageClient(clid, 'Help about %s:\n%s' % (command, self.commands[command][1]))
            else:
                self.sendtextmessageClient(client_id, 'Invalid command! Try \'%shelp\' for a list of commands!' % self.call)

    def reload_func(self, params, clid, clname):
        self.bot.reloadPlugins()
        self.sendtextmessageClient(clid, 'Reloaded plugins!')