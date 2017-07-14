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
        self.flag_imemaout = None
        self.flag_directaout = None

        self.flag_skip = None
        self.skipby = 0

        self.flag_active = 0

        self.ifln = []
        for item in open(fl).readlines():
            if item != "\n":
                self.ifln.append(item.replace("~","\n~").split("~")[0])
        #print(self.ifln) #debug-gives data interpreted

        self.main_loop()

    def flag_handler(self):

        if self.flag_const:
            i = 0
            while self.imem[i] != 0: i+=1
            self.imem[i] = self.char_data.replace(" ","")
            #print("const: stored constant %s at index %s." % (self.imem[i], i))
            self.flag_const = False

        elif self.flag_decl:

            check = len([x for x in self.i if x == '"'])
            name = self.i.split('"')[1]
            value = self.i[:-1].split('$')[1].rstrip()

            if check == 1:
                raise error.SyntaxError(error.missing_ONE_quot)
            elif check > 2:
                raise error.SyntaxError(error.too_many_quot)

            if " " in name:
                raise error.SyntaxError(error.mthan_ONE_word_in_quot)
            elif "$" in name:
                raise error.SyntaxError(error.spcChar_in_quot)

            if value.lower() not in ("true","false","1","0"):
                if chk(self.i) == "bool":
                    raise error.TypeError(error.Conv_Bool % value)
            else:
                exec("%s('%s')" % (chk(self.i),value))
            
            self.var_list.append( {name : (chk(self.i),value)} )
            self.flag_decl = False
            #print('decl: "%s" created with the type:"%s" and value "%s".' % 
            #    (name,chk(self.i),value))

        elif self.flag_out:
            if self.flag_directout:
                try: 
                    ifiltered = self.i[5:-1].replace("$","").rstrip()
                    print('%.f' % float(ifiltered), end = "")
                except ValueError:
                    raise error.TypeError(error.Conv_Float % ifiltered)

                self.flag_directout = False
                self.flag_out = False

            elif self.flag_imemout:
                try:
                    iz = self.char_data.replace("i","").rstrip()
                    print('%s' % self.imem[int(iz)], end = "")
                except IndexError:
                    raise error.IndexError(error.Mem_Index)
                self.flag_imemout
                self.flag_out = False

        elif self.flag_aout:
            if self.flag_directaout:

                try: 
                    ifiltered = self.i[6:-1].replace("$","")
                    print('%s' % chr(int(ifiltered.rstrip())), end = "")
                except ValueError:
                    raise error.TypeError(error.Conv_Int % ifiltered)

                self.flag_skip = True
                try: 
                    while self.i[self.skipby] != "\n": self.skipby+=1
                except: pass
                self.flag_directaout = False
                self.flag_aout = False

            elif self.flag_imemaout:

                try:
                    ind = int(self.i[6:].replace("i","").replace("\n",""))
                    value = int(self.imem[ind])
                    print('%s' % chr(value), end = "")
                except (TypeError,ValueError):
                    raise error.TypeError(error.Int_exp_got_float)

                self.flag_skip = True
                try:
                    while self.i[self.skipby] != "\n": self.skipby+=1
                except: pass
                self.flag_imemaout = False
                self.flag_aout = False

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

        if not self.flag_active and self.flag_start:
            if self.i[:3].upper() != 'END':
                if self.i.replace(" ","") != '\n':
                    isvar = self.i.replace("\n","")
                    raise error.SyntaxError(error.NO_kw_present % isvar)

        for self.pos_char,self.char_data in enumerate(self.i):

            if self.char_data == '\n':
                continue

            if self.flag_skip and self.skipby != 0:
                self.skipby-=1
                continue

            elif self.flag_skip and self.skipby == 0:
                self.flag_skip = False

            if not self.flag_aout:
                self.encountered()

            if self.char_data not in (" ","i"):
                self.flag_handler()

    def full_words(self): #keyword handler

        if self.i[:3].upper() == 'END':
            print("ending...")
            self.flag_exit = True
            self.flag_skip = True
            self.skipby = len(self.i)

        elif self.i[:6].upper() == "CONST ":
            self.flag_active+=1
            self.flag_const = True
            self.flag_skip = True
            self.skipby = 5

        elif self.i[:5].upper() == "DECL:":
            self.flag_active+=1
            self.flag_skip = True
            self.skipby = 5
            if '"' in self.i:
                self.flag_decl = True
            else:
                raise error.SyntaxError(error.missing_BOTH_quot)

        elif self.i[:4].upper() == "OUT ":
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

        elif self.i[:5].upper() == "AOUT ":
            self.flag_active+=1
            self.flag_aout = True
            self.flag_skip = True
            self.skipby = 4
            if "$" in self.i and "i" in self.i:
                raise error.SyntaxError(error.MTO_sc_present)
            elif "$" in self.i:
                self.flag_directaout = True
                self.skipby+=1
            elif "i" in self.i:
                self.flag_imemaout = True
                self.skipby+=1
                return 0
            else:
                raise error.SyntaxError(error.NO_sc_present)

    def main_loop(self):
        for self.x, self.i in enumerate(self.ifln):
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

def chk(i):
    if i[5:9] == "int ": return "int"
    elif i[5:10] == "bool ": return "bool"
    elif i[5:11] == "float ": return "float"
    elif i[5:12] == "string ": return "str"
    else: raise error.SyntaxError(error.Conv_Type)

dfile = "./runf.toye"

if __name__ == "__main__":
    try: 
        interpreter(sys.argv[1])
    except IndexError:
        print('Silently Using: default file "%s"\n' % dfile)
        interpreter(dfile)
