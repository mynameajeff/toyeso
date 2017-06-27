import sys, msvcrt, error

class interpreter:
    def __init__(self, fl):
        self.imem = [0]*512
        self.var_list = []

        self.flag_start = None
        self.flag_const = None

        self.flag_out = None
        self.flag_imemout = None
        self.flag_directout = None

        self.flag_aout = None #ascii
        self.flag_directaout = None

        self.flag_decl = None

        self.flag_skip = None
        self.skipby = 0

        self.flag_enc = True

        self.ifln = open(fl).readlines()
        #print(self.ifln) #debug statement, gives all data 4 file

        self.main_loop()

    def char_data_handler(self):

        if self.char_data in (" ","$","i"):
            return 0

        if self.flag_out:
            raise error.ValueError("Cannot convert character data to imem index int.")

        if self.char_data != " " and self.flag_enc:
            #print("Encountered Char:",self.char_data)
            raise error.SyntaxError('Encountered "%s", Invalid Syntax.'% self.char_data)

        if self.flag_decl:
            check = [x for x in self.i if x == '"']

            if len(check) == 1:
                raise error.SyntaxError('Missing one " in order to declare Var')
            elif len(check) > 2:
                raise error.SyntaxError('too many " in line')

            name = self.i.split('"')[1].split('"')[0]
            if " " in name:
                raise error.SyntaxError("More than one word found between the quotation marks.")
            value = self.i[:-1].split('$')[1].split('~')[0]
            self.var_list.append({name:value})
            self.flag_decl = False
            #print(self.var_list)
            print('decl: "%s" created with the value "%s".'% (name,value))

    def flag_handler(self):
        if self.flag_const:
            i = 0
            while self.imem[i] != 0: i+=1
            self.imem[i] = self.char_data.split("~")[0].replace(" ","")
            print("const: stored constant %s at index %s." % (self.imem[i], i))
            self.flag_const = False
            return 0

        if self.flag_out:
            if self.flag_directout:
                try: 
                    ifiltered = self.i[5:-1].split("~")[0].replace(" ","").replace("$","")
                    print('out: input was "%s"' % ifiltered)
                except ValueError:
                    raise error.ValueError("Cannot convert %s to integer, is invalid." % self.i[5:-1])

                self.flag_directout = False
                self.flag_out = False
                return 0

            if self.flag_imemout:
                try:
                    i = self.imem[int(self.char_data.replace("~","").replace("i",""))]
                except IndexError:
                    raise IndexError("Invalid Imemory index.")
                print('out: at index %s there is "%s".' % (self.char_data.replace("~",""), i))
                self.flag_out = False
            return 0

        if self.flag_aout:
            if self.flag_directaout:

                try: 
                    print('aout: %s' % chr(int(self.i[6:-1].split("~")[0].replace("~",""))))
                except ValueError:
                    raise error.ValueError('Cannot convert "%s" to integer, is invalid.' % self.i[6:-1])

                self.flag_directaout = False
                self.flag_skip = True
                while self.i[self.skipby] != "\n": self.skipby+=1
                self.flag_aout = False
                return 0

            self.flag_skip = True
            self.skipby = 1
            self.flag_aout = False
            return 0

        if self.flag_enc: 
            #print("Encountered Num:",self.char_data.split("~")[0])
            raise error.SyntaxError('Encountered "%s", Invalid Syntax.' % self.char_data)

    def encountered(self):
        try:
            float(self.char_data)
            self.flag_skip = True
        except ValueError:
            self.char_data_handler()
            return 0
        var1 = 1
        while self.i[self.pos_char+var1] not in ("\n"):
            self.char_data+=self.i[self.pos_char+var1]

            if "~" in self.char_data:
                break

            try: 
                if self.flag_enc: float(self.char_data)
            except ValueError:
                raise error.ValueError("Cannot convert character data to Float")
            var1+=1
        self.skipby += (var1-1)
        self.flag_handler()

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

            if self.flag_decl:
                pass

            if not self.flag_aout:
                self.encountered()
            else: self.flag_handler()

    def full_words(self): #keyword handler

        if self.i[:3].upper() == 'END':
            print("ending...")
            # msvcrt.getch()
            sys.exit()

        elif self.i[:5].upper() == "CONST":
            self.flag_const = True
            self.flag_skip = True
            self.skipby = 5

        elif self.i[:3].upper() == "OUT":
            self.flag_out = True
            self.flag_skip = True
            self.skipby = 3
            if "$" in self.i:
                self.flag_directout = True
                self.skipby+=1
                return 0
            if "i" in self.i:
                self.flag_imemout = True
                self.skipby+=1
                return 0
            else:
                raise error.SyntaxError("Invalid Syntax. No denomination character present.")

        elif self.i[:4].upper() == "AOUT":
            self.flag_aout = True
            self.flag_skip = True
            self.skipby = 4
            if "$" in self.i[4:]:
                self.flag_directaout = True
                self.skipby+=1

        elif self.i[:4].upper() == "DECL":
            self.flag_skip = True
            self.skipby = 5
            if '"' in self.i[4:]:
                self.flag_decl = True
                self.flag_enc = False
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

            if not self.flag_enc:
                self.flag_enc = True

dfile = "./runf.toye"

if __name__ == "__main__":
    if 'idlelib.run' not in sys.modules:
        try: interpreter(sys.argv[1])
        except: 
            print('Silently Using: default file "%s"\n' % dfile)
            interpreter(dfile)
    else: interpreter(dfile)
