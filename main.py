import sys, msvcrt

class toy:
    class SyntaxError(Exception):
        pass
    class ValueError(Exception):
        pass

class interpreter:
    def __init__(self, fl):
        self.imem = [0]*4096

        self.flag_start = None
        self.flag_store = None

        self.flag_out = None
        self.flag_directout = None

        self.flag_aout = None #ascii
        self.flag_directaout = None

        self.flag_skip = None

        self.skipby = 0
        self.ifln = open(fl).readlines()
        #print(self.ifln) #debug statement, gives all data 4 file
        self.enum = enumerate(self.ifln)

        try:
            if self.ifln[0] not in ('START\n','start\n') or self.ifln[len(self.ifln)-1] not in ('END','end'):
                raise toy.SyntaxError("No START or END statement passed in code")
        except IndexError:
            raise toy.SyntaxError("No START and END statement passed in code")

        self.main_loop()

    def flag_handler(self):
        if self.flag_store:
            i = 0
            while self.imem[i] != 0: i+=1
            self.imem[i] = self.char_data
            print("imemory: stored %s at index %s." % (self.char_data, i))
            self.flag_store = False
            return 0

        if self.flag_out:
            if self.flag_directout:
                print('direct: input was "%s".' % self.i[5:-1])
                self.flag_directout = False
                self.flag_out = False
                return 0

            i = self.imem[int(self.char_data)]
            print('imemory: at index %s there is "%s".' % (self.char_data, i))
            self.flag_out = False
            return 0

        if self.flag_aout:
            if self.flag_directaout:

                try: print('ascii output: %s' % chr(int(self.i[6:-1])))
                except ValueError:
                    raise toy.ValueError("Cannot convert %s to integer, is invalid." % self.i[6:-1])
                self.flag_directaout = False
                self.flag_skip = True
                self.skipby = 1
                self.flag_aout = False
                return 0

            self.flag_skip = True
            self.skipby = 1
            self.flag_aout = False
            return 0

        print("Encountered Num:",self.char_data)

    def encountered(self):
        try: 
            float(self.char_data)
            self.flag_skip = True
        except ValueError:
            if self.flag_out:
                raise toy.ValueError("Cannot convert character data to imem index int.")
                return 0

            print("Encountered Char:",self.char_data)
            return 0
        var1 = 1
        while self.ifln[self.x][self.pos_char+var1] != "\n":
            self.char_data+=self.ifln[self.x][self.pos_char+var1]
            try: float(self.char_data)
            except ValueError:
                raise toy.ValueError("Cannot convert character data to Float")
            var1+=1
        self.skipby += (var1-1)

        self.flag_handler()

    def chars(self): #numbers, etc
        for self.pos_char,self.char_data in enumerate(self.ifln[self.x]):

            if self.char_data == '\n':
                #print("newline!")
                continue

            if self.flag_skip and self.skipby != 0:
                self.skipby-=1
                continue

            elif self.flag_skip and self.skipby == 0:
                self.flag_skip = False

            if not self.flag_aout: self.encountered()
            else: self.flag_handler()

    def full_words(self): #keyword handler
        if self.i in ('START\n','start\n'):
            if self.flag_start:
                raise toy.SyntaxError("More than one START statement is present.")
            print("beginning!")
            self.flag_start = True
            self.flag_skip = True
            self.skipby = 5

        elif self.i in ('END','end'):
            print("ending...")
            msvcrt.getch()
            sys.exit()

        elif "STORE" == self.i[:5] or "store" == self.i[:5]:
            self.flag_skip = True
            self.flag_store = True
            self.skipby = 6

        elif "OUT" == self.i[:3] or "out" == self.i[:3]:
            self.flag_skip = True
            self.flag_out = True
            self.skipby = 4
            if self.i[4:5] == "$":
                self.flag_directout = True
                self.skipby+=1

        elif "AOUT" == self.i[:4] or "aout" == self.i[:4]:
            self.flag_skip = True
            self.flag_aout = True
            self.skipby = 5
            if self.i[5:6] == "$":
                self.flag_directaout = True
                self.skipby+=1

    def main_loop(self):
        for self.x,self.i in self.enum:
            self.full_words()
            if self.flag_start: 
                self.chars()

dfile = "./runf.toy"

if __name__ == "__main__":
    if 'idlelib.run' not in sys.modules:
        try: interpreter(sys.argv[1])
        except: 
            print('Silently Using: default file "%s"\n' % dfile)
            interpreter(dfile)
    else: interpreter(dfile)
