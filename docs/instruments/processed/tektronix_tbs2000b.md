# Tektronix TBS2000B Series SCPI Command Reference

> **Source restriction:** Prepared only from the supplied `<File>TBS2000B-Programmer-Manual-EN-US-077114904.pdf</File>`, document number 077-1149-04, May 2024. No commands or parameters were added from external sources.

## 1. Introduction

This document is a structured reference for remotely controlling Tektronix TBS2000B Series digital oscilloscopes. It records the command syntax, documented argument choices or numeric limits, function, sample command, and printed manual page.

The manual uses Tektronix/IEEE 488.2 command conventions and Backus-Naur Form (BNF). Commands are accepted through Ethernet or USB; the protocol table additionally marks GPIB as supported and RS-232 as unsupported for the documented model/option. Refer to the product user manual for physical remote-connectivity setup and testing.

### 1.1 SCPI and BNF syntax rules

| Rule | Description | Example |
|---|---|---|
| Uppercase letters | Minimum accepted abbreviation | `ACQ:NUMA` |
| Lowercase letters | Remaining characters in full mnemonic | `ACQuire:NUMAVg` |
| Case sensitivity | Commands may be entered in uppercase or lowercase | `ACQ:MODE`, `acq:mode` |
| `{ }` | Group containing one required choice | `{SAMple|PEAKdetect|HIRes|AVErage}` |
| `[ ]` | Optional element | `HORizontal[:MAIn]:SCAle` |
| `< >` | Defined element or value placeholder | `<NR3>`, `<QString>` |
| `|` | Exclusive OR between alternatives | `{AC|DC}` |
| `...` | Previous element may repeat | `<Argument>[,<Argument>...]` |
| `?` | Query form | `ACQuire:MODe?` |
| `:` | Separates hierarchical mnemonics | `TRIGger:A:EDGE:SLOpe` |
| `;` | Concatenates commands/queries | `ACQ:MODE AVERAGE;NUMAVG 16` |
| `,` | Separates multiple arguments | `SAVE:WAVEFORM CH1,REF1` |
| `*` | IEEE 488.2 common command | `*IDN?` |

### 1.2 Argument types

| Type | Meaning |
|---|---|
| `<NR1>` | Signed integer |
| `<NR2>` | Floating-point value without exponent |
| `<NR3>` | Floating-point value with exponent |
| `<QString>` | ASCII string enclosed by matching single or double quotes |
| `<Block>` | Definite or indefinite-length binary block |
| `CH<x>` | Channel specifier; model-dependent, typically CH1-CH2 or CH1-CH4 |
| `REF<x>` | Reference waveform specifier; typically REF1-REF2 |
| `MEAS<x>` | Automated measurement slot; x = 1-6 |
| `<wfm>` | Waveform: `CH<x>`, `MATH`, or `REF<y>` |

Incorrect numeric values may be clamped to the nearest supported minimum/maximum or rounded to a supported value. Therefore, software should query the setting after writing a value when exact acceptance matters.

## 2. Connections

| Interface / item | Manual information | Page |
|---|---|---:|
| Ethernet | Supported for remote control. Physical setup is delegated to the product user manual. | 14-15 |
| USB | Supported using USBTMC/USB488-style communication. USB EOM is indicated in the USB header and responses end with LF. | 14-19 |
| GPIB | Protocol table marks GPIB supported. GPIB messages may terminate with EOI, LF, or both. | 15, 18, 23 |
| RS-232 | Protocol table marks RS-232 unsupported for the documented model/option, although general command-format text discusses legacy RS-232 behavior. | 15, 17, 22 |
| ASCII | Commands use enhanced ASCII encoding. | 15 |
| Output queue | Read each query response before sending the next terminated message, or the prior response can be lost and a query error raised. | 17, 207 |
| Header control | `HEADer` enables/disables headers in query responses; `VERBose` selects full or abbreviated returned keywords. | 17, 107, 183 |
| Default TCP port | The manual states default port 4000 in the setup/time command section. | 164 |

### 2.1 Message termination and concatenation

- GPIB accepts EOI, LF, or both; CR LF is accepted because whitespace before the terminator is allowed.
- USB uses the EOM bit in the USBTMC header and terminates responses with LF.
- Unrelated command trees in a concatenated message require `;:` before the next root command.
- Commands sharing the same tree may omit repeated leading mnemonics.
- Star commands must not be preceded by a colon.
- A query returning arbitrary data, such as `ID?`, must be last in a concatenated message.

## 3. SCPI TABLE

The tables below list the commands documented in the manual. A blank Range/Parameters cell means the command has no argument or the command-group summary does not state a fixed numeric range.
### 3.1 Acquisition and Alias

| CMD | Range / Parameters | Function | Sample | Page |
|---|---|---|---|---:|
| `ACQuire?` |  | Query current stop-after, state, mode, and average count. | `ACQ?` | 41 |
| `ACQuire:MAXSamplerate?` | Model-dependent | Query maximum real-time sample rate. | `ACQ:MAXS?` | 41 |
| `ACQuire:MODe {SAMple|PEAKdetect|HIRes|AVErage}` | Required mode selection | Set/query acquisition mode. | `ACQ:MODE AVERAGE` | 41-42 |
| `ACQuire:NUMACq?` | Returns `<NR1>` | Query acquisitions since acquisition started/reset. | `ACQ:NUMACQ?` | 42-43 |
| `ACQuire:NUMAVg <NR1>` | 2-512, powers of two | Set/query acquisitions used for averaging. | `ACQ:NUMAVG 16` | 43 |
| `ACQuire:STATE {OFF|ON|RUN|STOP|<NR1>}` | 0 stops; nonzero starts | Start or stop acquisition. | `ACQ:STATE RUN` | 43-44 |
| `ACQuire:STOPAfter {RUNSTop|SEQuence}` | Continuous or single sequence | Set/query when acquisition stops. | `ACQ:STOPA SEQ` | 44 |
| `ALIas {OFF|ON|<NR1>}` | 0 OFF; nonzero ON | Enable/query alias expansion. | `ALIAS ON` | 45 |
| `ALIas:CATalog?` |  | Return defined alias labels. | `ALIAS:CAT?` | 45 |
| `ALIas:DEFine <QString>,{<QString>|<Block>}` | Label <=12 chars; body <=256 chars | Define/query a command-sequence alias. | `ALIAS:DEFINE "ST1",":RECALL:SETUP 5;:AUTOSET EXECUTE"` | 46 |
| `ALIas:DELEte <QString>` | Existing alias name | Delete one alias. | `ALIAS:DELETE "SETUP1"` | 46-47 |
| `ALIas:DELEte:ALL` |  | Delete all aliases. | `ALIAS:DELETE:ALL` | 47 |
| `ALIas:DELEte[:NAMe] <QString>` | Existing alias name | Delete one named alias. | `ALIAS:DELETE:NAME "STARTUP"` | 47 |
| `ALIas[:STATE] {OFF|ON|<NR1>}` | 0 OFF; nonzero ON | Enable/query alias state. | `ALIAS:STATE OFF` | 48 |

