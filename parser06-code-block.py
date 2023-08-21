
class Token(object):

    def __init__(self,atype,avalue):
        self.type = atype
        self.value = avalue

    def __eq__(self,other):
        if isinstance(other,Token):
            return self.type==other.type and self.value==other.value
        return self.type==other

    def __repr__(self):
        return f"({self.type} {self.value})"

def tokenizer(xs):
    tokens=[]
    symbols = {"{":"lcurly","}":"rcurly",",":"coma","=":"equal", ";":"semi", "(":"lparen",")":"rparen","+":"op","-":"op","*":"op","/":"op" }
    for x in xs:
        if x.isalpha():
            tokens.append( Token("name",x) )
        elif x.isdigit():
            tokens.append( Token("number", int(x)) )
        elif x in symbols.keys():
            tokens.append( Token(symbols[x],x) )
    return tokens


class Parser:
    def __init__(self,code):
        self.code = code
        self.i=0
        self.current = self.code[0]
        
    def next(self):
        self.i+=1
        alist = self.code[self.i:self.i+1] or [Token("eof",object())]
        self.current = alist[0]
    
    def matching(self,*args):
        for i, arg in enumerate(args):
            if arg==None or arg==self.code[self.i+i]:
                continue
            if isinstance(arg,list):
                if self.code[self.i+i] in arg:
                    continue
            return False
        return True
    
    def match(self,a):
        if self.current==a or (isinstance(a,list) and self.current in a):
            result=self.current.value
            self.next()
            return result
        raise Exception(f"error matching {a}")
    
    def parse_function_call(self):
        params = []
        func = self.match("name")
        self.match("lparen")
        while True:
            params.append(self.parse_expression())
            if self.matching("coma"):
                self.match("coma")
                continue
            
            if self.matching("rparen"):
                break
            raise Exception("ERROR: Syntax error while parsing function call")
        self.match("rparen")
        return ["Call",func,params]
    
    def parse_assignment(self):
        name = self.match("name")
        self.match("equal")
        result=["Set",name,self.parse_expression()]
        self.match("semi")
        return result
    
    def parse_statement(self):
        if self.matching("name","equal"):
            return self.parse_assignment()
        if self.matching("name","lparen"):
            return self.parse_function_call()
        if self.matching("lcurly"):
            return self.parse_block()
    
    def parse_block(self):
        self.match("lcurly")
        block = []
        while True:
            if self.matching("rcurly"):
                break
            if self.matching("semi"):
                self.match("semi")
                continue
            block.append(self.parse_statement())
        self.match("rcurly")
        return block
        
    def parse_expression(self,left=False,op=False):
        precedence = {"+":0,"-":0,"*":2,"/":1}
        
        if self.matching("name","lparen"):
            result = self.parse_function_call()
            if left:
                result = [op,left,result]
            if self.matching("op"):
                op2 = self.match("op")
                return self.parse_expression(result,op2)
            return result
        
        if self.matching("lparen"):
            self.match("lparen")
            result=self.parse_expression()
            self.match("rparen")
            if left:
                result = [op,left,result]
            if self.matching("op"):
                op2 = self.match("op")
                return self.parse_expression(result,op2)
            return result
            
        if self.matching(["name","number"], ["semi","rparen","coma"]):
            name_or_number = self.match(["name","number"])
            if left:
                return [op,left,name_or_number]
            return name_or_number
        
        if self.matching(["name","number"],"op") and left:
            name_or_number = self.match(["name","number"])
            op2 = self.match("op")
            if precedence[op]>precedence[op2]:
                return self.parse_expression([op,left,name_or_number],op2)
            return [op,left,self.parse_expression(name_or_number,op2)]
        
        if self.matching(["name","number"], "op"):
            name_or_number = self.match(["name","number"])
            op2 = self.match("op")
            return self.parse_expression(name_or_number,op2)
    
p=Parser(tokenizer("{a=b;}"))
print(p.parse_statement())
