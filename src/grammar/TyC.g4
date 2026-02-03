grammar TyC;

@lexer::header {
from lexererr import *
}

@lexer::members {
def emit(self):
    tk = self.type
    if tk == self.UNCLOSE_STRING:       
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
program: EOF;




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

INCREMENT : '++' ;
DECREMENT : '--' ;

ASSIGN : '=' ;
ACCESS : '.' ;



// SEPARATORS --------------------
LP : '(' ;
RP : ')' ;
LSB : '[' ;
RSB : ']' ;
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

FLOAT_LITERAL: '-'? (
    DIGIT+ '.' DIGIT* EXPONENT? |
    '.' DIGIT+ EXPONENT? |
    DIGIT+ EXPONENT
) ;

INTEGER_LITERAL : '-'? DIGIT+ ;



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

UNCLOSE_STRING : '"' 
(
    VALID_ESCAPE
    | ~["\\\r\n]
)*  
    ( '\r' | '\n' | EOF )
{
    self.text = self.text[1:]
} ;

STRING_LITERAL : '"' 
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
WS : [ \t\r\n]+ -> skip ; // skip spaces, tabs
ERROR_CHAR: . ; 


