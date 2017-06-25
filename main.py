import sys, msvcrt, error

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

        try:
            if 'START' not in self.ifln[0][:5].upper() or 'END' not in self.ifln[len(self.ifln)-1][:5].upper():
                raise error.SyntaxError("No START or END statement passed in code")
        except IndexError:
            raise error.SyntaxError("No START and END statement passed in code")

        self.main_loop()

    def flag_handler(self):
        if self.flag_store:
            i = 0
            while self.imem[i] != 0: i+=1
            self.imem[i] = self.char_data.split("~")[0]
            print("imemory: stored %s at index %s." % (self.char_data.split("~")[0], i))
            self.flag_store = False
            return 0

        if self.flag_out:
            if self.flag_directout:
                try: 
                    print('direct: input was "%s"' % self.i[5:-1].split("~")[0])
                except ValueError:
                    raise error.ValueError("Cannot convert %s to integer, is invalid." % self.i[5:-1])

                self.flag_directout = False
                self.flag_out = False
                return 0

            i = self.imem[int(self.char_data.replace("~",""))]
            print('imemory: at index %s there is "%s".' % (self.char_data.replace("~",""), i))
            self.flag_out = False
            return 0

        if self.flag_aout:
            if self.flag_directaout:

                try: 
                    print('ascii output: %s' % chr(int(self.i[6:-1].split("~")[0].replace("~",""))))
                except ValueError:
                    raise error.ValueError("Cannot convert %s to integer, is invalid." % self.i[6:-1])

                self.flag_directaout = False
                self.flag_skip = True
                while self.i[self.skipby] != "\n": self.skipby+=1
                self.flag_aout = False
                return 0

            self.flag_skip = True
            self.skipby = 1
            self.flag_aout = False
            return 0

        print("Encountered Num:",self.char_data.split("~")[0])

    def encountered(self):
        try: 
            float(self.char_data)
            self.flag_skip = True
        except ValueError:
            if self.flag_out:
                raise error.ValueError("Cannot convert character data to imem index int.")

            if self.char_data != " ":
                print("Encountered Char:",self.char_data)
            return 0
        var1 = 1
        while self.i[self.pos_char+var1] not in ("\n"," "):
            self.char_data+=self.i[self.pos_char+var1]

            if "~" in self.char_data:
                break

            try: float(self.char_data)
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

            if not self.flag_aout:
                self.encountered()
            else: self.flag_handler()

    def full_words(self): #keyword handler
        if self.i[:5] in ('START','start'):
            if self.flag_start:
                raise error.SyntaxError("More than one START statement is present.")
            print("beginning!")
            self.flag_start = True
            self.flag_skip = True
            self.skipby = 5

        elif self.i[:3] in ('END','end'):
            print("ending...")
            msvcrt.getch()
            sys.exit()

        elif self.i[:5] in ("STORE","store"):
            self.flag_skip = True
            self.flag_store = True
            self.skipby = 6

        elif self.i[:3] in ("OUT","out"):
            self.flag_skip = True
            self.flag_out = True
            self.skipby = 4
            if self.i[4:5] == "$":
                self.flag_directout = True
                self.skipby+=1

        elif self.i[:4] in ("AOUT","aout"):
            self.flag_skip = True
            self.flag_aout = True
            self.skipby = 5
            if self.i[5:6] == "$":
                self.flag_directaout = True
                self.skipby+=1

    def main_loop(self):
        for self.x,self.i in enumerate(self.ifln):
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