### 3.2 Calibration, diagnostics, status, and IEEE 488.2

| CMD | Range / Parameters | Function | Sample | Page |
|---|---|---|---|---:|
| `*CAL?` | Returns 0 on success | Run internal self-calibration and return status; disconnect signals first. | `*CAL?` | 52 |
| `CALibrate:INTERNAL` |  | Start signal-path compensation. | `CAL:INTERNAL` | 52 |
| `CALibrate:INTERNal:STARt` |  | Start internal SPC. | `CAL:INTERNAL:START` | 53 |
| `CALibrate:INTERNal:STATus?` | `INIT|PASS|FAIL|RUNNING` | Query SPC status. | `CAL:INTERNAL:STATUS?` | 53 |
| `CALibrate:RESults?` | Status string | Query calibration readiness without running calibration. | `CAL:RESULTS?` | 54 |
| `CALibrate:RESults:SPC?` | `INIT|PASS|FAIL|RUNNING` | Query last SPC result. | `CAL:RESULTS:SPC?` | 54 |
| `DIAg:FAN?` | PWM and voltage | Read current PWM fan value. | `DIAG:FAN?` | 81 |
| `DIAg:LOOP:OPTion {ALWAYS|FAIL|ONFAIL|ONCE|NTIMES}` | Required selection | Set diagnostic loop behavior. | `DIAG:LOOP:OPTION ONCE` | 81 |
| `DIAg:LOOP:OPTion:NTIMes <NR1>` | Loop count | Set/query diagnostic loop count. | `DIAG:LOOP:OPTION:NTIMES 3` | 81-82 |
| `DIAg:LOOP:STOP` |  | Stop self-test after current loop. | `DIAG:LOOP:STOP` | 82 |
| `DIAg:RESUlt:FLAg?` | `PASS|FAIL` | Query overall result of last diagnostics. | `DIAG:RESULT:FLAG?` | 82 |
| `DIAg:RESUlt:LOG?` | Quoted result log | Query last diagnostic result log. | `DIAG:RESULT:LOG?` | 83 |
| `DIAg:SELect {ALL|APPKey|CPU|DISplay|FPAnel|IO|ROM|ACQ}` | Required diagnostic group | Select diagnostic group. | `DIAG:SELECT ALL` | 83 |
| `DIAg:SELect:<function>` | `ACQ|CPU|DISplay|FPAnel|IO|ROM` | Select one subsystem for self-test. | `DIAG:SELECT:ACQ` | 84 |
| `DIAg:STATE {EXECute|ABORt}` | Required action | Start or stop self-test. | `DIAG:STATE EXECUTE` | 84 |
| `DIAg:TEMPVAL?` | FPGA and ambient temperature | Read internal temperatures. | `DIAG:TEMPVAL?` | 85 |
| `ALLEv?` | Event code/message list | Return and remove all queued events. | `ALLEV?` | 48-49 |
| `BUSY?` | 0 not busy; 1 busy | Query extended-operation busy state. | `BUSY?` | 51 |
| `*CLS` |  | Clear event queue, SESR and SBR except MAV. | `*CLS` | 65 |
| `DESE <NR1>` | 0-255 | Set/query Device Event Status Enable Register. | `DESE 209` | 80 |
| `*ESE <NR1>` | 0-255 | Set/query Event Status Enable Register. | `*ESE 209` | 88-89 |
| `*ESR?` | 0-255 | Read and clear Standard Event Status Register. | `*ESR?` | 89 |
| `EVENT?` | Event code | Read/remove one event code. | `EVENT?` | 89-90 |
| `EVMsg?` | Event code and message | Read/remove one event with explanation. | `EVMSG?` | 90 |
| `EVQty?` | Event count | Query number of queued events. | `EVQTY?` | 91 |
| `ERRLOG:FIRST?` | String | Read first error-log entry. | `ERRLOG:FIRST?` | 88 |
| `ERRLOG:NEXT?` | String | Read next error-log entry. | `ERRLOG:NEXT?` | 88 |
| `*OPC` / `*OPC?` | Query returns 1 when complete | Signal or wait for completion of pending OPC operations. | `ACQ:STATE ON;*OPC?` | 149 |
| `*PSC {OFF|ON|<NR1>}` | 0 preserve; nonzero clear at power-on | Control power-on status register initialization. | `*PSC 1` | 150 |
| `*SRE <NR1>` | 0-255 | Set/query Service Request Enable Register. | `*SRE 32` | 164-165 |
| `*STB?` | 0-255 | Read Status Byte Register. | `*STB?` | 165 |
| `*WAI` |  | Block further command processing until pending OPC operations complete. | `ACQ:STATE ON;*WAI` | 184 |

### 3.3 Vertical channels and waveform selection

| CMD | Range / Parameters | Function | Sample | Page |
|---|---|---|---|---:|
| `CH<x>?` | x is model-dependent channel | Query all vertical parameters for a channel. | `CH1?` | 55 |
| `CH<x>:AMPSVIAVOLTs:ENABLe {ON|OFF|<NR1>}` | 0 OFF; nonzero ON | Enable/query current-via-volts measurement. | `CH1:AMPSVIAVOLTS:ENABLE ON` | 55 |
| `CH<x>:AMPSVIAVOLTs:FACTOR <NR3>` | Current factor | Set/query amperes-per-volt factor. | `CH1:AMPSVIAVOLTS:FACTOR 1` | 56 |
| `CH<x>:BANdwidth {TWEnty|FULl|<NR3>}` | 20 MHz, full, or supported value | Set/query channel bandwidth limit. | `CH1:BANDWIDTH TWENTY` | 56 |
| `CH<x>:COUPling {AC|DC}` | Required coupling | Set/query input coupling. | `CH1:COUPLING AC` | 57 |
| `CH<x>:DESKew <NR3>` | -100 ns to +100 ns, 1 ns resolution | Set/query channel deskew. | `CH2:DESKEW 5E-9` | 57 |
| `CH<x>:INVert {ON|OFF}` | Boolean | Set/query inversion. | `CH1:INVERT ON` | 58 |
| `CH<x>:LABel <QString>` | Up to 30 characters | Set/query waveform label. | `CH1:LABEL "ICCDATA"` | 58 |
| `CH<x>:OFFSet <NR3>` | Scale-dependent; +/-0.8 V or +/-20 V at 1x probe | Set/query acquisition-window vertical offset. | `CH1:OFFSET 2E-3` | 59 |
| `CH<x>:POSition <NR3>` | -5 to +5 divisions | Set/query vertical display position. | `CH2:POSITION 1.3` | 59-60 |
| `CH<x>:PRObe?` |  | Query attached probe information. | `CH1:PROBE?` | 60 |
| `CH<x>:PRObe:GAIN <NR3>` | Probe-dependent | Set/query probe gain. | `CH1:PROBE:GAIN 0.1` | 60-61 |
| `CH<x>:PRObe:ID?` | Type and serial | Query probe type and serial number. | `CH1:PROBE:ID?` | 61 |
| `CH<x>:PRObe:ID:SERnumber?` | String | Query probe serial number. | `CH1:PROBE:ID:SERNUMBER?` | 61 |
| `CH<x>:PRObe:ID:TYPE?` | String | Query probe type. | `CH1:PROBE:ID:TYPE?` | 62 |
| `CH<x>:PRObe:SIGnal {BYPass|PASS}` | Supported TekVPI probes | Set/query probe input bypass. | `CH1:PROBE:SIGNAL PASS` | 62 |
| `CH<x>:PRObe:UNIts?` | String | Query probe units. | `CH1:PROBE:UNITS?` | 62-63 |
| `CH<x>:SCAle <NR3>` | Probe- and model-dependent units/div | Set/query vertical scale. | `CH1:SCALE 100E-3` | 63 |
| `CH<x>:VOLts <NR3>` | Volts/div; alias of SCAle | Set/query vertical sensitivity. | `CH1:VOLTS 1.0` | 64 |
| `CH<x>:YUNit <QString>` | Documented unit strings | Set/query channel engineering units. | `CH2:YUNIT "V"` | 64 |
| `SELect:CH<x> {ON|OFF|<NR1>}` | 0 OFF; nonzero ON | Show/hide and select channel. | `SELECT:CH2 ON` | 160-161 |
| `SELect:CONTROl {CH<x>|MATH|FFT|REF<x>}` | Required waveform | Set/query waveform receiving front-panel-like controls. | `SELECT:CONTROL CH1` | 161 |
| `SELect:FFT {ON|OFF|<NR1>}` | Boolean | Show/hide FFT waveform. | `SELECT:FFT ON` | 161-162 |
| `SELect:MATH {ON|OFF|<NR1>}` | Boolean | Show/hide math waveform. | `SELECT:MATH ON` | 162 |
| `SELect:REF<x> {ON|OFF|<NR1>}` | Boolean | Show/hide reference waveform. | `SELECT:REF2 ON` | 162-163 |

