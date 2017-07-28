import re, error

class handler:
    def flag_handler(self):

        if self.flag_const:
            i = 0
            while self.imem[i] != 0: i+=1
            if self.indentlvl == 0:
                self.imem[i] = self.i.split("const ")[-1].replace("\n","")
            else:
                self.imem[i] = self.char_data[self.indentlvl:].replace(" ","")
            #print("const: stored constant %s at index %s." % (self.imem[i], i))
            self.flag_const = False

        elif self.flag_decl:

            check = len([x for x in self.i if x == '"'])
            value = self.i[:-1].split('$')[1].rstrip()
            typeof = self.i.split()[0][5:].lower()
            name = self.i.split('"')[1]

            if check == 1:
                raise error.SyntaxError(error.missing_ONE_quot
                    % self.lineno)
            elif check > 2:
                raise error.SyntaxError(error.too_many_quot
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
                    raise error.TypeError(error.nv_Bool 
                        % (value, self.lineno))

            valid_var = 0
            for varl in self.var_list:
                try:
                    if varl[name]: valid_var+=1
                except KeyError: pass
            
            if valid_var > 1:
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
                    raise error.TypeError(error.nv_Float 
                        % (ifiltered, self.lineno))

                self.flag_directout = False

            elif self.flag_imemout:
                try:
                    ind = int(self.i[5:-1].replace(" ","").split("i")[-1])
                    print(self.imem[ind], end = "")
                except IndexError:
                    raise error.IndexError(error.em_Index
                        % self.lineno)
                self.flag_imemout = False

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
                    raise error.TypeError(error.Int_exp_got_float
                        % self.lineno)

                self.flag_imemaout = False

            elif self.flag_varaout:

                string = self.i.split('"')
                check = len([x for x in self.i if x == '"'])

                if check == 1:
                    raise error.SyntaxError(error.missing_ONE_quot
                        % self.lineno)
                elif check > 2:
                    raise error.SyntaxError(error.too_many_quot
                        % self.lineno)

                if "$" in string[0]:
                    raise error.SyntaxError(error.MTO_sc_present
                        % self.lineno)
                elif "i" in string[0]:
                    raise error.SyntaxError(error.MTO_sc_present
                        % self.lineno)

                valid_var = 0

                for varl in self.var_list:
                    try:
                        if varl[string[1]]: 
                            valid_var+=1
                            self.varl = varl
                    except KeyError: pass

                if not valid_var:
                    raise error.SyntaxError(error.NO_var_w_name 
                        % (string[1], self.lineno))

                type_of_variable = self.varl[string[1]][0]
                value_of_var = self.varl[string[1]][1]

                if type_of_variable == "int":
                    print('%s' % chr(int(value_of_var)), end = "")
                elif type_of_variable in ("float","bool"):
                    try:
                        print('%s' % chr(int(value_of_var)), end = "")
                    except:
                        raise error.TypeError(error.nv_Float 
                            % (value_of_var, self.lineno))
                elif type_of_variable == "str":
                    print(value_of_var, end = "")
                    #raise error.TypeError(error.nv_Int 
                    #    % (value_of_var, self.lineno))

                else: 
                    raise error.TypeError(error.nv_Type
                        % self.lineno)

                self.flag_varaout = False

            self.flag_aout = False
            self.flag_skip = True
            while self.i[self.skipby] != "\n":
                self.skipby+=1

        if self.flag_logicflow:
            if self.flag_logic_if:
                self.skip_if = None

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
                        raise error.SyntaxError(error.bsquareb_MTO_present
                            % self.lineno) 
                    else:
                        raise error.SyntaxError(error.MTO_lsquareb_present
                            % self.lineno)
                elif rbracketchk > 1:
                    raise error.SyntaxError(error.MTO_rsquareb_present
                        % self.lineno) 

                logic_space = self.i.split("[")[1].split("]")[0]
                #print("here it is: %s"%logic_space)
                if logic_space == '':
                    raise error.SyntaxError(error.NO_Logic_present
                        % self.lineno) 

                expression_list = logic_space.split(' ')
                #equal to, not equal to, less than, more than
                comparisons = ("==","!=") #,"\\\\","//"

                if len(expression_list) != 3:
                    raise error.SyntaxError(error.Inv_Args_present
                        % self.lineno) 

                if expression_list[1] not in comparisons:
                    raise error.SyntaxError(error.Inv_Op_present
                        % self.lineno) 

                spec_char_list = ["$", "i"]
                varsl = []

                for x in range(0,3,2):
                    special_exists = None

                    for sc in spec_char_list:
                        if sc == expression_list[x][0]:
                            special_exists = sc
                            #print(sc)
                    #print(x, "|%s|" % special_exists)

                    if special_exists == "$": #direct
                        #print("went to the $!")

                        type_of_var = None
                        value_of_var = expression_list[x][1:]

                        try:
                            value_of_var = int(value_of_var)
                        except:
                            try:
                                value_of_var = float(value_of_var)
                            except:
                                pass
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
                            raise error.TypeError(error.Conv_Int 
                                % (expression_list[x][1:], self.lineno))

                        try:
                            value_of_var = int(value_of_var)
                            type_of_var = "int"
                        except:
                            value_of_var = float(value_of_var)
                            type_of_var = "float"

                        #print(value_of_var)

                    else: #string-variable

                        valid_var = 0

                        for varl in self.var_list:
                            try:
                                if varl[expression_list[x]]:
                                    valid_var+=1
                                    self.varl = varl
                            except KeyError: pass

                        if not valid_var:
                            raise error.SyntaxError(error.NO_var_w_name 
                                % (expression_list[x], self.lineno))

                        type_of_var, value_of_var = self.varl[expression_list[x]]
                        #print("!",type_of_var, value_of_var)
                        
                        if type_of_var == "int":
                            value_of_var = int(value_of_var)

                        elif type_of_var == "float":
                            value_of_var = float(value_of_var)

                    varsl.append((type_of_var, value_of_var))


                check_list = []
                for item in varsl:
                    if item[0] == "str":
                        check_list.append(1)
                    elif item[0] in ("int", "float"):
                        check_list.append(2)
                    else:
                        #check_list.append(3)
                        raise error.TypeError(error.Conv_Type
                            % self.lineno) 

                if check_list == [1,1]:
                    if varsl[0][1] == varsl[1][1]:
                        IFexpr = True
                    else:
                        IFexpr = False

                elif check_list == [2,2]:
                    if float(varsl[0][1]) == float(varsl[1][1]):
                        IFexpr = True
                    else:
                        IFexpr = False

                elif check_list in ([1,2],[2,1]):
                    if varsl[0][0] == "str":
                        if len(varsl[0][1]) == varsl[1][1]:
                            IFexpr = True
                        else:
                            IFexpr = False
                    else:
                        if varsl[0][1] == len(varsl[1][1]):
                            IFexpr = True
                        else:
                            IFexpr = False

                if IFexpr:
                    if expression_list[1] == "==":
                        self.skip_if = False
                    else:
                        self.skip_if = True
                else:
                    if expression_list[1] == "==":
                        self.skip_if = True
                    else:
                        self.skip_if = False

                self.flag_logic_if = False

            self.flag_logicflow = False
