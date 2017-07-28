class SyntaxError(Exception):
    def __init__(self, message):
        super().__init__('Invalid Syntax. %s.' % message) 
class ValueError(Exception):
    def __init__(self, message):
        super().__init__('Invalid Values. %s.' % message)
class IndexError(Exception):
    def __init__(self, message):
        super().__init__('Invalid Index. %s.' % message)
class TypeError(Exception):
    def __init__(self, message):
        super().__init__('Invalid Type. %s.' % message)

#~ Variable Presence Errors ~
MTO_var_w_name = 'More than one Variable assigned the name "%s", line %s'
NO_var_w_name = 'No Variable assigned the name "%s", line %s'

#~ Character/Keyword Presence Errors ~
NO_if_present = 'No IF statement is present, line %s'
MTO_lsquareb_present = 'More than one [ is present, line %s'
MTO_rsquareb_present = 'More than one ] is present, line %s'
NO_start_present = 'No START statement is present, line %s'
MTO_st_present = 'More than one START statement is present, line %s'
NO_end_present = 'No END statement is present, line %s'
MTO_sc_present = 'More than one special character present, line %s'
NO_sc_present = 'No denomination character present, line %s'
NO_kw_present = 'No keyword given for data: "%s", line %s'

#~ Quotation Errors ~
missing_square_brackets = 'Missing both [] in order to form logical check, line %s'
missing_square_bracket = 'Missing "%s" in order to form logical check, line %s'
bsquareb_MTO_present = 'More than one ] and [ is present, line %s'
missing_BOTH_quot = "Missing both ' in order to declare the variable, line %s"
missing_ONE_quot = "Missing one ' in order to declare the variable, line %s"
too_many_quot = 'Too many " in line, cannot declare the variable, line %s'
MTO_word_in_quot = 'More than one word found in quotation marks, line %s'

#~ Type Errors ~
Int_exp_got_float = 'Integer was expected, got Float instead, line %s'
Conv_Float = 'Cannot convert character data: "%s" to Float, line %s'
Conv_Int = 'Cannot convert character data: "%s" to Integer, line %s'
Conv_Bool = 'Cannot convert character data: "%s" to Boolean, line %s'
Conv_Type = 'Type for variable passed is invalid, line %s'

#~ Index Errors ~
Mem_Index = 'Invalid Memory index present'

#~ Logical Errors ~
NO_Logic_present = 'No logical statement present between square brackets, line %s'
Inv_Op_present = 'Invalid Operator present within logical expression, line %s'
Inv_Args_present = 'Invalid Amount of Expression arguments present, line %s'
