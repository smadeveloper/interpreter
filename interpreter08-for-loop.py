class Interpreter:
    def __init__(self):
        self.scope=[{}]
        self.loop_stack=[]
        
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
            if elseblock:
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
 
    
    def Break(self,xs):
        self.loop_stack[-1]["break"]=True
    def Continue(self,xs):
        self.loop_stack[-1]["continue"]=True
        
    def While(self,xs):
        self.loop_stack.append({"break":False,"continue":False})
        _ , cond , block = xs
        while self.eval(cond):
            if isinstance(block[0],list):
                for x in block:
                    self.eval(x)
                    if self.loop_stack[-1]["break"]:
                        self.loop_stack.pop()
                        return
                    if self.loop_stack[-1]["continue"]:
                        self.loop_stack[-1]["continue"]=False
                        break
            else:
                self.eval(block)
        self.loop_stack.pop()
    
    def For(self,xs):
        self.loop_stack.append({"break":False,"continue":False})        
        _, inits, cond, increments, block = xs
        for x in inits: 
            self.eval(x)
        while self.eval(cond):
            if isinstance(block[0],list):
                for x in block:
                    self.eval(x)
                    if self.loop_stack[-1]["break"]:
                        self.loop_stack.pop()
                        return
                    if self.loop_stack[-1]["continue"]:
                        self.loop_stack[-1]["continue"]=False
                        break
            else:
                self.eval(block) 
            for x in increments:
                self.eval(x)
        self.loop_stack.pop()
        
code=[
    
    ["Set","sum",0],
    
    ["For", [["Set","i",0]], 
            ["Lt", ["Get","i"], 100], 
            [["Set","i", ["Add",["Get","i"], 1] ]],   
    [   
        
        ["Set","sum", ["Add",["Get", "sum"],["Get","i"]]],
        
        ["Print","i=",["Get","i"],", sum=",["Get","sum"]],
        
        ["If", ["Eq", ["Get", "i"], 10], 
             ["Break"],[]
        ],
        
        
    ]],
    
]
    
interpreter=Interpreter()

interpreter.run(code)
