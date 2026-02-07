grammar TyC;

@lexer::header {
from lexererr import *
}

@lexer::members {
def emit(self):
    tk = self.type
    if tk == self.UNCLOSE_STRING or tk == self.UNCLOSE_STRING2:      
        result = super().emit();
        raise UncloseString(result.text);
    elif tk == self.ILLEGAL_ESCAPE:
        result = super().emit();
        raise IllegalEscape(result.text);
    elif tk == self.ERROR_CHAR:
        result = super().emit();
        raise ErrorToken(result.text); 
    else:
        return super().emit();
}

options{
	language=Python3;
}

// ---------------------------- //
//         PARSER RULES         //
// ---------------------------- //

// PROGRAM -----------------------
program : (structDecl | funcDecl)* EOF ;



// TYPES ------------------------
type : INT | FLOAT | STRING | ID ;



// DECLARATION -------------------
structDecl : STRUCT ID LB structMember* RB SEMICOLON ;
structMember : type ID SEMICOLON ;

funcDecl : returnType? ID LP paramList? RP block ;
paramList : param (COMMA param)* ;
param : type ID ;
returnType : VOID | type ;



// STATEMENT ---------------------
statement 
    : varDecl
    | exprStmt
    | ifStmt
    | whileStmt
    | forStmt
    | switchStmt
    | block
    | returnStmt
    | breakStmt
    | continueStmt
    ;

varDecl
    : AUTO ID (ASSIGN expr)? SEMICOLON
    | type ID (ASSIGN expr | ASSIGN struct_lit)? SEMICOLON
    ;
struct_lit : LB (expr (COMMA expr)*)? RB ;

exprStmt : expr SEMICOLON ;
block : LB statement* RB ;

ifStmt : IF LP expr RP statement (ELSE statement)? ;
whileStmt : WHILE LP expr RP statement ;

forStmt : FOR LP forInit? SEMICOLON forCond? SEMICOLON forUpdate? RP statement ;
forInit : forVarDecl | expr ;
forCond : expr ;
forVarDecl 
    : AUTO ID (ASSIGN expr)? 
    | type ID (ASSIGN expr | ASSIGN struct_lit)?
    ;

forUpdate : lhs ASSIGN assignExpr | inc_dec ;
inc_dec 
    : (INCREMENT | DECREMENT) lhs
    | lhs (INCREMENT | DECREMENT)
    ;

switchStmt : SWITCH LP expr RP LB caseClause* defaultClause? caseClause* RB ;
caseClause : CASE expr COLON statement* ;
defaultClause : DEFAULT COLON statement* ;

returnStmt : RETURN expr? SEMICOLON ;
breakStmt : BREAK SEMICOLON ;
continueStmt : CONTINUE SEMICOLON ;



// EXPRESSION --------------------
expr : assignExpr ;
assignExpr : lhs ASSIGN assignExpr | orExpr ;

lhs : ID (ACCESS ID)* 
    | LP lhs RP (ACCESS ID)* 
    ;

orExpr : andExpr (OR andExpr)* ;
andExpr : equalExpr (AND equalExpr)* ;

equalExpr : relationalExpr ((EQUAL | NOT_EQUAL) relationalExpr)* ;
relationalExpr : addiExpr ((LESS | EQUAL_LESS | GRAT | EQUAL_GRAT ) addiExpr)* ;

addiExpr : multiExpr ((ADD | SUB) multiExpr)* ;
multiExpr : unaryExpr ((MUL | DIV | MOD) unaryExpr)* ;

unaryExpr 
    : (ADD | SUB | NOT) unaryExpr 
    | (INCREMENT | DECREMENT) lhs
    | postfixExpr 
    ;

postfixExpr
    : lhs postfixIncDec?         
    | primaryExpr                          
    ;
postfixIncDec : (INCREMENT | DECREMENT)+ ;

primaryExpr : atom (ACCESS ID)* ;
atom
    : literal
    | ID
    | funcCall
    | struct_lit
    | LP expr RP
    ;

literal : INT_LIT | FLOAT_LIT | STRING_LIT ;
funcCall : ID LP argList? RP ;
argList : expr (COMMA expr)* ;





// ---------------------------- //
//         LEXER RULES          //
// ---------------------------- //

// KEYWORDS ----------------------
DEFAULT : 'default' ;
AUTO : 'auto' ;
INT : 'int' ;
FLOAT : 'float' ;
STRING : 'string' ;
VOID : 'void' ;
STRUCT : 'struct' ;

IF : 'if' ;
ELSE : 'else' ;
SWITCH : 'switch' ;
CASE : 'case' ;

FOR : 'for';
WHILE : 'while' ;
BREAK : 'break' ;
CONTINUE : 'continue' ;

RETURN : 'return' ;



// OPERATORS ---------------------
INCREMENT : '++' ;
DECREMENT : '--' ;

ADD : '+' ;
SUB : '-' ;
MUL : '*' ;
DIV : '/' ;
MOD : '%' ;

EQUAL : '==' ;
NOT_EQUAL : '!=' ;
EQUAL_LESS : '<=' ;
EQUAL_GRAT : '>=' ;
LESS : '<' ;
GRAT : '>' ;

AND : '&&' ;
OR : '||' ;
NOT : '!' ;

ASSIGN : '=' ;
ACCESS : '.' ;



// SEPARATORS --------------------
LP : '(' ;
RP : ')' ;
LB : '{' ;
RB : '}' ;

SEMICOLON : ';' ;
COMMA : ',' ;
COLON : ':' ;



// IDENTIFIER --------------------
ID: [a-zA-Z_][a-zA-Z0-9_]* ;


   
// LITERALS ----------------------
fragment DIGIT : [0-9] ;
fragment EXPONENT : [eE] [+-]? DIGIT+ ; 

FLOAT_LIT: (
    DIGIT+ '.' DIGIT* {self.text.count('.') == 1}? EXPONENT? |
    '.' DIGIT+ EXPONENT? |
    DIGIT+ EXPONENT
) ;

INT_LIT : DIGIT+ ;



// STRING_LITERAL ----------------
fragment ESCAPE_CHAR : [bfrnt"\\] ;
fragment VALID_ESCAPE : '\\' ESCAPE_CHAR ;
fragment INVALID_ESCAPE : '\\' ~[bfrnt"\\\r\n] ;

ILLEGAL_ESCAPE : '"' 
(
    VALID_ESCAPE
    | ~["\\\r\n]
)*  
    INVALID_ESCAPE 
{ 
    self.text = self.text[1:]            #error text = content without opening quote
} ;           

// Unclosed string when backslash is immediately followed by newline or EOF
UNCLOSE_STRING2 : '"' 
(
    VALID_ESCAPE
    | ~["\\\r\n]
)*  
    '\\' ( '\r' | '\n' | EOF )
{
    self.text = self.text[1:]
} ;

UNCLOSE_STRING : '"' 
(
    VALID_ESCAPE
    | ~["\\\r\n]
)*  
    ( '\r' | '\n' | EOF )
{
    self.text = self.text[1:]
} ;

STRING_LIT : '"' 
(
    VALID_ESCAPE
    | ~["\\\r\n]      
)*  
    '"'
{       
    self.text = self.text[1:-1]            #strip surrounding quotes
} ;



// COMMENTS ----------------------
LINE_COMMENT : '//' ~[\r\n]* -> skip ;
BLOCK_COMMENT : '/*' .*? '*/' -> skip ;



// OTHERS ------------------------
WS : [ \t\r\n\f]+ -> skip ; // skip spaces, tabs
ERROR_CHAR: . ;