### 3.4 Horizontal and acquisition timing

| CMD | Range / Parameters | Function | Sample | Page |
|---|---|---|---|---:|
| `HORizontal?` |  | Query all horizontal settings. | `HOR?` | 112 |
| `HORizontal:ACQLENGTH?` | Record points | Query acquisition record length. | `HOR:ACQLENGTH?` | 112-113 |
| `HORizontal:DIVisions?` | Typically 15 | Query horizontal divisions. | `HOR:DIV?` | 113 |
| `HORizontal[:MAIn][:DELay]:POSition <NR1>` | Percent of record | Set/query horizontal position. | `HOR:POSITION 50` | 113 |
| `HORizontal:MAIn:DELay:MODe {OFF|ON|<NR1>}` | Boolean | Set/query horizontal delay mode. | `HOR:DELAY:MODE OFF` | 114 |
| `HORizontal:MAIn:DELay:STATe {OFF|ON|<NR1>}` | Boolean | Alias of delay mode. | `HOR:DELAY:STATE ON` | 114-115 |
| `HORizontal[:MAIn]:DELay:TIMe <NR3>` | Seconds | Set/query delay time. | `HOR:DELAY:TIME 0.3` | 115 |
| `HORizontal[:MAIn]:SAMPLERate?` | Samples/s | Query sample rate. | `HOR:SAMPLERATE?` | 115-116 |
| `HORizontal[:MAIn]:SCAle <NR3>` | 1 or 2 ns/div to 100 s/div, model-dependent | Set/query horizontal time/div. | `HOR:MAIN:SCALE 2E-6` | 116 |
| `HORizontal[:MAIn]:SECdiv <NR3>` | Same as SCAle | Set/query seconds/div. | `HOR:MAIN:SECDIV 2E-6` | 116-117 |
| `HORizontal:MAIn:UNIts[:STRing]?` | Returns seconds | Query horizontal unit. | `HOR:MAIN:UNITS?` | 117 |
| `HORizontal:PREViewstate?` | 0/1 | Query acquisition preview state. | `HOR:PREVIEWSTATE?` | 117 |
| `HORizontal:RECOrdlength <NR1>` | 1000, 2000, 20000, 200000, 2000000, 5000000 | Set/query record length. | `HOR:RECORDLENGTH 200000` | 118 |
| `HORizontal:RECOrdlength:Auto <NR1>` | 0 OFF; 1 ON | Set/query automatic record-length mode. | `HOR:RECORDLENGTH:AUTO 1` | 118 |
| `HORizontal:RESOlution <NR1>` | Supported record lengths | Set/query record length while maintaining time/div. | `HOR:RESOLUTION 200000` | 118-119 |
| `HORizontal:ROLL?` | ON/OFF | Query roll-mode state. | `HOR:ROLL?` | 119 |
| `HORizontal:TRIGger:POSition <NR3>` | Percent of record | Set/query trigger position. | `HOR:TRIG:POSITION 50` | 119 |

### 3.5 Trigger

