# toyeso
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

    - Capitals are optional for keywords,
        but are not for special use characters(such as i or $)

    ~ Every program must define the size of the Imemory
        (the place for storing constant numbers int, or float.)

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

There are a few keywords, I'll list them now.
    (The full descriptions will be at the end.)

    const:
        stores constant number in the Imemory
        where the next index is available.

        Example "const 55"

    decl:
        plain: <not implemented>

        i: <not implemented>

        $:
            creates a variable with the name given within the "'s 
            and the value given after the $.

            Example "decl "variable" $54.63"

    out:
        plain: <not implemented>

        i: 
            This command will output the value stored at the index 
            in the Imemory specified by the number after the i,
            which is by default 0.

            Example "out i0"

        $:
            This command will output the value specified by the number after the $.

            Example "out $22.5"

    aout:
        plain: <not implemented>

        i: <not implemented>

        $: 
            This command will output the ascii character 
            represented by the number given after the $.

            Example "aout $65"
