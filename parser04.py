
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
    symbols = {"(":"lparen",")":"rparen","=":"equal", ";":"semi", "+":"op","-":"op","*":"op","/":"op" }
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
        for i,arg in enumerate(args):
            if arg==None or arg==self.code[self.i+i]:
                continue
            if isinstance(arg,list):
                if self.code[self.i+i] in arg:
                    continue
            return False
        return True
    
    def match(self, a):
        if self.current==a or (isinstance(a,list) and self.current in a):
            result=self.current.value
            self.next()
            return result

        raise Exception(f"match error: {a}")

    def parse_expression(self,left=False,op=False):

        precedence ={"+":0,"-":0,"*":2,"/":1}

        if self.matching("lparen"):
            self.match("lparen")
            result = self.parse_expression()
            self.match("rparen")
            if left:
                result = [op,left,result]
            if self.matching("op"):
                op2 = self.match("op")
                return self.parse_expression(result,op2)
            return result
        
        if self.matching(["name","number"],["semi","rparen"]):
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

        if self.matching(["name","number"],"op"):
            name_or_number = self.match(["name","number"])
            op = self.match("op")
            return self.parse_expression(name_or_number,op)
    
p=Parser(tokenizer("(1+2)+(3+4);"))
print(p.parse_expression());