| CMD | Range / Parameters | Function | Sample | Page |
|---|---|---|---|---:|
| `TRIGger FORCe` |  | Force a trigger if trigger state is READY. | `TRIGGER FORCE` | 167 |
| `TRIGger:A SETLevel` | 50% of signal min/max | Set trigger level to 50%. | `TRIGGER:A SETLEVEL` | 167 |
| `TRIGger:A?` |  | Query all A-trigger parameters. | `TRIGGER:A?` | 167-168 |
| `TRIGger:A:EDGE?` |  | Query edge source, coupling, and slope. | `TRIG:A:EDGE?` | 168 |
| `TRIGger:A:EDGE:COUPling {DC|HFRej|LFRej|NOISErej}` | Required selection | Set/query edge-trigger coupling. | `TRIG:A:EDGE:COUP DC` | 168-169 |
| `TRIGger:A:EDGE:SLOpe {RISe|FALL}` | Required slope | Set/query edge-trigger slope. | `TRIG:A:EDGE:SLOPE RISE` | 169 |
| `TRIGger:A:EDGE:SOUrce {CH1|CH2|LINE|AUX}` | Model-dependent channels | Set/query edge-trigger source. | `TRIG:A:EDGE:SOURCE CH1` | 169-170 |
| `TRIGger:A:HOLDOff?` |  | Query holdoff parameters. | `TRIG:A:HOLDOFF?` | 170 |
| `TRIGger:A:HOLDOff:TIMe <NR3>` | 20 ns to 8.0 s | Set/query trigger holdoff. | `TRIG:A:HOLDOFF:TIME 1.2E-6` | 170-171 |
| `TRIGger:A:LEVel {ECL|TTL|<NR3>}` | ECL -1.3 V; TTL 1.4 V; or volts | Set/query trigger level. | `TRIG:A:LEVEL TTL` | 171 |
| `TRIGger:A:LEVel:CH<x> {<NR3>|TTL|ECL}` | Per-channel level | Set/query trigger level for a channel. | `TRIG:A:LEVEL:CH2 1.3` | 171-172 |
| `TRIGger:A:LOWerthreshold:CH<x> {ECL|TTL|<NR3>}` | Per-channel volts | Set/query lower runt threshold. | `TRIG:A:LOWERTHRESHOLD:CH2 50E-3` | 172 |
| `TRIGger:A:MODe {AUTO|NORMal}` | Required mode | Set/query trigger mode. | `TRIG:A:MODE NORMAL` | 173 |
| `TRIGger:A:PULse?` |  | Query pulse-trigger settings. | `TRIG:A:PULSE?` | 173 |
| `TRIGger:A:PULse:CLAss {RUNt|WIDth}` | Required class | Select/query pulse trigger class. | `TRIG:A:PULSE:CLASS WIDTH` | 174 |
| `TRIGger:A:PULSE:Width?` |  | Query pulse-width settings. | `TRIG:A:PULSEWIDTH?` | 174 |
| `TRIGger:A:PULse:WIDth:POLarity {NEGative|POSitive}` | Required polarity | Set/query pulse polarity. | `TRIG:A:PULSEWIDTH:POLARITY NEGATIVE` | 175 |
| `TRIGger:A:PULSEWidth:SOUrce {CH1|CH2|LINE}` | Model-dependent channels | Set/query pulse-width source. | `TRIG:A:PULSEWIDTH:SOURCE CH1` | 175 |
| `TRIGger:A:PULse:WIDth:WHEN {LESSthan|MOREthan|EQual|UNEQual}` | Equal/unequal tolerance +/-5% | Set/query pulse-width condition. | `TRIG:A:PULSEWIDTH:WHEN LESSTHAN` | 176 |
| `TRIGger:A:PULse:WIDth:WIDth <NR3>` | Seconds | Set/query pulse-width threshold. | `TRIG:A:PULSEWIDTH:WIDTH 5E-6` | 176-177 |
| `TRIGger:A:RUNT?` |  | Query runt-trigger parameters. | `TRIG:A:RUNT?` | 177 |
| `TRIGger:A:RUNT:POLarity {NEGative|POSitive}` | Required polarity | Set/query runt polarity. | `TRIG:A:RUNT:POLARITY NEGATIVE` | 177-178 |
| `TRIGger:A:RUNT:SOUrce {CH1|CH2}` | Channel source | Set/query runt source. | `TRIG:A:RUNT:SOURCE CH2` | 178 |
| `TRIGger:A:RUNT:WHEn {LESSthan|MOREthan|EQual|UNEQual|OCCURS}` | Equal/unequal tolerance +/-5% | Set/query runt-width condition. | `TRIG:A:RUNT:WHEN OCCURS` | 178-179 |
| `TRIGger:A:RUNT:WIDth <NR3>` | Seconds | Set/query minimum runt width. | `TRIG:A:RUNT:WIDTH 15E-6` | 179 |
| `TRIGger:A:TYPe {EDGe|PULSe}` | Required type | Set/query trigger type. | `TRIG:A:TYPE EDGE` | 179-180 |
| `TRIGger:A:UPPerthreshold:CH<x> {<NR3>|ECL|TTL}` | Per-channel volts | Set/query upper runt threshold. | `TRIG:A:UPPERTHRESHOLD:CH2 50E-3` | 180 |
| `TRIGger:FREQuency?` | Hz | Query edge/pulse trigger frequency. | `TRIG:FREQUENCY?` | 181 |
| `TRIGger:STATE?` | `ARMED|AUTO|READY|SAVE|TRIGGER` | Query trigger-system state. | `TRIG:STATE?` | 181 |

### 3.6 Measurement

| CMD | Range / Parameters | Function | Sample | Page |
|---|---|---|---|---:|
| `MEASUrement?` |  | Query all measurement settings. | `MEASUREMENT?` | 128 |
| `MEASUrement:CLEARSNapshot` |  | Clear snapshot results and close snapshot window. | `MEAS:CLEARSNAPSHOT` | 129 |
| `MEASUrement:ENABLE {ON|OFF}` | Boolean | Enable/query measurement feature. | `MEAS:ENABLE ON` | 129 |
| `MEASUrement:GATing {OFF|SCREen|CURSor}` | Required gating mode | Set/query measurement gate. | `MEAS:GATING CURSOR` | 130 |
| `MEASUrement:IMMed?` |  | Query immediate-measurement setup. | `MEAS:IMMED?` | 130 |
| `MEASUrement:IMMed:DELay?` |  | Query immediate delay parameters. | `MEAS:IMMED:DELAY?` | 131 |
| `MEASUrement:IMMed:DELay:EDGE<x> {FALL|RISe}` | x=1 from, x=2 to | Set/query edge used for delay measurement. | `MEAS:IMMED:DELAY:EDGE1 RISE` | 131 |
| `MEASUrement:IMMed:SOUrce1 {CH<x>|MATH}` | Primary source | Set/query immediate measurement source 1. | `MEAS:IMMED:SOURCE1 CH1` | 131-132 |
| `MEASUrement:IMMed:SOUrce2 {CH<x>|MATH}` | Secondary source | Set/query source 2 for phase/delay. | `MEAS:IMMED:SOURCE2 CH2` | 132 |
| `MEASUrement:IMMed:TYPe {<type>}` | See measurement types below | Set/query immediate measurement type. | `MEAS:IMMED:TYPE FREQUENCY` | 133-134 |
| `MEASUrement:IMMed:UNIts?` | Unit string | Query immediate-measurement units. | `MEAS:IMMED:UNITS?` | 134-135 |
| `MEASUrement:IMMed:VALue?` | Returns `<NR3>` | Execute and return immediate measurement. | `MEAS:IMMED:VALUE?` | 135 |
| `MEASUrement:MEAS<x>?` | x=1-6 | Query all settings for displayed measurement slot. | `MEAS:MEAS3?` | 135-136 |
| `MEASUrement:MEAS<x>:DELay?` | x=1-6 | Query delay parameters for slot. | `MEAS:MEAS1:DELAY?` | 136 |
| `MEASUrement:MEAS<x>:DELay:EDGE<x> {FALL|RISe}` | From/to edge | Set/query displayed delay edge. | `MEAS:MEAS1:DELAY:EDGE1 RISE` | 136-137 |
| `MEASUrement:MEAS<x>:SOUrce1 {CH<x>|MATH}` | Primary source | Set/query measurement source 1. | `MEAS:MEAS2:SOURCE1 CH1` | 137 |
| `MEASUrement:MEAS<x>:SOUrce2 {CH<x>|MATH}` | Secondary source | Set/query source 2 for delay/phase. | `MEAS:MEAS1:SOURCE2 CH2` | 137-138 |
| `MEASUrement:MEAS<x>:STATE {OFF|ON|<NR1>}` | 0 OFF; nonzero ON | Enable/query displayed measurement slot. | `MEAS:MEAS2:STATE ON` | 138 |
| `MEASUrement:MEAS<x>:TYPe {<type>}` | See measurement types below | Set/query displayed measurement type. | `MEAS:MEAS2:TYPE FREQUENCY` | 139-141 |
| `MEASUrement:MEAS<x>:UNIts?` | Unit string | Query measurement units. | `MEAS:MEAS3:UNITS?` | 141 |
| `MEASUrement:MEAS<x>:VALue?` | Returns `<NR3>` | Query displayed measurement value. | `MEAS:MEAS3:VALUE?` | 141-142 |
| `MEASUrement:REFLevel?` |  | Query all measurement reference levels. | `MEAS:REFLEVEL?` | 142 |
| `MEASUrement:REFLevel:ABSolute:LOW <NR3>` | Volts; default 0 V | Set/query absolute low reference. | `MEAS:REF:ABS:LOW 0.2` | 142-143 |
| `MEASUrement:REFLevel:ABSolute:MID[1] <NR3>` | Volts; default 0 V | Set/query absolute mid reference for source 1. | `MEAS:REF:ABS:MID1 0.71` | 143 |
| `MEASUrement:REFLevel:ABSolute:MID2 <NR3>` | Volts; default 0 V | Set/query absolute mid reference for source 2. | `MEAS:REF:ABS:MID2 0.5` | 143-144 |
| `MEASUrement:REFLevel:METHod {ABSolute|PERCent}` | Required method | Select/query reference-level method. | `MEAS:REF:METHOD PERCENT` | 144 |
| `MEASUrement:REFLevel:PERCent:HIGH <NR3>` | 0-100%; default 90% | Set/query high reference percent. | `MEAS:REF:PERCENT:HIGH 95` | 145 |
| `MEASUrement:REFLevel:PERCent:LOW <NR3>` | 0-100%; default 10% | Set/query low reference percent. | `MEAS:REF:PERCENT:LOW 15` | 145-146 |
| `MEASUrement:REFLevel:PERCent:MID[1] <NR3>` | 0-100%; default 50% | Set/query source-1 mid reference. | `MEAS:REF:PERCENT:MID1 60` | 146 |
| `MEASUrement:REFLevel:PERCent:MID2 <NR3>` | 0-100%; default 50% | Set/query source-2 mid reference. | `MEAS:REF:PERCENT:MID2 40` | 146-147 |
| `MEASUrement:SNAPSHOT` |  | Display measurement snapshot list. | `MEAS:SNAPSHOT` | 147 |
| `MEASUrement:SOURCESNAPShot {CH1|CH2|CH3|CH4|MATH}` | Model-dependent channels | Set/query snapshot source. | `MEAS:SOURCESNAPSHOT CH1` | 147-148 |

