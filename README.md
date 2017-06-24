# toyeso
A toy esoteric language project created by mynameajeff.

The concept/s(currently):

    - The Imemory, it is a place to store numbers immutably for use until the program ends.
    - The Imemory is limited, with a maximum size of 4096 cells.
    (more space than anyone needs for this purpose really)

The syntax(currently):

    - every file must begin with either START or start.
    - every file must end with either END or end.
    - the keywords available are such:
    -     store or STORE
    -     out or OUT
    -     aout or AOUT

~~~~~~~~~~~~~~~~
The STORE keyword:
    this keyword will store the number given to it in the next available slot of Imemory.
    example of use:
        'store 202.44'
    output:
        'imemory: stored 202.44 at index 0.'
~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~
The OUT keyword:
this keyword has two ways of use: with $ and without $    
    without $: this references a number in imemory, for example: 0 would be the first item saved to imem
    example of use:
        'out 0'
    output:
        'imemory: at index 0 there is "202.44"'

    with $: this prints out 'direct: input was "££".' with ££ being the number passed after the $.
    example of use:
        'out $0'
    output:
        'direct: input was "0".'
~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~
The AOUT keyword:
this keyword has two ways of use: with $ and without $    
    without $: <not implemented>
    
    with $: this prints out 'ascii output: $$' with $$ being the ascii character at the number given
    example of use:
        'aout $65'
    output:
        'ascii output: A'
