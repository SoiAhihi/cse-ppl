
"""
 * @author nhphung
"""
from abc import ABC, abstractmethod, ABCMeta
from dataclasses import dataclass
from typing import List, Tuple
from AST import * 
from Visitor import *
from StaticError import *
from functools import *

class Type(ABC):
    __metaclass__ = ABCMeta
    pass
class Prim(Type):
    __metaclass__ = ABCMeta
    pass
class IntType(Prim):
    pass
class FloatType(Prim):
    pass
class StringType(Prim):
    pass
class BoolType(Prim):
    pass
class VoidType(Type):
    pass
class Unknown(Type):
    pass

@dataclass
class ArrayType(Type):
    dimen:List[int]
    eletype: Type

@dataclass
class MType:
    intype:List[Type]
    restype:Type

@dataclass
class Symbol:
    name: str
    mtype:Type

class StaticChecker(BaseVisitor):
    def __init__(self,ast):
        self.ast = ast
        self.global_envi = [
Symbol("int_of_float",MType([FloatType()],IntType())),
Symbol("float_of_int",MType([IntType()],FloatType())),
Symbol("int_of_string",MType([StringType()],IntType())),
Symbol("string_of_int",MType([IntType()],StringType())),
Symbol("float_of_string",MType([StringType()],FloatType())),
Symbol("string_of_float",MType([FloatType()],StringType())),
Symbol("bool_of_string",MType([StringType()],BoolType())),
Symbol("string_of_bool",MType([BoolType()],StringType())),
Symbol("read",MType([],StringType())),
Symbol("printLn",MType([],VoidType())),
Symbol("printStr",MType([StringType()],VoidType())),
Symbol("printStrLn",MType([StringType()],VoidType()))]                           
   
    def check(self):
        return self.visit(self.ast,self.global_envi)



    def get(self,name,c):
        local =[i for i in c[1]] 
        unlocal = [i for i in c[0]]
        for i in local:
            if i.name == name:
                return i.mtype
        else:
            for x in unlocal:
                if x.name == name:
                    return x.mtype
            else:
                return -1
    def update(self,name,typ,c):
        pass


    def visitProgram(self,ast, c):
        Global =[self.global_envi,[]]
        reduce(lambda x,y: self.visit(y,x),ast.decl,Global)
    

    def visitVarDecl(self, ast, param):
        name =ast.variable.name
        if isinstance(param,list):
            if self.get(name,param) != -1:
                raise Redeclared(Variable(),name)
            typ = Unknown()
            if ast.varInit != None:
                typ = self.visit(ast.varInit,param)
            if isinstance(typ,ArrayType):
                typ.dimen =  ast.varDimen
            param[1].extend([Symbol(name,typ)])    
            return param
        else:
            if name in [i.variable.name for i in param]:
                raise Redeclared(Parameter(),name)
            param += (Symbol(name,Unknown()))
            return param
    


    def visitFuncDecl(self, ast, param):
        if self.get(ast.name,param) != -1:
                raise Redeclared(Function(),ast.name)
        params = reduce(lambda x,y:self.visit(y,x),ast.param,())

        param[1].extend([Symbol(ast.name,MType(list(params),VoidType()))])
        unlocal = []
        unlocal.extend(param[1])
        for i in param[0]:
            if i.name not in [x.name for x in unlocal]:
                unlocal.extend([i])
        else:
            pass
        local=[]
        local.extend(list(params))

        dec=[unlocal,local]
        reduce(lambda x,y:self.visit(y,x),ast.body[0],dec)


        return param

    def visitBinaryOp(self, ast, param):
        return None
    
    def visitUnaryOp(self, ast, param):
        return None
    
    def visitCallExpr(self, ast, param):
        return None
    
    def visitId(self, ast, param):
        return None
    
    def visitArrayCell(self, ast, param):
        return None
    
    def visitAssign(self, ast, param):
        return None
    
    def visitIf(self, ast, param):
        return None
    
    def visitFor(self, ast, param):
        return None
    
    def visitContinue(self, ast, param):
        return None
    
    def visitBreak(self, ast, param):
        return None
    
    def visitReturn(self, ast, param):
        return None
    
    def visitDowhile(self, ast, param):
        return None

    def visitWhile(self, ast, param):
        return None

    def visitCallStmt(self, ast, param):
        return None

    def visitIntLiteral(self, ast, param):
        return IntType()
    
    def visitFloatLiteral(self, ast, param):
        return FloatType()
    
    def visitBooleanLiteral(self, ast, param):
        return BoolType()
    
    def visitStringLiteral(self, ast, param):
        return StringType()

    def visitArrayLiteral(self, ast, param):
        init = self.visit(ast.value[0],param)
        for i in [self.visit(_,param) for _ in ast.value[1:]]:
            if type(i) != type(init):
                pass
        return ArrayType([],init)