#### Supported measurement type arguments

`AMPlitude`, `AREa`, `BURst`, `CARea`, `CMEan`, `CRMs`, `DELay`, `FALL`, `FREQuency`, `HIGH`, `LOW`, `MAXimum`, `MEAN`, `MINImum`, `NDUty`, `NEDGECount`, `NOVershoot`, `NPULSECount`, `NWIdth`, `PEDGECount`, `PDUty`, `PERIod`, `PHAse`, `PK2Pk`, `POVershoot`, `PPULSECount`, `PWIdth`, `RISe`, and `RMS`. See pages 133-140 for the manual definitions and formulas.


### 3.7 Cursor, display, FFT, math, and zoom

| CMD | Range / Parameters | Function | Sample | Page |
|---|---|---|---|---:|
| `CURSor?` |  | Query all cursor settings. | `CURSOR?` | 66 |
| `CURSor:ENABLE {ON|OFF}` | Boolean | Enable/query cursor feature. | `CURSOR:ENABLE ON` | 66 |
| `CURSor:FUNCtion {OFF|SCREEN|TIME|AMPLitude}` | Required type | Set/query cursor type. | `CURSOR:FUNCTION TIME` | 67 |
| `CURSor:HBArs?` |  | Query horizontal-bar settings. | `CURSOR:HBARS?` | 67 |
| `CURSor:HBArs:DELTa?` | Vertical units | Query H-bar difference. | `CURSOR:HBARS:DELTA?` | 68 |
| `CURSor:HBArs:POSITION<x> <NR3>` | x=1 or 2 | Set/query H-bar position. | `CURSOR:HBARS:POSITION1 25E-3` | 68-69 |
| `CURSor:HBArs:UNIts {BASe|PERcent}` | Required unit mode | Set/query H-bar units. | `CURSOR:HBARS:UNITS BASE` | 69 |
| `CURSor:HBArs:USE {CURrent|HALFgrat|FIVEdivs}` | Required scale | Set ratio-cursor scale. | `CURSOR:HBARS:USE FIVEDIVS` | 69-70 |
| `CURSor:MODe {TRACk|INDependent}` | Required mode | Set/query cursor linkage. | `CURSOR:MODE TRACK` | 70 |
| `CURSor:VBArs?` |  | Query V-bar positions and units. | `CURSOR:VBARS?` | 70 |
| `CURSor:VBArs:ALTERNATE<x>?` | x=1 or 2 | Query alternate bus-waveform cursor readout. | `CURSOR:VBARS:ALTERNATE1?` | 71 |
| `CURSor:VBArs:DELTa?` | Seconds or hertz | Query V-bar horizontal difference. | `CURSOR:VBARS:DELTA?` | 71 |
| `CURSor:VBArs:HPOS<x>?` | x=1 or 2 | Query horizontal value of cursor tick. | `CURSOR:VBARS:HPOS1?` | 72 |
| `CURSor:VBArs:POSITION<x> <NR3>` | x=1 or 2 | Set/query V-bar position. | `CURSOR:VBARS:POSITION2 9E-6` | 72-73 |
| `CURSor:VBArs:UNIts {SECOnds|HERtz}` | Required unit | Set/query V-bar units. | `CURSOR:VBARS:UNITS SECONDS` | 73 |
| `CURSor:VBArs:VDELTa?` | Vertical units | Query vertical amplitude difference at V-bars. | `CURSOR:VBARS:VDELTA?` | 73-74 |
| `DISplay:GRAticule {<NR1>|ON|OFF}` | Boolean | Set/query graticule state. | `DISPLAY:GRATICULE ON` | 85 |
| `DISplay:INTENSITy:BACKLight <NR1>` | 1-100 | Set/query backlight intensity. | `DISPLAY:INTENSITY:BACKLIGHT 60` | 85-86 |
| `DISplay:PERSistence:STATe {ON|OFF|<NR1>}` | Boolean | Set/query persistence. | `DISPLAY:PERSISTENCE:STATE ON` | 86 |
| `DISplay:PERSistence:VALUe {<NR3>|AUTO|INFInite}` | Seconds/auto/infinite | Set/query persistence duration. | `DISPLAY:PERSISTENCE:VALUE 3` | 86-87 |
| `FFT?` |  | Query all FFT parameters. | `FFT?` | 93 |
| `FFT:HORizontal:POSition <NR3>` | Frequency position | Set/query FFT horizontal position. | `FFT:HORIZONTAL:POSITION 750E3` | 93-94 |
| `FFT:HORizontal:SCAle <NR3>` | Frequency scale | Set/query FFT horizontal scale. | `FFT:HORIZONTAL:SCALE 500E6` | 94 |
| `FFT:SOURce {CH1|CH2}` | Required source | Set/query FFT source. | `FFT:SOURCE CH2` | 94-95 |
| `FFT:SRCWFM {ON|OFF|<NR1>}` | Boolean | Show/hide FFT source waveform. | `FFT:SRCWFM OFF` | 95 |
| `FFT:VERTical:POSition <NR2>` | Divisions | Set/query FFT vertical position. | `FFT:VERTICAL:POSITION 2` | 95-96 |
| `FFT:VERTical:SCAle <NR2>` | Zoom factor | Set/query FFT vertical scale. | `FFT:VERTICAL:SCALE 20` | 96 |
| `FFT:VERTical:UNIts?` | Unit string | Query FFT vertical units. | `FFT:VERTICAL:UNITS?` | 96 |
| `FFT:VType {DB|LINEAr}` | Required unit type | Set/query FFT vertical representation. | `FFT:VTYPE DB` | 96-97 |
| `FFT:WINdow {HAMming|HANning|RECTangular|BLAckmanharris}` | Required window | Set/query FFT window. | `FFT:WINDOW HAMMING` | 97 |
| `MATH?` |  | Query math definition and display parameters. | `MATH?` | 124 |
| `MATH:DEFINE <QString>` | `CH1+CH2`, `CH1-CH2`, `CH2-CH1`, `CH1*CH2` | Set/query math expression. | `MATH:DEFINE "CH1-CH2"` | 124-125 |
| `MATH:HORizontal:POSition <NR2>` | Percent of record | Set/query math horizontal position. | `MATH:HORIZONTAL:POSITION 20` | 125 |
| `MATH:HORizontal:SCALe <NR3>` | Time/div | Set/query math horizontal scale. | `MATH:HORIZONTAL:SCALE 20E-6` | 125-126 |
| `MATH:HORizontal:UNIts?` | String | Query math horizontal units. | `MATH:HORIZONTAL:UNITS?` | 126 |
| `MATH:LABel <QString>` | Quoted label | Set/query math label. | `MATH:LABEL "Output"` | 126 |
| `MATH:VERtical:POSition <NR3>` | Divisions | Set/query math vertical position. | `MATH:VERTICAL:POSITION 4` | 127 |
| `MATH:VERtical:SCAle <NR3>` | Units/div | Set/query math vertical scale. | `MATH:VERTICAL:SCALE 5` | 127 |
| `MATH:VERTical:UNIts?` | String | Query math vertical units. | `MATH:VERTICAL:UNITS?` | 128 |
| `ZOOM?` |  | Query zoom settings. | `ZOOM?` | 199 |
| `ZOOm{:MODe|:STATE} {ON|OFF|<NR1>}` | Boolean | Enable/query zoom mode. | `ZOOM:MODE ON` | 199 |
| `ZOOm:ZOOM1?` |  | Query Zoom1 settings. | `ZOOM:ZOOM1?` | 200 |
| `ZOOM:ZOOM1:FACtor?` | Zoom factor | Query zoom factor. | `ZOOM:ZOOM1:FACTOR?` | 200 |
| `ZOOM:ZOOM1:HORizontal:POSition <NR1>` | 1-100% | Set/query zoom-box horizontal position. | `ZOOM:ZOOM1:HORIZONTAL:POSITION 50` | 200-201 |
| `ZOOM:ZOOM1:HORizontal:SCAle <NR3>` | 1E-9 to 100 | Set/query zoom horizontal scale. | `ZOOM:ZOOM1:HORIZONTAL:SCALE 5` | 201 |
| `ZOOm:ZOOM1:POSition <NR3>` | 0-100% | Set/query zoom position. | `ZOOM:ZOOM1:POSITION 20` | 201-202 |
| `ZOOm:ZOOM1:SCAle <NR3>` | 1E-9 to 100 | Set/query Zoom1 scale. | `ZOOM:ZOOM1:SCALE 5` | 202 |
| `ZOOM:ZOOM1:STATE {ON|OFF|<NR1>}` | Boolean | Enable/query Zoom1. | `ZOOM:ZOOM1:STATE ON` | 202-203 |

