class flag_vars:
    def __init__(self):
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
        self.flag_skip_if = None

        self.indentlvl = 0

        self.flag_skipchars = None
        self.flag_skip = None
        self.skipby = 0

        self.flag_active = 0
