#!/usr/bin/env python
from flag_vars import *
import flag, error, sys

__author__ = "mynameajeff"

class interpreter(flag.handler):
    def __init__(self, fl):
        flag_vars.__init__(self)

        with open(fl) as file:
            self.ifln = [line.replace("~","\n~").split("~")[0] for line in file]
        self.lineno = 0
        #debug - gives file data that is interpreted
        #print(self.ifln)

        self.main_loop()

    def chars(self): #numbers, etc
        if self.flag_skipchars == True:
            self.flag_skipchars = False
            return 0

        if not self.flag_active and self.flag_start:
            if self.i[self.indentlvl:3+self.indentlvl].upper() != 'END':
                if self.i.replace(" ","") != '\n':
                    raise error.SyntaxError(error.NO_kw_present 
                        % (self.i.replace("\n",""), self.lineno))

        for self.pos_char, self.char_data in enumerate(self.i):
            if self.char_data == '\n': continue

            if self.flag_skip and self.skipby != 0:
                self.skipby-=1
                continue

            elif self.flag_skip and self.skipby == 0:
                self.flag_skip = False

            self.flag_handler()

    def full_words(self): #keyword handler
        i_indented = self.i[self.indentlvl:].upper()
        i_indented_endif = self.i[self.indentlvl-4:1+self.indentlvl]
        self.tokens = [x for x in self.i[:-1].split(' ') if x != '']

        if i_indented_endif.upper() == "ENDIF":
            self.indentlvl -= 4
            if self.flag_skip_if:
                self.flag_skip_if = False
            return 0

        elif i_indented[:5] == "ENDIF" and not self.indentlvl:
            raise error.SyntaxError(error.NO_if_present 
                % self.lineno)

        else:
            if self.flag_skip_if: return 0

        if i_indented[:3] == "END":
            print("ending...")
            self.flag_exit = True
            self.flag_skip = True
            self.skipby = len(self.i)

        elif i_indented[:6] == "CONST ":
            self.flag_active+=1
            self.flag_const = True
            self.flag_skip = True
            self.skipby = 5

        elif i_indented[:5] == "DECL:":
            self.flag_active+=1
            self.flag_skip = True
            self.skipby = 5

            self.flag_decl = True

            if "$" == self.tokens[2][0]:
                self.flag_directdecl = True

            elif "i" == self.tokens[2][0]:
                self.flag_imemdecl = True

            else:
                raise error.SyntaxError(error.NO_sc_present
                    % self.lineno)

        elif i_indented[:4] == "OUT ":
            self.flag_active+=1
            self.flag_out = True
            self.flag_skip = True
            self.skipby = 3

            if "$" in self.i and "i" in self.i:
                raise error.SyntaxError(error.MTO_sc_present 
                    % self.lineno)

            elif "@" == self.tokens[1][0]: 
                self.flag_varout = True

            elif "$" == self.tokens[1][0]: 
                self.flag_directout = True

            elif "i" == self.tokens[1][0]: 
                self.flag_imemout = True

            else:
                raise error.SyntaxError(error.NO_sc_present
                    % self.lineno)

        elif i_indented[:5] == "AOUT ":
            self.flag_active+=1
            self.flag_aout = True
            self.flag_skip = True
            self.skipby = 4
            if "$" in self.i and "i" in self.i:
                raise error.SyntaxError(error.MTO_sc_present 
                    % self.lineno)

            if "@" == self.tokens[1][0]: 
                self.flag_varaout = True

            elif "$" == self.tokens[1][0]: 
                self.flag_directaout = True

            elif "i" == self.tokens[1][0]: 
                self.flag_imemaout = True

            else:
                raise error.SyntaxError(error.NO_sc_present
                    % self.lineno)

        elif i_indented[:2] == "IF":
            self.flag_active += 1
            self.indentlvl += 4
            self.flag_logicflow = True
            self.flag_logic_if = True
            self.flag_skip = True
            self.skipby = 2

    def main_loop(self):
        for self.i in self.ifln:
            self.lineno += 1

            if self.flag_exit:
                break

            if self.i[:5].upper() == 'START':
                if self.flag_start:
                    raise error.SyntaxError(error.MTO_st_present 
                        % self.lineno)
                print("starting...")
                self.flag_start = True
                self.flag_skip = True
                self.skipby = len(self.i)
                continue

            if self.flag_start:
                self.full_words()
                if not self.flag_skip_if: self.chars()

            if self.flag_active:
                self.flag_active = 0

        if not self.flag_exit:
            if not self.flag_start:
                raise error.SyntaxError(error.NO_start_present 
                    % self.lineno)
            raise error.SyntaxError(error.NO_end_present
                % self.lineno)

#dfile = "code-examples/hello-world-program.toye"
#dfile = "code-examples/runf.toye"
dfile = "code-examples/if.toye"

if __name__ == "__main__":
    try:
        interpreter(sys.argv[1])
    except:
        #print('Silently Using: default file "%s"\n' % dfile)
        interpreter(dfile)