### 3.8 Waveform transfer and preamble

| CMD | Range / Parameters | Function | Sample | Page |
|---|---|---|---|---:|
| `CURVe {<Block>|<asc curve>}` / `CURVe?` | Binary block or comma-separated `<NR1>` values | Transfer waveform data to/from instrument. | `CURVE?` | 74-75 |
| `DATa {INIT|SNAp}` | Initialize or cursor-based selection | Set/query waveform transfer settings. | `DATA INIT` | 76 |
| `DATa:DESTination REF<x>` | Reference memory | Set/query incoming waveform destination. | `DATA:DESTINATION REF1` | 76-77 |
| `DATa:SOUrce {CH1|CH2|CH3|CH4|MATH|REF1|REF2}` | Model-dependent channels | Set/query outgoing waveform source. | `DATA:SOURCE CH1` | 77 |
| `DATa:STARt <NR1>` | 1 to record length | Set/query first transferred point. | `DATA:START 1` | 77-78 |
| `DATa:STOP <NR1>` | 1 to record length | Set/query last transferred point. | `DATA:STOP 2000` | 78-79 |
| `DATa:WIDth <NR1>` | 1 or 2 bytes/point | Set/query transfer width. | `DATA:WIDTH 1` | 79 |
| `WAVFrm?` |  | Return synchronized output preamble and curve data. | `WAVFRM?` | 184 |
| `WFMInpre?` |  | Query incoming waveform formatting/scaling preamble. | `WFMINPRE?` | 185 |
| `WFMInpre:BIT_Nr <NR1>` | 8 or 16 bits | Set/query incoming bits per point. | `WFMINPRE:BIT_NR 16` | 185 |
| `WFMInpre:BYT_Nr <NR1>` | 1 or 2 bytes | Set/query incoming bytes per point. | `WFMINPRE:BYT_NR 1` | 186 |
| `WFMInpre:ENCdg {ASCii|BINary}` | Required encoding | Set/query incoming encoding. | `WFMINPRE:ENCDG ASCII` | 186 |
| `WFMInpre:NR_Pt <NR1>` | Point count | Set/query incoming point count. | `WFMINPRE:NR_PT 10000` | 187 |
| `WFMInpre:XINcr <NR3>` | X units/point | Set/query incoming sample interval. | `WFMINPRE:XINCR 3E-3` | 187 |
| `WFMInpre:XUNit <QString>` | Up to 3 alpha characters | Set/query incoming horizontal units. | `WFMINPRE:XUNIT "s"` | 188 |
| `WFMInpre:XZEro <NR3>` | Horizontal units | Set/query first-sample X coordinate. | `WFMINPRE:XZERO 5.7E-6` | 188-189 |
| `WFMInpre:YMUlt <NR3>` | Y units/digitizing level | Set/query incoming vertical scale factor. | `WFMINPRE:YMULT 40E-3` | 189 |
| `WFMInpre:YOFf <NR3>` | Digitizing levels | Set/query incoming vertical position. | `WFMINPRE:YOFF 50` | 189-190 |
| `WFMInpre:YUNit <QString>` | Vertical unit string | Set/query incoming vertical units. | `WFMINPRE:YUNIT "V"` | 190 |
| `WFMInpre:YZEro <NR3>` | Y units | Set/query incoming vertical offset. | `WFMINPRE:YZERO 1.5` | 191 |
| `WFMOutpre?` |  | Query outgoing waveform transfer/scaling preamble. | `WFMOUTPRE?` | 191 |
| `WFMOutpre:BIT_Nr <NR1>` | 8 or 16 bits | Set/query outgoing bits per point. | `WFMOUTPRE:BIT_NR 16` | 192 |
| `WFMOutpre:BN_Fmt {RI|RP}` | Signed or positive integer | Set/query outgoing binary numeric format. | `WFMOUTPRE:BN_FMT RP` | 192-193 |
| `WFMOutpre:BYT_Nr <NR1>` | 1 or 2 bytes | Set/query outgoing bytes per point. | `WFMOUTPRE:BYT_NR 1` | 193 |
| `WFMOutpre:ENCdg {ASCii|BINary}` | Required encoding | Set/query outgoing encoding. | `WFMOUTPRE:ENCDG ASCII` | 193-194 |
| `WFMOutpre:NR_Pt?` | Point count | Query transmitted point count. | `WFMOUTPRE:NR_PT?` | 194 |
| `WFMOutpre:RECOrdlength?` | Point count | Query source record length. | `WFMOUTPRE:RECORDLENGTH?` | 194 |
| `WFMOutpre:WFId?` | Description string | Query waveform identification summary. | `WFMOUTPRE:WFID?` | 195 |
| `WFMOutpre:XINcr?` | X units/point | Query sample interval. | `WFMOUTPRE:XINCR?` | 195-196 |
| `WFMOutpre:XUNit?` | String | Query horizontal units. | `WFMOUTPRE:XUNIT?` | 196 |
| `WFMOutpre:XZEro?` | X units | Query first-point time coordinate. | `WFMOUTPRE:XZERO?` | 196 |
| `WFMOutpre:YMUlt?` | Y units/digitizing level | Query vertical scale factor. | `WFMOUTPRE:YMULT?` | 197 |
| `WFMOutpre:YOFf?` | Digitizing levels | Query vertical position. | `WFMOUTPRE:YOFF?` | 197 |
| `WFMOutpre:YUNit?` | String | Query vertical units. | `WFMOUTPRE:YUNIT?` | 198 |
| `WFMOutpre:YZEro?` | Y units | Query vertical offset. | `WFMOUTPRE:YZERO?` | 198 |

