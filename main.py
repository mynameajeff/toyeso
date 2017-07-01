import sys, msvcrt, error

class interpreter:
    def __init__(self, fl):
        self.imem = [0]*512
        self.var_list = []

        self.flag_start = None

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

        self.ifln = open(fl).readlines()
        #print(self.ifln) #debug statement, gives all data 4 file

        self.main_loop()

    def flag_handler(self):

        if self.char_data in (" ","i"): return 0

        if self.flag_const:
            i = 0
            while self.imem[i] != 0: i+=1
            self.imem[i] = self.char_data.split("~")[0].replace(" ","")
            print("const: stored constant %s at index %s." % (self.imem[i], i))
            self.flag_const = False
            return 0

        elif self.flag_out:
            if self.flag_directout:
                try: 
                    ifiltered = self.i[5:-1].split("~")[0].replace(" ","").replace("$","")
                    print('out: input was "%s"' % ifiltered)
                except ValueError:
                    raise error.ValueError("Cannot convert %s to integer, is invalid." % self.i[5:-1])

                self.flag_directout = False
                self.flag_out = False
                return 0

            elif self.flag_imemout:
                try:
                    i = self.imem[int(self.char_data.replace("~",""))]
                except IndexError:
                    raise IndexError("Invalid Imemory index.")
                ind = self.char_data.replace("~","").replace(" ","")
                print('out: at index %s there is "%s".' % (ind, i))
                self.flag_imemout
                self.flag_out = False
                return 0

        elif self.flag_aout:
            if self.flag_directaout:

                try: 
                    print('aout: %s' % chr(int(self.i[6:-1].split("~")[0].replace("~",""))))
                except ValueError:
                    raise error.ValueError('Cannot convert "%s" to integer, is invalid.' % self.i[6:-1])

                self.flag_skip = True
                while self.i[self.skipby] != "\n": self.skipby+=1
                self.flag_directaout = False
                self.flag_aout = False
                return 0

            elif self.flag_imemaout:

                try:
                    ind = int(self.i[6:-1].replace("i",""))
                    value = int(self.imem[ind])
                    print('aout: at index %s there is "%s".' % (ind, chr(value) ))
                except(TypeError,ValueError):
                    raise error.TypeError("integer argument expected, got float")

                self.flag_skip = True
                while self.i[self.skipby] != "\n": self.skipby+=1
                self.flag_imemaout = False
                self.flag_aout = False
                return 0

        elif self.flag_decl:
            err = "raise error.SyntaxError('Invalid Syntax. Type for variable passed is invalid.')"
            chk_num = lambda: "float" if self.i[5:11] == "float " else "int" if self.i[5:9] == "int " else exec(err)
            chk = lambda: "str" if self.i[5:12] == "string " else "bool" if self.i[5:10] == "bool " else chk_num()

            check = [x for x in self.i if x == '"']
            name = self.i.split('"')[1].split('"')[0]
            value = self.i[:-1].split('$')[1].split('~')[0]

            if len(check) == 1:
                raise error.SyntaxError('Missing one " in order to declare Var')
            elif len(check) > 2:
                raise error.SyntaxError('too many " in line')

            if " " in name:
                raise error.SyntaxError("More than one word found between the quotation marks.")

            if value.lower() not in ("true","false","1","0") and chk() == "bool":
                raise error.ValueError("Invalid Value %s cannot convert to boolean."%value)
            else:
                exec("%s('%s')"%(chk(),value))
            
            self.var_list.append( {name : (chk(),value)} )
            self.flag_decl = False
            print('decl: "%s" created with the type:"%s" and value "%s".'% (name,chk(),value))

    def encountered(self):
        try:
            float(self.char_data)
        except ValueError: return 0

        var1 = 1
        while self.i[self.pos_char+var1] != "\n":
            self.char_data += self.i[self.pos_char+var1]

            if "~" in self.char_data:
                break

            if "01234567890" in self.char_data:
                try: float(self.char_data)

                except ValueError:
                    raise error.ValueError("Cannot convert character data to Float")

            var1+=1

    def chars(self): #numbers, etc
        for self.pos_char,self.char_data in enumerate(self.i):

            if self.char_data == '\n':
                #print("newline!")
                continue

            if self.char_data == "~":
                self.flag_skip = True
                self.skipby += len(self.i.split("~")[1])-1
                continue

            if self.flag_skip and self.skipby != 0:
                self.skipby-=1
                continue

            elif self.flag_skip and self.skipby == 0:
                self.flag_skip = False

            if not self.flag_aout:
                self.encountered()
            self.flag_handler()

    def full_words(self): #keyword handler

        if self.i[:3].upper() == 'END':
            print("ending...")
            # msvcrt.getch()
            sys.exit()

        elif self.i[:6].upper() == "CONST ":
            self.flag_const = True
            self.flag_skip = True
            self.skipby = 5

        elif self.i[:4].upper() == "OUT ":
            self.flag_out = True
            self.flag_skip = True
            self.skipby = 3

            if "$" in self.i and "i" in self.i:
                raise error.SyntaxError("Invalid Syntax. More than one special character present")

            elif "$" in self.i:
                self.flag_directout = True
                self.skipby+=1
                return 0
            elif "i" in self.i:
                self.flag_imemout = True
                self.skipby+=1
                return 0
            else:
                raise error.SyntaxError("Invalid Syntax. No denomination character present.")

        elif self.i[:5].upper() == "AOUT ":
            self.flag_aout = True
            self.flag_skip = True
            self.skipby = 4
            if "$" in self.i and "i" in self.i:
                raise error.SyntaxError("Invalid Syntax. More than one special character present")
            elif "$" in self.i:
                self.flag_directaout = True
                self.skipby+=1
            elif "i" in self.i:
                self.flag_imemaout = True
                self.skipby+=1
                return 0
            else:
                raise error.SyntaxError("Invalid Syntax. No denomination character present.")

        elif self.i[:5].upper() == "DECL:":
            self.flag_skip = True
            self.skipby = 5
            if '"' in self.i:
                self.flag_decl = True
            else:
                raise error.SyntaxError('Missing both " in order to declare Var')

    def main_loop(self):
        for self.x, self.i in enumerate(self.ifln):

            if self.i[:5].upper() == 'START':
                if self.flag_start:
                    raise error.SyntaxError("More than one START statement is present.")
                print("starting...")
                self.flag_start = True
                self.flag_skip = True
                self.skipby = 5

            if self.flag_start:
                self.full_words()
                self.chars()

dfile = "./runf.toye"

if __name__ == "__main__":
    if 'idlelib.run' not in sys.modules:
        try: interpreter(sys.argv[1])
        except: 
            print('Silently Using: default file "%s"\n' % dfile)
            interpreter(dfile)
    else: interpreter(dfile)
