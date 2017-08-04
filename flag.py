import re, error, decimal

class handler:
    def flag_handler(self):

        if self.flag_const:
            i = 0
            while self.imem[i] != 0: i+=1
            if self.indentlvl == 0:
                value = self.i.split("const ")[-1].replace("\n","")
            else:
                value = self.char_data[self.indentlvl:].replace(" ","")
            #print("const: stored constant %s at index %s." % (self.imem[i], i))

            try: float(value)

            except:
                raise error.ValueError(error.Conv_Float
                    % (value, self.lineno))

            self.imem[i] = value 
            self.flag_const = False

        elif self.flag_decl:

            check = len([x for x in self.i if x == '"'])
            value = self.i[:-1].split('$')[1].rstrip().lstrip()
            typeof = self.i.split()[0][5:].lower()
            name = self.i.split('"')[1]

            if check:
                if check > 2:
                    raise error.SyntaxError(error.too_many_quot
                        % self.lineno)
                elif check == 1:
                    raise error.SyntaxError(error.missing_ONE_quot
                        % self.lineno)
            else:
                raise error.SyntaxError(error.missing_BOTH_quot
                    % self.lineno)

            if " " in name:
                raise error.SyntaxError(error.MTO_word_in_quot
                    % self.lineno)

            if value.lower() in ("true","false","1","0"):
                try: exec("%s('%s')" % (typeof, value))
                except: raise error.SyntaxError(error.Conv_Type
                    % self.lineno)
            else:
                if typeof == "bool":
                    raise error.TypeError(error.Conv_Bool 
                        % (value, self.lineno))

            if typeof == "float":
                try:
                    value = float(value)
                except ValueError:
                    raise error.TypeError(error.Conv_Float
                        % (value, self.lineno))

            if typeof == "int":
                try:
                    if not float(value).is_integer():
                        raise error.TypeError(error.Conv_Int
                            % (value, self.lineno))
                    value = decimal.Decimal(value)

                except decimal.InvalidOperation:
                    raise error.TypeError(error.Conv_Int
                        % (value, self.lineno))

            valid_var = 0
            for varl in self.var_list:
                try:
                    if varl[name]: valid_var+=1
                except KeyError: pass
            
            if valid_var >= 1:
                raise error.SyntaxError(error.MTO_var_w_name 
                    % (name, self.lineno))

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
                    raise error.TypeError(error.Conv_Float 
                        % (ifiltered, self.lineno))

                self.flag_directout = False

            elif self.flag_imemout:
                try:
                    ind = int(self.i[5:-1].replace(" ","").split("i")[-1])
                    print(self.imem[ind], end = "")
                except IndexError:
                    raise error.IndexError(error.Mem_Index
                        % self.lineno)
                self.flag_imemout = False

            elif self.flag_varout:

                i_rel = self.i.replace("\n","")
                string = self.i.lower().split('out ')[1]
                strlist = [
                    string[0],
                    ''.join(i_rel.split('@')[1][1:].split('"'))
                ]

                self.validation_1(string, strlist[1])

                type_of_variable = self.varl[strlist[1]][0]
                value_of_var = self.varl[strlist[1]][1]

                if type_of_variable == "int":
                    print('%d' % int(value_of_var), end = "")

                elif type_of_variable == "float":
                    print(value_of_var, end = "")

                elif type_of_variable == "bool":
                    if value_of_var.lower() in ("false","0"):
                        tempvar = 0
                    else:
                        tempvar = 1
                    print(tempvar, end = "")

                elif type_of_variable == "str":
                    for x in value_of_var:
                        print(ord(x), end = " ")

                else:
                    raise error.TypeError(error.Conv_Type
                        % self.lineno)

                self.flag_varout = False

            self.flag_out = False

        elif self.flag_aout:
            if self.flag_directaout:

                try: 
                    ifiltered = self.i[6:-1].split("$")[-1]
                    print('%s' % chr(int(ifiltered.rstrip())), end = "")
                except:
                    raise error.TypeError(error.Conv_Int 
                        % (ifiltered, self.lineno))

                self.flag_directaout = False

            elif self.flag_imemaout:

                try:
                    ind = int(self.i[4:].split("i")[-1])
                    value = chr(int(self.imem[ind]))
                    print('%s' % value, end = "")
                except ValueError:
                    try:
                        raise error.TypeError(error.Conv_Int
                            % (self.imem[ind], self.lineno))
                    except UnboundLocalError:
                        raise error.IndexError(error.Mem_Index
                            % self.lineno)

                self.flag_imemaout = False

            elif self.flag_varaout:

                i_rel = self.i.replace("\n","")
                string = self.i.lower().split('aout ')[1]
                strlist = [
                    string[0],
                    ''.join(i_rel.split('@')[1][1:].split('"'))
                ]

                self.validation_1(string, strlist[1])

                type_of_variable = self.varl[strlist[1]][0]
                value_of_var = self.varl[strlist[1]][1]

                if type_of_variable == "int":
                    print('%s' % chr(int(value_of_var)), end = "")

                elif type_of_variable == "float":
                    try:
                        print('%s' % chr(int(value_of_var)), end = "")
                    except:
                        raise error.TypeError(error.Conv_Int 
                            % (value_of_var, self.lineno))

                elif type_of_variable == "bool":
                    if value_of_var.lower() in ("false","0"):
                        tempvar = "false"
                    else:
                        tempvar = "true"
                    print(tempvar, end = "")

                elif type_of_variable == "str":
                    print(value_of_var, end = "")

                else: 
                    raise error.TypeError(error.Conv_Type
                        % self.lineno)

                self.flag_varaout = False

            self.flag_aout = False

        if self.flag_logicflow:
            if self.flag_logic_if:
                self.flag_skip_if = None

                if "[" not in self.i and "]" not in self.i:
                    raise error.SyntaxError(error.missing_square_brackets
                        % self.lineno)

                for x in range(2):
                    if ("[","]")[x] not in self.i:
                        raise error.SyntaxError(error.missing_square_bracket 
                            % (("[","]")[x], self.lineno))

                lbracketchk = len([x for x in self.i if x == '['])
                rbracketchk = len([x for x in self.i if x == ']'])

                if lbracketchk > 1:
                    if rbracketchk > 1:
                        raise error.SyntaxError(error.MTO_squareb_present
                            % self.lineno) 
                    else:
                        raise error.SyntaxError(error.MTO_lsquareb_present
                            % self.lineno)
                elif rbracketchk > 1:
                    raise error.SyntaxError(error.MTO_rsquareb_present
                        % self.lineno) 

                expression_list = self.i.split("[")[1].split("]")[0].split(' ')

                if expression_list == '':
                    raise error.SyntaxError(error.NO_Logic_present
                        % self.lineno) 

                if len(expression_list) != 3:
                    raise error.SyntaxError(error.Inv_Args_present
                        % self.lineno) 

                #equal to, not equal to, less than, more than
                if expression_list[1] not in ("==","!="): #,"\\\\","//"
                    raise error.SyntaxError(error.Inv_Op_present
                        % self.lineno) 

                check_list = []
                varsl = []

                def rfunc():
                    raise error.TypeError(error.Conv_Type
                        % self.lineno)

                l1 = lambda: 2 if type_of_var in ("int", "float") else rfunc()
                return_typevar = lambda: 1 if type_of_var == "str" else l1()

                for x in range(0, 3, 2):
                    special_exists = None

                    for sc in ("$", "i"):
                        if sc == expression_list[x][0]:
                            special_exists = sc

                    if special_exists == "$": #direct
                        value_of_var = expression_list[x][1:]
                        type_of_var = None

                        try: value_of_var = int(value_of_var)

                        except:
                            try: value_of_var = float(value_of_var)
                            except: pass

                        finally:
                            if type(value_of_var) == int:
                                type_of_var = "int"
                            elif type(value_of_var) == float:
                                type_of_var = "float"
                            else:
                                if value_of_var.lower() in ("1","0","true","false"):
                                    type_of_var = "bool"
                                else:
                                    type_of_var = "str"

                    elif special_exists == "i": #imem
                        try:
                            value_of_var = self.imem[int(expression_list[x][1:])]
                        except ValueError:
                            try:
                                t, v = self.get_var_vt(expression_list[x])
                                type_of_var, value_of_var = t, v
                            except:
                                raise error.TypeError(error.Conv_Int 
                                    % (expression_list[x][1:], self.lineno))
                        try:
                            value_of_var = int(value_of_var)
                            type_of_var = "int"
                        except:
                            try:
                                value_of_var = float(value_of_var)
                                type_of_var = "float"
                            except:
                                pass #if string

                    else: #string-variable
                        
                        type_of_var, value_of_var = self.get_var_vt(expression_list[x])

                        if type_of_var == "float":
                            value_of_var = float(value_of_var)

                    varsl.append([type_of_var, value_of_var])
                    check_list.append(return_typevar())

                if check_list == [1,1]:
                    check_tuple_1 = (varsl[0][1], varsl[1][1])

                elif check_list == [2,2]:
                    check_tuple_1 = (float(varsl[0][1]), float(varsl[1][1]))

                elif check_list in ([1,2], [2,1]):
                    if varsl[0][0] == 1:
                        check_tuple_1 = (len(varsl[0][1]), varsl[1][1])
                    else:
                        check_tuple_1 = (varsl[0][1], len(varsl[1][1]))

                check_tuple_2 = (
                    check_tuple_1[0] != check_tuple_1[1],
                    check_tuple_1[0] == check_tuple_1[1]
                )

                if expression_list[1] == "==":
                    self.flag_skip_if = check_tuple_2[0]
                else:
                    self.flag_skip_if = check_tuple_2[1]

                self.flag_logic_if = False

            self.flag_logicflow = False

    def get_var_vt(self, expr_item):
        valid_var = 0

        for varl in self.var_list:
            try:
                if varl[expr_item]:
                    valid_var+=1
                    self.varl = varl
            except KeyError:
                pass
        if not valid_var:
            raise error.SyntaxError(error.NO_var_w_name 
                % (expr_item, self.lineno))

        return self.varl[expr_item] #type_of_var, value_of_var

    def validation_1(self, string, strlist_part):
        check = len([x for x in string if x == '"'])

        if check:
            if check > 2:
                raise error.SyntaxError(error.too_many_quot
                    % self.lineno)
            elif check == 1:
                raise error.SyntaxError(error.missing_ONE_quot
                    % self.lineno)
        else:
            raise error.SyntaxError(error.missing_BOTH_quot
                % self.lineno)

        valid_var = 0

        for varl in self.var_list:
            try:
                if varl[strlist_part]: 
                    valid_var+=1
                    self.varl = varl
            except KeyError: pass
        if not valid_var:
            raise error.SyntaxError(error.NO_var_w_name 
                % (strlist_part, self.lineno))
