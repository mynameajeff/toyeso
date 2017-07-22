class SyntaxError(Exception):
    def __init__(self, message):
        super().__init__("Invalid Syntax. %s" % message) 
class ValueError(Exception):
    def __init__(self, message):
        super().__init__("Invalid Values. %s" % message)
class IndexError(Exception):
    def __init__(self, message):
        super().__init__("Invalid Index. %s" % message)
class TypeError(Exception):
    def __init__(self, message):
        super().__init__("Invalid Type. %s" % message)

#~ Variable Presence Errors ~
MTO_var_w_name = 'More than one Variable assigned the name "%s".'
NO_var_w_name = 'No Variable assigned the name "%s".'

#~ Character Presence Errors ~
MTO_lsquareb_present = "More than one [ is present."
MTO_rsquareb_present = "More than one ] is present."
MTO_st_present = "More than one START statement is present."
NO_end_present = "No END statement is present."
MTO_sc_present = "More than one special character present."
NO_sc_present = "No denomination character present."

#~ Quotation Errors ~
missing_square_brackets = "Missing both [] in order to form logical check."
missing_lsquare_bracket = "Missing [ in order to form logical check."
missing_rsquare_bracket = "Missing ] in order to form logical check."
bsquareb_MTO_present = "More than one ] and [ is present."
missing_BOTH_quot = 'Missing both " in order to declare the variable.'
missing_ONE_quot = 'Missing one " in order to declare the variable.'
too_many_quot = 'Too many " in line, cannot declare the variable.'
MTO_word_in_quot = 'More than one word found in quotation marks.'

#~ Keyword Errors ~
NO_kw_present = 'No keyword given for data: "%s".'

#~ Type Errors ~
Int_exp_got_float = 'Integer was expected, got Float instead.'
Conv_Float = 'Cannot convert character data: "%s" to Float.'
Conv_Int = 'Cannot convert character data: "%s" to Integer.'
Conv_Bool = 'Cannot convert character data: "%s" to Boolean.'
Conv_Type = 'Type for variable passed is invalid.'

#~ Index Errors ~
Mem_Index = 'Invalid Memory index present.'
