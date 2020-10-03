class Interpreter:
    def __init__(self):
        self.scope=[{}]
        
    def run(self,code):
        for xs in code:
            self.eval(xs)
            
    def eval(self,xs):
        if isinstance(xs,list):
            return self.__getattribute__(xs[0])(xs)
        return xs
    
    def Print(self,xs):
        if len(xs)==1:
            print()
            return
        l=len(xs)-1
        for i,x in enumerate(xs[1:]):
            e=self.eval(x)
            if i<l-1:
                print(e,end="")
            else:
                if e!=",":
                    print(e)
                else:
                    print(e,end="")
    
    def Add(self,xs):
        return self.eval(xs[1])+self.eval(xs[2])
    def Sub(self,xs):
        return self.eval(xs[1])-self.eval(xs[2])
    def Mul(self,xs):
        return self.eval(xs[1])*self.eval(xs[2])
    def Div(self,xs):
        return self.eval(xs[1])/self.eval(xs[2])
    
    def If(self,xs):
        _,cond,trueblock,elseblock=xs
        if self.eval(cond):
            if isinstance(trueblock[0],list):
                for x in trueblock:
                    self.eval(x)
            else:
                self.eval(trueblock)
        else:
            if isinstance(elseblock[0],list):
                for x in elseblock:
                    self.eval(x)
            else:
                self.eval(elseblock)
    def Lt(self,xs):
        return self.eval(xs[1])<self.eval(xs[2])
    def Gt(self,xs):
        return self.eval(xs[1])>self.eval(xs[2])
    def Lte(self,xs):
        return not self.Gt(xs)
    def Gte(self,xs):
        return not self.Lt(xs)
    def Eq(self,xs):
        return self.eval(xs[1])==self.eval(xs[2])
    def NotEq(self,xs):
        return not self.Eq(xs)
    
    def Set(self,xs):
        _, key, val = xs
        self.scope[-1][key] = self.eval(val)
        
    def Get(self,xs):
        _, key = xs
        if key in self.scope[-1]:
            return self.scope[-1][key]
        elif key in self.scope[-1]:
            return self.scope[0][key]
        raise Exception("error: variable not found: "+key) 
    
    def While(self,xs):
        _ , cond , block = xs
        while self.eval(cond):
            if isinstance(block[0],list):
                for x in block:
                    self.eval(x)
            else:
                self.eval(block)
        
code=[
    
    ["Set","sum",0],
    
    ["Set","i",0],
    
    ["While", ["Lt", ["Get","i"], 100], [
        
        ["Set","i", ["Add",["Get","i"], 1] ],
        ["Set","sum", ["Add",["Get", "sum"],["Get","i"]]]
    ]],
    
    ["Print","sum(1..100) = ",["Get","sum"] ]
]
    
interpreter=Interpreter()

interpreter.run(code)
