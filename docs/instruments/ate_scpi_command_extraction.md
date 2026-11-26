# Introduction
The file is instructions for read and indentify SCPI command of ATE (Automation Test empuiqment).

# Rule
- Read and understand ATE user manual. (don't use data in other source)
- Identify available SCPI commands.
- explain command syntax and parameter
- Record commands in a structured format.
- Include page numbers and manual references.
- Avoid inventing commands that are not documented.
- rule for read SCPI command
SCPI Command Syntax			
	Rule	Description	Example
1	Uppercase letters	Abbreviated command is accepted	VOLT
2	Lowercase letters	Full command is accepted	VOLTage
3	Case sensitivity	SCPI is case-insensitive	Volt, VOLT
4	{ }	Required selection between parameters	{MIN|MAX|DEF}
5	[ ]	Optional command or parameter	[SENSe:]
6	< >	Parameter requiring a value	<range>
7	?	Query current setting or measurement	VOLT:DC:RANG?
8	;	Separate multiple commands	*RST;*CLS

# Output
type as file <manufacture><emquiqment-name>.md
## 1. Introduction
## 2. Connections
## 3. SCPI TABLE
	CMD	Range	Functions	Sample
1	CONFigure?		Query current measurement configuration
2	CONFigure:CONTinuity		Configure continuity measurement
3	CONFigure:CURRent:{AC|DC} [{<range>|AUTO|MIN|MAX|DEF}]	200uA, 2mA, 20mA, 200mA, 2A, 10A	Configure AC/DC current measurement


