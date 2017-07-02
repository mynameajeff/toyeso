class SyntaxError(Exception):
    def __init__(self, message):
        super().__init__("Invalid Syntax. " + message) 
class ValueError(Exception):
    def __init__(self, message):
        super().__init__("Invalid Values. " + message)
class IndexError(Exception):
    def __init__(self, message):
        super().__init__("Invalid Index. " + message)
class TypeError(Exception):
    def __init__(self, message):
        super().__init__("Invalid Type. " + message)

#~ Character Presence Errors ~
MTO_st_present = "More than one START statement is present."
MTO_sc_present = "More than one special character present."
NO_sc_present = "No denomination character present."

#~ Quotation Errors ~
missing_BOTH_quot = 'Missing both " in order to declare the variable.'
missing_ONE_quot = 'Missing one " in order to declare the variable.'
too_many_quot = 'Too many " in line, cannot declare the variable.'
spcChar_in_quot = 'Unexpected Special character in quotation marks.'
mthan_ONE_word_in_quot = 'More than one word found in quotation marks.'

#~ Keyword Errors ~
NO_kw_present = 'No keyword given for data: "%s" supplied.'

#~ Type Errors ~
Int_exp_got_float = 'Integer was expected, got Float instead.'
Conv_Float = 'Cannot convert character data: "%s" to Float.'
Conv_Int = 'Cannot convert character data: "%s" to Integer.'
Conv_Bool = 'Cannot convert character data: "%s" to Boolean.'

#~ Index Errors ~
Mem_Index = 'Invalid Memory index present'
