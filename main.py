import sys, error

class interpreter:
    def __init__(self, fl):
        self.imem = [0]*512
        self.var_list = []

        self.flag_start = None
        self.flag_exit = None

        self.flag_const = None
        self.flag_decl = None

        self.flag_out = None
        self.flag_imemout = None
        self.flag_directout = None

        self.flag_aout = None #ascii
        self.flag_varaout = None
        self.flag_imemaout = None
        self.flag_directaout = None

        self.flag_logicflow = None
        self.flag_logic_if = None

        self.indentlvl = 0

        self.flag_skipchars = None
        self.flag_skip = None
        self.skipby = 0

        self.flag_active = 0

        self.ifln = []
        for item in open(fl).readlines():
            if item != "\n":
                self.ifln.append(item.replace("~","\n~").split("~")[0])
        #print(self.ifln) #debug - gives file data that is interpreted

        self.main_loop()

    def flag_handler(self):

        if self.flag_const:
            i = 0
            while self.imem[i] != 0: i+=1
            self.imem[i] = self.char_data[self.indentlvl:].replace(" ","")
            #print("const: stored constant %s at index %s." % (self.imem[i], i))
            self.flag_const = False
            return 0

        elif self.flag_decl:

            check = len([x for x in self.i if x == '"'])
            value = self.i[:-1].split('$')[1].rstrip()
            typeof = self.i.split()[0][5:].lower()
            name = self.i.split('"')[1]

            if check == 1:
                raise error.SyntaxError(error.missing_ONE_quot)
            elif check > 2:
                raise error.SyntaxError(error.too_many_quot)
            if " " in name:
                raise error.SyntaxError(error.MTO_word_in_quot)

            if value.lower() in ("true","false","1","0"):
                try: exec("%s('%s')" % (typeof, value))
                except: raise error.SyntaxError(error.Conv_Type)
            else:
                if typeof == "bool":
                    raise error.TypeError(error.Conv_Bool % value)

            valid_var = 0
            for varl in self.var_list:
                try:
                    if varl[name]: valid_var+=1
                except KeyError: pass
            
            if valid_var > 1:
                raise error.SyntaxError(error.MTO_var_w_name % name)

            self.flag_decl = False
            self.var_list.append( {name : (typeof, value)} )
            # print('decl: "%s" created with the type:"%s" and value "%s".' % 
            #    (name, typeof, value))

        elif self.flag_out:
            if self.flag_directout:
                try: 
                    ifiltered = self.i[5:-1].replace("$","").rstrip()
                    print('%.f' % float(ifiltered), end = "")
                except ValueError:
                    raise error.TypeError(error.Conv_Float % ifiltered)

                self.flag_directout = False

            elif self.flag_imemout:
                try:
                    ind = int(self.i[5:-1].replace(" ","").split("i")[-1])
                    print(self.imem[ind], end = "")
                except IndexError:
                    raise error.IndexError(error.Mem_Index)
                self.flag_imemout = False

            self.flag_out = False

        elif self.flag_aout:
            if self.flag_directaout:

                try: 
                    ifiltered = self.i[6:-1].split("$")[-1]
                    print('%s' % chr(int(ifiltered.rstrip())), end = "")
                except ValueError:
                    raise error.TypeError(error.Conv_Int % ifiltered)

                self.flag_directaout = False

            elif self.flag_imemaout:

                try:
                    ind = int(self.i[6:-1].split("i")[-1])
                    value = int(self.imem[ind])
                    print('%s' % chr(value), end = "")
                except (TypeError,ValueError):
                    raise error.TypeError(error.Int_exp_got_float)

                self.flag_imemaout = False

            elif self.flag_varaout:

                string = self.i.split('"')
                check = len([x for x in self.i if x == '"'])

                if check == 1:
                    raise error.SyntaxError(error.missing_ONE_quot)
                elif check > 2:
                    raise error.SyntaxError(error.too_many_quot)

                if "$" in string[0]:
                    raise error.SyntaxError(error.MTO_sc_present)
                elif "i" in string[0]:
                    raise error.SyntaxError(error.MTO_sc_present)

                valid_var = 0

                for varl in self.var_list:
                    try:
                        if varl[string[1]]: 
                            valid_var+=1
                            self.varl = varl
                    except KeyError: pass

                if not valid_var:
                    raise error.SyntaxError(error.NO_var_w_name % string[1])

                type_of_variable = self.varl[string[1]][0]
                value_of_var = self.varl[string[1]][1]

                if type_of_variable == "int":
                    print('%s' % chr(int(value_of_var)), end = "")
                elif type_of_variable in ("float","bool"):
                    try:
                        print('%s' % chr(int(value_of_var)), end = "")
                    except:
                        raise error.TypeError(error.Conv_Float % value_of_var)
                elif type_of_variable == "str":
                    print(value_of_var, end = "")
                    #raise error.TypeError(error.Conv_Int % value_of_var)

                else: raise error.TypeError(error.Conv_Type)

                self.flag_varaout = False

            self.flag_aout = False
            self.flag_skip = True
            while self.i[self.skipby] != "\n":
                self.skipby+=1

        if self.flag_logicflow:
            if self.flag_logic_if:

                if "[" not in self.i and "]" not in self.i:
                    raise error.SyntaxError(error.missing_square_brackets)
                elif "[" not in self.i:
                    raise error.SyntaxError(error.missing_lsquare_bracket)
                elif "]" not in self.i:
                    raise error.SyntaxError(error.missing_rsquare_bracket)

                lbracketchk = len([x for x in self.i if x == '['])
                rbracketchk = len([x for x in self.i if x == ']'])

                if lbracketchk > 1:
                    if rbracketchk > 1:
                        raise error.SyntaxError(error.bsquareb_MTO_present) 
                    else:
                        raise error.SyntaxError(error.MTO_lsquareb_present)
                elif rbracketchk > 1:
                    raise error.SyntaxError(error.MTO_rsquareb_present)

                self.flag_logic_if = False



            self.flag_logicflow = False

    def encountered(self):

        var1 = 1
        while self.i[self.pos_char+var1] != "\n":
            self.char_data += self.i[self.pos_char+var1]

            if "01234567890" in self.char_data or not self.flag_active:
                try:
                    if self.i[self.pos_char+var1] != " ":
                        float(self.char_data)
                    else: pass

                except ValueError:
                    raise error.ValueError(error.Conv_Float % self.char_data)

            var1+=1

    def chars(self): #numbers, etc
        if self.flag_skipchars == True:
            self.flag_skipchars = False
            return 0

        if not self.flag_active and self.flag_start:
            if self.i[self.indentlvl:3+self.indentlvl].upper() != 'END':
                if self.i.replace(" ","") != '\n':
                    isvar = self.i.replace("\n","")
                    raise error.SyntaxError(error.NO_kw_present % isvar)

        for self.pos_char, self.char_data in enumerate(self.i):
            if self.char_data == '\n': continue

            if self.flag_skip and self.skipby != 0:
                self.skipby-=1
                continue

            elif self.flag_skip and self.skipby == 0:
                self.flag_skip = False

            self.encountered()
            self.flag_handler()

    def full_words(self): #keyword handler

        if self.i[self.indentlvl:3+self.indentlvl].upper() == "END":
            print("ending...")
            self.flag_exit = True
            self.flag_skip = True
            self.skipby = len(self.i)

        elif self.i[self.indentlvl:6+self.indentlvl].upper() == "CONST ":
            self.flag_active+=1
            self.flag_const = True
            self.flag_skip = True
            self.skipby = 5

        elif self.i[self.indentlvl:5+self.indentlvl].upper() == "DECL:":
            self.flag_active+=1
            self.flag_skip = True
            self.skipby = 5
            if '"' in self.i:
                self.flag_decl = True
            else:
                raise error.SyntaxError(error.missing_BOTH_quot)

        elif self.i[self.indentlvl:4+self.indentlvl].upper() == "OUT ":
            self.flag_active+=1
            self.flag_out = True
            self.flag_skip = True
            self.skipby = 3

            if "$" in self.i and "i" in self.i:
                raise error.SyntaxError(error.MTO_sc_present)

            elif "$" in self.i:
                self.flag_directout = True
                self.skipby+=1
                return 0
            elif "i" in self.i:
                self.flag_imemout = True
                self.skipby+=1
                return 0
            else:
                raise error.SyntaxError(error.NO_sc_present)

        elif self.i[self.indentlvl:5+self.indentlvl].upper() == "AOUT ":
            self.flag_active+=1
            self.flag_aout = True
            self.flag_skip = True
            self.skipby = 4
            if "$" in self.i and "i" in self.i:
                raise error.SyntaxError(error.MTO_sc_present)

            elif "@" in self.i: self.flag_varaout = True

            elif "$" in self.i: self.flag_directaout = True

            elif "i" in self.i: self.flag_imemaout = True

            else:
                raise error.SyntaxError(error.NO_sc_present)

        elif self.i[self.indentlvl:2+self.indentlvl].upper() == "IF":
            self.flag_active += 1
            self.indentlvl += 4
            self.flag_logicflow = True
            self.flag_logic_if = True
            self.flag_skip = True
            self.skipby = 2

        if self.i[self.indentlvl-4:1+self.indentlvl].upper() == "ENDIF":
            self.indentlvl -= 4

    def main_loop(self):
        for self.x, self.i in enumerate(self.ifln):
            if self.i == "\n": continue

            if self.flag_exit:
                sys.exit()

            if self.i[:5].upper() == 'START':
                if self.flag_start:
                    raise error.SyntaxError(error.MTO_st_present)
                print("starting...")
                self.flag_start = True
                self.flag_skip = True
                self.skipby = len(self.i)
                continue

            if self.flag_start:
                self.full_words()
                self.chars()

            if self.flag_active:
                self.flag_active = 0

        if not self.flag_exit:
            raise error.SyntaxError(error.NO_end_present)

#dfile = "code-examples/hello-world-program.toye"
dfile = "code-examples/runf.toye"


if __name__ == "__main__":
    try: 
        interpreter(sys.argv[1])
    except IndexError:
        print('Silently Using: default file "%s"\n' % dfile)
        interpreter(dfile)
