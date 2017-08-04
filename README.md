# The Toyeso Lang
A toy esoteric language project created by mynameajeff.

The Toyeso Spec:

Short Description:

    - A toy esoteric language project created by mynameajeff.

The aim of this language:

    ~ "To look similar to ASM/lower level langs, 
        but have functionality more similar to python, 
        including my own personal tweaks. " - mynameajeff

The Rules of the lang:

    - Every program must begin with a START statement.

    - Every program must end with an END statement.

    - Capitals are optional for keywords & variable names,
        but are not for types and the special char (i)

    - Before the START statement, (which must 
        occupy the first five character spaces of a line),
        commmenting is allowed because, the interpreter 
        will not have begun scanning for syntax. This also
        means no code will be recognised here.

    - After the END statement, (same thing as START but three)
        you may comment once again, because the interpreter will
        have terminated and is therefore not scanning for syntax anymore.

    - In the event you want to comment within the codespace(start-end)
        you could use the special character "~",
        either on it's own line,
        or at the end of another.
        
    - Type is implemented with variables(not in the Imem)
        what is currently implemented: string, bool, int, float,
        they are stored, and can be accessed via the AOUT command.
        
    - The special characters are these:

        @: this one means 'from var', so @"variable" literally means 'from var named variable'
        
        i: this one means 'from constant variable store at index',
                so i0 literally means 'from constant variable store at index 0'

        $: this one means 'the direct value', so $33 literally means 'the direct value 33'
        
        all of them work with the command to create the final product of that command.

There are a few keywords, I'll list them now.

    const:
        stores constant number in the Imemory
        where the next index is available.

        Example: const 55

    decl:
        @: <not implemented>

        i: <not implemented>

        $:
            creates a variable(of type given after :)
            with the name given within the "'s 
            and the value given after the $.

            Example: decl:float "variable" $54.63

    out:
        @: 
            This command will output the value tied to the name
            specified after the @, but depending on the type,
            will display it slightly differently.
            
            Example: out @"variable"

        i: 
            This command will output the value stored at the index 
            in the Imemory specified by the number after the i,
            which is by default 0.

            Example: out i0

        $:
            This command will output the value specified by the number after the $.

            Example: out $22.5

    aout:
        @:  This command will look to the variable specified within the "'s,
            get the value and depending on the type, output it.
            
            Also, this command does not work with Floats, however OUT does.
            
            Example: aout @"variable"

        i:  This command will output the ascii character
            represented by the number in the Imem at the index
            given after the i.
        
            Example: aout i0

        $: 
            This command will output the ascii character 
            represented by the number given after the $.

            Example: aout $65
    if:
    
        This keyword is unlike the ones above,
        as it is used like this:
        
        if [expression]
            ~Code here
        endif

        what this means, is that @, $ and i are used a bit differently, 
        alongside the syntactic differences.

        if the expression within the [] evaluates to true,
        the code it will run is raised by 4 spaces,
        until it meets an ENDIF on the same level as if.
        
        the operators currently implemented: !=, ==
        
        booleans cannot be used yet within expressions.
        
        if's are nestable.
        if.toye contains an example of this functionality.
        
        a few examples of usage:
        
        if [variable == $30]
            ~Code here
        endif
        if [i0 != another_variable]
            ~Code here
        endif
        if [$13.4 != i6]
            ~Code here
        endif