### 3.9 File system, save, and recall

| CMD | Range / Parameters | Function | Sample | Page |
|---|---|---|---|---:|
| `FILESystem?` |  | Query current directory list and free space. | `FILESYSTEM?` | 97-98 |
| `FILESystem:CWD <QString>` | 8.3-style path names | Set/query current working directory. | `FILESYSTEM:CWD "USB0/TEKSCOPE/IMAGES"` | 98 |
| `FILESystem:DELEte <file path>` | Quoted path; `*.*` deletes all | Delete file or directory contents. | `FILESYSTEM:DELETE "NOT_MINE.SET"` | 98-99 |
| `FILESystem:DIR?` |  | List current directory entries. | `FILESYSTEM:DIR?` | 99 |
| `FILESystem:FORMat <drive>` | Quoted drive; destructive | Format a mass-storage device. | `FILESYSTEM:FORMAT "USB0/"` | 99-100 |
| `FILESystem:FREESpace?` | Bytes | Query free space on current drive. | `FILESYSTEM:FREESPACE?` | 100 |
| `FILESystem:MKDir <directory path>` | Quoted path | Create directory. | `FILESYSTEM:MKDIR "USB0/NEWDIR"` | 100-101 |
| `FILESystem:READFile <QString>` | Quoted path | Send file contents to current interface. | `FILESYSTEM:READFILE "USB0/TEST_DATA/FILE.CSV"` | 101 |
| `FILESystem:REName <old>,<new>` | Two quoted paths | Rename or move file/folder. | `FILESYSTEM:RENAME "USB0/OLD.SET","USB0/NEW.SET"` | 101-102 |
| `FILESystem:RMDir <directory path>` | Quoted path | Delete directory and contents as documented. | `FILESYSTEM:RMDIR "USB0/OLDDIR"` | 102 |
| `FILESystem:WRITEFile <file path>,<data>` | Block <=262144 bytes | Write block data to file. | `FILESYSTEM:WRITEFILE "TEST.BIN",#...` | 103 |
| `FACtory` |  | Reset factory defaults without clearing specified protected/communication data. | `FACTORY` | 92 |
| `*RCL <NR1>` | 1-10 | Recall setup from nonvolatile memory. | `*RCL 3` | 151 |
| `RECAll:SETUp {FACtory|<NR1>|<file path>}` | 1-10 or quoted .SET path | Recall factory, internal, or USB setup. | `RECALL:SETUP "TEK00000.SET"` | 151-152 |
| `RECAll:WAVEForm <file path>,REF<x>` | REF1 or REF2 | Recall waveform file into reference memory. | `RECALL:WAVEFORM "TEK00000.ISF",REF1` | 152 |
| `*SAV <NR1>` | 1-10 | Save setup to nonvolatile memory. | `*SAV 2` | 156 |
| `SAVe:ASSIgn:TYPe {IMAGe|WAVEform|SETUp|PRINTer}` | Required type | Assign front-panel Save action. | `SAVE:ASSIGN:TYPE WAVEFORM` | 156-157 |
| `SAVe:IMAge <file path>` | Quoted filename/path | Save screen image. | `SAVE:IMAGE "USB0/PROD-TST/VID-EVAL.BMP"` | 157 |
| `SAVe:IMAge:FILEFormat {PNG|BMP|JPG}` | Required format | Set/query screen-image format. | `SAVE:IMAGE:FILEFORMAT PNG` | 157-158 |
| `SAVe:IMAGe:LAYout {LANdscape|PORTRait}` | Required layout | Set/query image layout. | `SAVE:IMAGE:LAYOUT LANDSCAPE` | 158 |
| `SAVe:SETUp {<file path>|<NR1>}` | 1-10 or quoted path | Save setup to memory or USB. | `SAVE:SETUP 5` | 158-159 |
| `SAVe:WAVEform <wfm>,{REF<x>|<QString>}` | Waveform and destination | Save waveform to reference memory or file. | `SAVE:WAVEFORM CH1,REF1` | 159 |
| `SAVe:WAVEform:FILEFormat {INTERNal|SPREADSheet}` | ISF or CSV | Set/query waveform file format. | `SAVE:WAVEFORM:FILEFORMAT SPREADSHEET` | 160 |
| `SETUP<x>:DATE?` | Saved setup number | Query saved-setup date. | `SETUP4:DATE?` | 163-164 |
| `SETUP<x>:TIME?` | Saved setup number | Query saved-setup time. | `SETUP2:TIME?` | 164 |

### 3.10 Miscellaneous and instrument control

