import sublime, sublime_plugin, os, re

class WikiLinkCommand(sublime_plugin.TextCommand):
    def run(self, edit):        
        #find our current directory
        directory = os.path.split(self.view.file_name())[0]
        #find our current window
        window = self.view.window()
        #find the cursor
        location = self.view.sel()[0]
        
        #find the word under the cursor
        word = self.view.substr(self.view.word(location.a)).replace("*", "")
        scope = self.view.substr(self.view.extract_scope(location.a)).replace("*", "")

        if "link.external.Wiki" in self.view.scope_name(location.a):
                sublime.status_message("try to open " + scope)
                sublime.active_window().run_command('open_url', {"url": scope})
        elif "link.email.Wiki" in self.view.scope_name(location.a):
                sublime.status_message("try to mail " + scope)
                sublime.active_window().run_command('open_url', {"url": "mailto:"+scope})
        elif "link.document.Wiki" in self.view.scope_name(location.a):
            target = "[>"+scope[2:];
            target = self.view.find(target,0,sublime.LITERAL)
            target = sublime.Region(target.a, target.a)
            self.view.sel().clear()
            self.view.sel().add(target)
            self.view.show_at_center(target)
        elif "link.internal.Wiki" in self.view.scope_name(location.a):
            #okay, we're good. Keep on keepin' on.        
            
            #compile the full file name and path.
            new_file = os.path.join(directory,word+".wiki")

            #debug section: uncomment to write to the console
            # print("Location: %d" % location.a)
            # print("Selected word is '%s'" % word)
            # print("Full file path: %s" % new_file)
            # print("Selected word scope is '%s'" % self.view.scope_name(location.a))
            # if internalLink in self.view.scope_name(location.a):
            #     print("this is an internal link")
            #end debug section

            if os.path.exists(new_file):
                #open the already-created page.
                new_view = window.open_file(new_file)
            else:
                #Create a new file and slap in the default text.
                new_view = window.new_file()
                default_text = "{0}\nWrite about {0} here.".format(word)

                new_view.insert(edit,0,default_text)
                new_view.run_command('append', {'characters': default_text})
                new_view.set_name("%s.wiki" % word)
                new_view.set_syntax_file(self.view.settings().get('syntax'))
        else:
            sublime.status_message("Can only open WikiWords, WikiLinks, email addresses or web addresses.")
