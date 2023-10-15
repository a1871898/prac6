class VMTranslator:

    def vm_push(segment, offset):
        if segment == "constant":
            return f"@{offset}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        else:
            return f"@{offset}\nD=A\n@{segment.upper()}\nA=M+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
    
    def vm_pop(segment, offset):
        if segment == "constant":
            raise ValueError("Cannot pop into the constant segment")
        else:
            return f"@{offset}\nD=A\n@{segment.upper()}\nD=M+D\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n"

    def vm_add():
        return "@SP\nAM=M-1\nD=M\nA=A-1\nM=D+M\n"

    def vm_sub():
        return "@SP\nAM=M-1\nD=M\nA=A-1\nM=M-D\n"

    def vm_neg():
        return "@SP\nA=M-1\nM=-M\n"

    def vm_eq():
        def vm_eq():
            return """
    // eq
    @SP
    M=M-1
    A=M
    D=M
    A=A-1
    D=D-M
    @EQUAL
    D;JEQ
    @SP
    A=M-1
    M=0
    @CONTINUE
    0;JMP
    (EQUAL)
    @SP
    A=M-1
    M=-1
    (CONTINUE)
    """

    def vm_gt():
        return """
    // gt
    @SP
    M=M-1
    A=M
    D=M
    A=A-1
    D=M-D
    @GREATER
    D;JGT
    @SP
    A=M-1
    M=0
    @CONTINUE
    0;JMP
    (GREATER)
    @SP
    A=M-1
    M=-1
    (CONTINUE)
    """

    def vm_lt():
        return """
    // lt
    @SP
    M=M-1
    A=M
    D=M
    A=A-1
    D=M-D
    @LESS
    D;JLT
    @SP
    A=M-1
    M=0
    @CONTINUE
    0;JMP
    (LESS)
    @SP
    A=M-1
    M=-1
    (CONTINUE)
    """

    def vm_and():
        return """
    // and
    @SP
    M=M-1
    A=M
    D=M
    A=A-1
    M=D&M
    """

    def vm_or():
        return """
    // or
    @SP
    M=M-1
    A=M
    D=M
    A=A-1
    M=D|M
    """

    def vm_not():
        return """
    // not
    @SP
    A=M-1
    M=!M
    """

    def vm_label(label):
        return f"({label})"

    def vm_goto(label):
        return f"@{label}\n0;JMP"

    def vm_if(label):
        return """
    // if-goto
    @SP
    M=M-1
    A=M
    D=M
    @%s
    D;JNE
    """ % label

    def vm_function(function_name, n_vars):
        '''Generate Hack Assembly code for a VM function operation'''
        return ""

    def vm_call(function_name, n_args):
        '''Generate Hack Assembly code for a VM call operation'''
        return ""

    def vm_return():
        '''Generate Hack Assembly code for a VM return operation'''
        return ""

# A quick-and-dirty parser when run as a standalone script.
if __name__ == "__main__":
    import sys
    if(len(sys.argv) > 1):
        with open(sys.argv[1], "r") as a_file:
            for line in a_file:
                tokens = line.strip().lower().split()
                if(len(tokens)==1):
                    if(tokens[0]=='add'):
                        print(VMTranslator.vm_add())
                    elif(tokens[0]=='sub'):
                        print(VMTranslator.vm_sub())
                    elif(tokens[0]=='neg'):
                        print(VMTranslator.vm_neg())
                    elif(tokens[0]=='eq'):
                        print(VMTranslator.vm_eq())
                    elif(tokens[0]=='gt'):
                        print(VMTranslator.vm_gt())
                    elif(tokens[0]=='lt'):
                        print(VMTranslator.vm_lt())
                    elif(tokens[0]=='and'):
                        print(VMTranslator.vm_and())
                    elif(tokens[0]=='or'):
                        print(VMTranslator.vm_or())
                    elif(tokens[0]=='not'):
                        print(VMTranslator.vm_not())
                    elif(tokens[0]=='return'):
                        print(VMTranslator.vm_return())
                elif(len(tokens)==2):
                    if(tokens[0]=='label'):
                        print(VMTranslator.vm_label(tokens[1]))
                    elif(tokens[0]=='goto'):
                        print(VMTranslator.vm_goto(tokens[1]))
                    elif(tokens[0]=='if-goto'):
                        print(VMTranslator.vm_if(tokens[1]))
                elif(len(tokens)==3):
                    if(tokens[0]=='push'):
                        print(VMTranslator.vm_push(tokens[1],int(tokens[2])))
                    elif(tokens[0]=='pop'):
                        print(VMTranslator.vm_pop(tokens[1],int(tokens[2])))
                    elif(tokens[0]=='function'):
                        print(VMTranslator.vm_function(tokens[1],int(tokens[2])))
                    elif(tokens[0]=='call'):
                        print(VMTranslator.vm_call(tokens[1],int(tokens[2])))

        