| CMD | Range / Parameters | Function | Sample | Page |
|---|---|---|---|---:|
| `AUTOSet {EXECute|UNDo}` | Required action | Run Autoset or restore pre-Autoset settings. | `AUTOSET EXECUTE` | 49 |
| `AUTOSet:ENABLE {ON|OFF}` | Boolean | Enable/query Autoset feature. | `AUTOSET:ENABLE ON` | 49-50 |
| `CLEARMenu` |  | Clear current display menu. | `CLEARMENU` | 65 |
| `DATE <QString>` | `"yyyy-mm-dd"` | Set/query instrument date. | `DATE "2010-05-06"` | 79-80 |
| `FEAEN:PASSWORD <password>` | Quoted password | Authorize Feature Enable settings. | `FEAEN:PASSWORD "111111"` | 92-93 |
| `FPAnel:PRESS <button>` | Documented button enumeration | Simulate front-panel button press. | `FPANEL:PRESS AUTOSET` | 103-104 |
| `FPAnel:TURN <knob>[,<n>]` | Signed rotation count; default +1 | Simulate turning a front-panel knob. | `FPANEL:TURN TRIGLEVEL,10` | 105 |
| `FWUpdate:Update` | Requires `TBS2000B.TEK` in USB root | Update firmware from USB. | `FWUPDATE:UPDATE` | 105-106 |
| `HDR` / `HEADer {ON|OFF|<NR1>}` | Boolean | Set/query response-header inclusion. | `HEADER OFF` | 107 |
| `ID?` | Identification string | Query Tektronix-format identity; must be last concatenated query. | `ID?` | 120 |
| `*IDN?` | IEEE 488.2 identification | Query manufacturer/model/serial/firmware. | `*IDN?` | 120-121 |
| `LANGuage <language>` | Supported display language | Set/query UI language. | `LANGUAGE FRENCH` | 122 |
| `LOCk {ALL|NONe}` | Required state | Lock/query front panel controls. | `LOCK ALL` | 122-123 |
| `UNLock ALL` |  | Unlock front-panel controls. | `UNLOCK ALL` | 182 |
| `*LRN?` / `SET?` |  | Return most instrument settings in reusable command form. | `SET?` | 123, 163 |
| `MEASUrement:ENABLE {ON|OFF}` | Boolean | Enable/query measurement feature. | `MEAS:ENABLE ON` | 129 |
| `*RST` |  | Reset instrument settings without purging stored settings/waveforms. | `*RST` | 155 |
| `TEKSecure` | 3-5 minutes | Erase user settings/confidential data; instrument unavailable while running. | `TEKSECURE` | 166 |
| `TIMe <QString>` | `"hh:mm:ss"` | Set/query instrument time. | `TIME "14:00:00"` | 166 |
| `VERBose {ON|OFF|<NR1>}` | Boolean | Set/query full or abbreviated returned keywords. | `VERBOSE ON` | 183 |
## 4. Practical ATE workflows

### 4.1 Identify and reset

```text
*IDN?
*CLS
*RST
```

Read the `*IDN?` response before sending the next terminated query. `*CLS` clears status structures, while `*RST` returns the oscilloscope to a known settings state without deleting saved setups or waveforms. See pages 65, 120-121, and 155.

### 4.2 Single-sequence acquisition with synchronization

```text
ACQUIRE:STATE OFF
SELECT:CH1 ON
ACQUIRE:MODE SAMPLE
ACQUIRE:STOPAFTER SEQUENCE
ACQUIRE:STATE ON
*OPC?
```

Wait for the `*OPC?` response `1` before reading measurements or waveform data. This is the simplest documented synchronization method, but the controller timeout must exceed the longest expected acquisition time. See pages 208-213.

### 4.3 Immediate automated measurement

```text
MEASUREMENT:IMMED:SOURCE1 CH1
MEASUREMENT:IMMED:TYPE FREQUENCY
MEASUREMENT:IMMED:VALUE?
*ESR?
ALLEV?
```

The manual recommends `MEASUrement:IMMed` commands for computer-controlled measurements because they do not consume a displayed measurement slot. A value of `9.9E37` indicates an invalid measurement condition; inspect the event system for the specific reason. See pages 130-135 and 222-223.

### 4.4 Waveform transfer

```text
DATA:SOURCE CH1
DATA:START 1
DATA:STOP 2000
WFMOUTPRE:ENCDG ASCII
WFMOUTPRE?
CURVE?
```

For binary transfers, set the outgoing encoding, byte width, and binary numeric format before `CURVE?`. The source waveform must be active. Convert digitizing levels to engineering units with:

`value = ((curve_value - YOFF) * YMULT) + YZERO`

The X coordinate for point index `i` is based on `XZERO` and `XINCR`. See pages 36-39, 74-79, and 191-198.

## 5. Important implementation cautions

1. **Read every query response immediately.** Sending another terminated command before reading the current response can clear the output queue and set a query error. See page 207.
2. **Synchronize long operations.** Use `*OPC?`, `*WAI`, `BUSY?`, or status-register/SRQ handling before measuring or transferring data after a single acquisition. See pages 208-213.
3. **Keep the source waveform active.** `CURVe?` and several `WFMOutpre` queries can return no data or time out when `DATa:SOUrce` is not displayed. See pages 74 and 194-198.
4. **Update `DATa:STOP` after changing record length.** The instrument does not automatically expand `DATa:STOP` when record length increases. See pages 78-79.
5. **Do not assume arbitrary numeric values are preserved.** The oscilloscope can clamp or round numeric arguments to supported values. Query the resulting setting. See page 20.
6. **Use `HEADer OFF` for simpler parsers.** With headers off, responses contain values only. With headers on, responses can often be reused as commands. See page 17.
7. **Protect destructive file operations.** `FILESystem:FORMat`, wildcard deletion, `FACtory`, and `TEKSecure` can remove data or settings. `TEKSecure` takes approximately 3-5 minutes. See pages 92, 99-100, and 166.
8. **Measurement error sentinel.** The manual uses `9.9E37`/`9.9000E+37` for unavailable or invalid results. Always follow questionable readings with status/event queries. See pages 71, 135, and 222-223.

## 6. Manual references

- **Manufacturer:** Tektronix
- **Equipment:** TBS2000B Series Digital Oscilloscopes
- **Document:** *TBS2000B Series Digital Oscilloscopes Programmer Manual*
- **Document number:** 077-1149-04
- **Revision date:** May 2024
- **Length:** 232 pages
- **Command syntax:** pages 15-22
- **Command groups:** pages 23-40
- **Detailed command descriptions:** pages 41-203
- **Status and events:** pages 204-221
- **Programming examples:** pages 222-223
- **Factory setup:** pages 225-226

## 7. Source-quality notes

The supplied manual contains a small number of apparent editorial inconsistencies, including references to commands or interfaces that differ from nearby syntax tables, duplicated descriptions, and examples with minor formatting errors. This reference preserves the documented command forms and does not invent corrections. For an automated driver, validate high-risk commands against the actual instrument using `*IDN?`, setting queries, `*ESR?`, and `ALLEV?`.
