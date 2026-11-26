# UNI-T UT8805E SCPI Command Reference

> **Source of truth:** *UT8805E SCPI Programming Manual*, 49 pages. This reference is extracted only from the supplied manual. Page numbers below are the printed manual page numbers. No undocumented commands have been added.

## 1. Introduction

This document catalogs the SCPI and IEEE-488.2 commands documented for the UNI-T UT8805E digital multimeter. It records command syntax, parameter choices, purpose, representative command examples, and manual page references.

### 1.1 Syntax conventions

| Notation | Meaning | Example |
|---|---|---|
| Uppercase letters | Short/abbreviated keyword form | `VOLT` |
| Mixed uppercase/lowercase | Long keyword form; uppercase characters identify the abbreviation | `VOLTage` |
| Case | SCPI keywords are case-insensitive | `Volt`, `VOLT`, `voltage` |
| `{A\|B}` | Required selection of one listed alternative; braces and `\|` are not transmitted | `{MIN\|MAX\|DEF}` |
| `[ ... ]` | Optional command keyword or parameter; brackets are not transmitted | `[SENSe:]` |
| `<...>` | A value must be supplied in place of the placeholder | `<range>` |
| `?` | Query the current setting or return a measurement | `VOLT:DC:RANG?` |
| `;` | Separates sequential commands in one command message | `*RST;*CLS` |
| `*` | Prefix used by IEEE-488.2 common commands | `*RST` |

**Important:** The manual's own syntax conventions take precedence over generic examples. For example, the manual documents `SAMPle:COUNt`, but does not define a general SCPI command called `CONFigure:CURRent` beyond the specific forms listed in this reference.

### 1.2 Parameter data types

- **Numeric:** Decimal values and scientific notation are supported. Unit prefixes may be accepted where applicable. Some commands accept `MIN`, `MAX`, and/or `DEF` as stated in the syntax.
- **Discrete:** One item from a documented list, such as `{IMMediate|EXTernal|BUS}`. Query responses are generally returned in uppercase abbreviated form.
- **Boolean:** The manual documents forms such as `{ON|1|OFF|0}`. Queries return `0` or `1`.
- **Optional parameters:** If omitted, the instrument uses the documented default.

## 2. Connections

The supplied SCPI Programming Manual does **not** provide a dedicated remote-interface wiring or connector pinout section. It does document these control/connection references:

| Interface / signal | Manual information | Page |
|---|---|---:|
| Remote port | Commands and responses are exchanged through the instrument's remote port; the manual does not specify a complete interface configuration procedure in this document. | 4, 6, 23, 46 |
| `Ext Trig` input | External trigger is applied to the rear-panel `Ext Trig` input. | 49 |
| `VM Comp` BNC output | Voltmeter-complete output signal is available on the rear-panel `VM Comp` BNC connector. | 5-6 |
| Front-panel/local mode | `*UNREMOTE` returns the instrument to local mode and unlocks front-panel keys. | 7 |

**Connection limitation:** USB/GPIB/LAN/RS-232 electrical details, connector pinouts, baud rates, VISA resource strings, and driver setup are not specified in the supplied programming manual. They are intentionally not inferred here.

## 3. SCPI TABLE

The `CMD` column gives the documented syntax. A semicolon is not part of a command's syntax unless shown in an example. Query forms are listed separately where the manual specifies them.

### 3.1 IEEE-488.2 and measurement-control commands

| CMD | Range / Parameters | Function | Sample | Page |
|---|---|---|---|---:|
| `*UNREMOTE` | None | Return to local mode and unlock front-panel keys. | `*UNREMOTE` | 7 |
| `ABORt` | None | Abort an ongoing or pending measurement and return the trigger system to the idle-trigger state. | `ABOR` | 4 |
| `FETCh?` | None | Wait for the latest measurement to complete and transfer available readings from reading memory to the output buffer. Does not erase reading memory. | `FETC?` | 4 |
| `INITiate[:IMMediate]` | None | Put the trigger system into the waiting-to-trigger state; starts measurement when trigger conditions are met. | `INIT` | 5 |
| `READ?` | None | Start measurement and return readings from reading memory; reads and erases returned readings. | `READ?` | 6 |
| `OUTPut:TRIGger:SLOPe {POSitive\|NEGative}` | `POSitive` or `NEGative` | Select polarity of the voltmeter-complete output pulse on the rear-panel `VM Comp` BNC. The manual states `NEGative` as the default. | `OUTP:TRIG:SLOP POS` | 5 |
| `SAMPle:COUNt {<count>\|MIN\|MAX\|DEF}` | 1 to 100,000; default 1 | Set the number of samples collected per trigger. | `SAMP:COUN 10` | 6-7 |
| `SAMPle:COUNt? [ {MIN\|MAX\|DEF} ]` | Optional query selector: `MIN`, `MAX`, `DEF` | Query the sample count or supported limit/default value. | `SAMP:COUN?` | 6 |
| `UNIT:TEMPerature {C\|F\|K}` | `C`, `F`, or `K`; default Celsius | Select temperature result units: Celsius, Fahrenheit, or Kelvin. | `UNIT:TEMP F` | 7 |

The manual also describes IEEE-488.2 common commands as beginning with `*`, followed by a three-character command mnemonic. Its examples include:

| CMD | Function | Sample | Page |
|---|---|---|---:|
| `*RST` | Reset instrument (used in manual examples). | `*RST` | 3, 12 |
| `*CLS` | Clear status (used in manual examples). | `*CLS` | 3, 8 |
| `*ESE <value>` | Set event status enable register (example value 32). | `*ESE 32` | 3 |
| `*OPC?` | Operation-complete query. | `*OPC?` | 3 |
| `*TRG` | Generate a bus trigger when BUS triggering is selected and the instrument is waiting for trigger. | `*TRG` | 5, 49 |

### 3.2 CALCulate subsystem

| CMD | Range / Parameters | Function | Sample | Page |
|---|---|---|---|---:|
| `CALCulate:CLEar[:IMMediate]` | None | Clear limit conditions, histogram data, statistical information, and measurement results. | `CALC:CLE:IMM` | 8-9 |
| `CALCulate:LIMit:CLEar[:IMMediate]` | None | Clear current limit indication and lower/upper limit-failure bits in the questionable data register. Does not clear readings in reading memory. | `CALC:LIM:CLE:IMM` | 8-9 |
| `CALCulate:LIMit:{LOWer\|UPPer}[:DATA] {<value>\|MIN\|MAX\|DEF}` | Numeric limit; documented range approximately `-1.0E15` to `-1.0E-15`, or `0.0` default, or positive range to `1.0E15` | Set lower or upper limit-test threshold. | `CALC:LIM:LOW 2.4` | 9 |
| `CALCulate:LIMit:{LOWer\|UPPer}[:DATA]? [{MIN\|MAX\|DEF}]` | Optional query selector | Query lower or upper limit threshold. | `CALC:LIM:UPP?` | 9 |
| `CALCulate:LIMit[:STATe] {ON\|1\|OFF\|0}` | Boolean; default OFF | Enable or disable limit testing. | `CALC:LIM:STAT ON` | 9-10 |
| `CALCulate:LIMit[:STATe]?` | None | Query limit-test enable state. | `CALC:LIM:STAT?` | 9-10 |
| `CALCulate:TRANsform:HISTogram:ALL?` | None | Return histogram lower/upper ranges, measurement count, and histogram-bin data. | `CALC:TRAN:HIST:ALL?` | 10-11 |
| `CALCulate:TRANsform:HISTogram:DATA?` | None | Return histogram-bin data only. | `CALC:TRAN:HIST:DATA?` | 10-11 |
| `CALCulate:TRANsform:HISTogram:CLEar[:IMMediate]` | None | Clear histogram data; reactivates automatic histogram range selection if enabled. | `CALC:TRAN:HIST:CLE` | 11 |
| `CALCulate:TRANsform:HISTogram:COUNt?` | None | Query number of measurements collected since histogram data was last cleared. | `CALC:TRAN:HIST:COUN?` | 11 |
| `CALCulate:TRANsform:HISTogram:POINts {<value>\|MIN\|MAX\|DEF}` | `{10\|20\|40\|100\|200\|400\|MIN\|MAX\|DEF}`; default 100 | Set number of histogram bins between lower and upper ranges. Two additional out-of-range bins are used. | `CALC:TRAN:HIST:POIN 100` | 11 |
| `CALCulate:TRANsform:HISTogram:POINts?` | None | Query histogram point count. | `CALC:TRAN:HIST:POIN?` | 11 |
| `CALCulate:TRANsform:HISTogram:AUTO:ONCE` | None | Automatically scale histogram once. | `CALC:TRAN:HIST:AUTO:ONCE` | 11 |
| `CALCulate:TRANsform:HISTogram:RANGe:AUTO {ON\|1\|OFF\|0}` | Boolean | Enable or disable automatic histogram range selection. | `CALC:TRAN:HIST:RANG:AUTO ON` | 10-12 |
| `CALCulate:TRANsform:HISTogram:RANGe:AUTO?` | None | Query automatic histogram range selection. | `CALC:TRAN:HIST:RANG:AUTO?` | 10-12 |
| `CALCulate:TRANsform:HISTogram:RANGe:{LOWer\|UPPer} {<value>\|MIN\|MAX\|DEF}` | Numeric; documented range approximately `-1.0E15` to `+1.0E15`; default 0 | Set histogram lower or upper boundary. Setting a boundary disables automatic range selection. | `CALC:TRAN:HIST:RANG:LOW 1` | 11-12 |
| `CALCulate:TRANsform:HISTogram:RANGe:{LOWer\|UPPer}?` | None | Query histogram lower or upper boundary. | `CALC:TRAN:HIST:RANG:LOW?` | 11-12 |
| `CALCulate:TRANsform:HISTogram[:STATe] {ON\|1\|OFF\|0}` | Boolean; default OFF | Enable or disable histogram calculation. | `CALC:TRAN:HIST:STAT ON` | 12 |
| `CALCulate:TRANsform:HISTogram[:STATe]?` | None | Query histogram calculation state. | `CALC:TRAN:HIST:STAT?` | 12 |
| `CALCulate:SCALe:DB:REFerence {<reference>\|MIN\|MAX\|DEF}` | -200.0 dBm to +200.0 dBm; default 0 | Set the relative reference used by dB calculation. ACV/DCV only. | `CALC:SCAL:DB:REF -10.0` | 12-13 |
| `CALCulate:SCALe:DB:REFerence? [{MIN\|MAX}]` | Optional `MIN` or `MAX` query selector | Query dB reference. | `CALC:SCAL:DB:REF?` | 12-13 |
| `CALCulate:SCALe:DBM:REFerence {<reference>\|MIN\|MAX\|DEF}` | `{50,75,93,110,124,125,135,150,250,300,500,600,800,900,1000,1200,8000}` ohms; default 600 ohms | Set reference resistance for dBm calculation. ACV/DCV only. | `CALC:SCAL:DBM:REF 600` | 13 |
| `CALCulate:SCALe:DBM:REFerence? [{MIN\|MAX}]` | Optional `MIN` or `MAX` query selector | Query dBm reference resistance. | `CALC:SCAL:DBM:REF?` | 13 |
| `CALCulate:SCALe:FUNCtion {DB\|DBM}` | `DB` or `DBM` | Select relative dB or dBm calculation. ACV/DCV only. | `CALC:SCAL:FUNC DBM` | 13-14 |
| `CALCulate:SCALe:FUNCtion?` | None | Query selected scaling function. | `CALC:SCAL:FUNC?` | 13-14 |
| `CALCulate:SCALe:REFerence:AUTO {ON\|1\|OFF\|0}` | Boolean | Enable or disable automatic reference selection for dB. ACV/DCV only. | `CALC:SCAL:REF:AUTO ON` | 14 |
| `CALCulate:SCALe:REFerence:AUTO?` | None | Query automatic dB reference selection. | `CALC:SCAL:REF:AUTO?` | 14 |
| `CALCulate:SCALe[:STATe] {ON\|1\|OFF\|0}` | Boolean | Enable or disable scaling/calibration function. ACV/DCV only. | `CALC:SCAL:STAT ON` | 14 |
| `CALCulate:SCALe[:STATe]?` | None | Query scaling/calibration state. | `CALC:SCAL:STAT?` | 14 |
| `CALCulate:AVERage[:STATe] {ON\|1\|OFF\|0}` | Boolean; default OFF | Enable or disable statistical calculations. | `CALC:AVER:STAT ON` | 15 |
| `CALCulate:AVERage[:STATe]?` | None | Query statistical calculation state. | `CALC:AVER:STAT?` | 15 |
| `CALCulate:AVERage:ALL?` | None | Query mean, standard deviation, maximum, and minimum since last statistics clear. | `CALC:AVER:ALL?` | 15-16 |
| `CALCulate:AVERage:AVERage?` | None | Query arithmetic mean. | `CALC:AVER:AVER?` | 15-16 |
| `CALCulate:AVERage:COUNt?` | None | Query number of measurements included in statistics. | `CALC:AVER:COUN?` | 15-16 |
| `CALCulate:AVERage:MAXimum?` | None | Query maximum measurement. | `CALC:AVER:MAX?` | 15-16 |
| `CALCulate:AVERage:MINimum?` | None | Query minimum measurement. | `CALC:AVER:MIN?` | 15-16 |
| `CALCulate:AVERage:PTPeak?` | None | Query peak-to-peak value. | `CALC:AVER:PTP?` | 15-16 |
| `CALCulate:AVERage:SDEViation?` | None | Query standard deviation. | `CALC:AVER:SDEV?` | 15-16 |
| `CALCulate:AVERage:CLEar[:IMMediate]` | None | Clear statistical values, including min, max, average, peak-to-peak, count, and standard deviation. | `CALC:AVER:CLE` | 16 |

### 3.3 CONFigure subsystem

`CONFigure` configures a measurement function and restores associated measurement/trigger attributes to defaults. It does not itself start measurement; use `INITiate` or `READ?` to start. The manual documents these forms:

| CMD | Range / Parameters | Function | Sample | Page |
|---|---|---|---|---:|
| `CONFigure?` | None | Return current measurement function and range in short form. | `CONF?` | 18 |
| `CONFigure:CONTinuity` | None | Configure continuity measurement with default settings. | `CONF:CONT` | 18-19 |
| `CONFigure:CURRent:{AC\|DC} [ {<range>\|AUTO\|MIN\|MAX\|DEF} ]` | AC/DC; range `{200uA\|2mA\|20mA\|200mA\|2A\|10A\|AUTO}`; default AUTO. 200 uA and 2 mA are DC-only; AC minimum is 20 mA. | Configure AC or DC current measurement. | `CONF:CURR:AC 2` | 19 |
| `CONFigure:DIODe` | None | Configure diode measurement; fixed 2 V DC range. | `CONF:DIOD` | 20 |
| `CONFigure:{FREQuency\|PERiod}` | None | Configure frequency or period measurement. | `CONF:FREQ` | 20 |
| `CONFigure:{RESistance\|FRESistance} [ {<range>\|AUTO\|MIN\|MAX\|DEF} ]` | `{200 ohm\|2 kohm\|20 kohm\|200 kohm\|2 Mohm\|10 Mohm\|100 Mohm}`; default AUTO | Configure 2-wire resistance or 4-wire resistance measurement. | `CONF:FRES 200` | 20-21 |
| `CONFigure:TEMPerature [ {FRTD\|RTD\|FTHermistor\|THERmistor\|TCouple} [, {<type>\|DEFault}] ]` | Probe type defaults RTD. RTD type: PT100. Thermocouple type: `{E\|J\|K\|N\|R\|T}`. | Configure temperature measurement. | `CONF:TEMP RTD,PT100` | 21 |
| `CONFigure[:VOLTage]:{AC\|DC} [ {<range>\|AUTO\|MIN\|MAX\|DEF} ]` | `{200 mV\|2 V\|20 V\|200 V\|1000 V DC / 750 V AC}`; default AUTO | Configure AC or DC voltage measurement. | `CONF:VOLT:AC 200` | 21-22 |
| `CONFigure:CAPacitance [ {<range>\|AUTO\|MIN\|MAX\|DEF} ]` | `{2nF\|20nF\|200nF\|2uF\|20uF\|200uF\|10000uF}`; default AUTO | Configure capacitance measurement. | `CONF:CAP 2uF` | 22 |

### 3.4 DATA subsystem

| CMD | Range / Parameters | Function | Sample | Page |
|---|---|---|---|---:|
| `DATA:LAST?` | None | Return latest measured result with unit; returns not-a-number indication if no data is available. | `DATA:LAST?` | 23 |
| `DATA:POINts?` | None | Return total number of readings in reading memory. | `DATA:POIN?` | 23 |
| `DATA:REMove? <num_readings> [,WAIT]` | `<num_readings>`: 1 to 10,000; optional `WAIT` | Read and erase the requested number of oldest readings. With `WAIT`, wait until enough readings are available. | `DATA:REM? 5` | 23-24 |

### 3.5 MEASure subsystem

`MEASure` applies default measurement/trigger attributes, performs the measurement immediately, and returns the result. It is functionally similar to configuring and then issuing `READ?`.

| CMD | Range / Parameters | Function | Sample | Page |
|---|---|---|---|---:|
| `MEASure:CONTinuity?` | None | Perform continuity measurement and return resistance. Range fixed at 1 kohm. | `MEAS:CONT?` | 24-25 |
| `MEASure:CURRent:{AC\|DC}? [ {<range>\|AUTO\|MIN\|MAX\|DEF} ]` | `{200uA\|2mA\|20mA\|200mA\|2A\|10A\|AUTO}`; 200 uA and 2 mA DC-only; AC minimum 20 mA | Perform AC/DC current measurement and return result. | `MEAS:CURR:AC? 2` | 25-26 |
| `MEASure:DIODe?` | None | Perform diode measurement and return voltage; fixed 2 V DC range. | `MEAS:DIOD?` | 26 |
| `MEASure:{FREQuency\|PERiod}?` | None | Perform frequency or period measurement. | `MEAS:FREQ?` | 26 |
| `MEASure:{RESistance\|FRESistance}? [ {<range>\|AUTO\|MIN\|MAX\|DEF} ]` | `{200 ohm\|2 kohm\|20 kohm\|200 kohm\|2 Mohm\|10 Mohm\|100 Mohm}`; default AUTO | Perform 2-wire or 4-wire resistance measurement. | `MEAS:FRES? 200` | 26-27 |
| `MEASure:TEMPerature? [ {RTD\|THER\|DEFault} [ {<type>\|DEFault} ] ]` | Probe type `{RTD\|THER}`, default THER. RTD type PT100; thermistor sensor types as listed in manual: `BITS90`, `EITS90`, `JITS90`, `KITS90`, `NITS90`, `RITS90`, `SITS90`, `TITS90`. | Perform temperature measurement and return result. | `MEAS:TEMP? RTD,PT100` | 27 |
| `MEASure[:VOLTage]:{AC\|DC}? [ {<range>\|AUTO\|MIN\|MAX\|DEF} ]` | `{200mV\|2V\|20V\|200V\|1000V DC / 750V AC}`; default AUTO | Perform AC/DC voltage measurement. | `MEAS:VOLT:AC? 200` | 27-28 |
| `MEASure:CAPacitance? [ {<range>\|AUTO\|MIN\|MAX\|DEF} ]` | `{2nF\|20nF\|200nF\|2uF\|20uF\|200uF\|10000uF}`; default AUTO | Perform capacitance measurement. | `MEAS:CAP? 2uF` | 28 |

### 3.6 SENSe subsystem

#### 3.6.1 Function selection

| CMD | Range / Parameters | Function | Sample | Page |
|---|---|---|---|---:|
| `[SENSe:]FUNCtion[:ON] "<function>"` | `CONTinuity`, `CURRent:AC`, `CURRent[:DC]`, `DIODe`, `FREQuency`, `FRESistance`, `PERiod`, `RESistance`, `TEMPerature`, `VOLTage:AC`, `VOLTage[:DC]`, `CAPacitance`; default DC voltage | Select measurement function while retaining function attributes. | `FUNC "VOLT:DC"` | 28-29 |
| `[SENSe:]FUNCtion[:ON]?` | None | Query selected measurement function. | `FUNC?` | 28-29 |

#### 3.6.2 Current measurement

| CMD | Range / Parameters | Function | Sample | Page |
|---|---|---|---|---:|
| `[SENSe:]CURRent:{AC\|DC}:NULL[:STATe] {ON\|1\|OFF\|0}` | Boolean; default OFF; AC and DC settings independent | Enable/disable current relative-zero function. | `CURR:AC:NULL:STAT ON` | 29-30 |
| `[SENSe:]CURRent:{AC\|DC}:NULL[:STATe]?` | None | Query current relative-zero state. | `CURR:AC:NULL:STAT?` | 29-30 |
| `[SENSe:]CURRent:{AC\|DC}:NULL:VALue {<value>\|MIN\|MAX\|DEF}` | -12 A to +12 A; default 0 | Set current zero/reference value. | `CURR:AC:NULL:VAL 100mA` | 30 |
| `[SENSe:]CURRent:{AC\|DC}:NULL:VALue?` | None | Query current zero/reference value. | `CURR:AC:NULL:VAL?` | 30 |
| `[SENSe:]CURRent:{AC\|DC}:NULL:VALue:AUTO {ON\|1\|OFF\|0}` | Boolean | Enable/disable automatic zero selection using the first measurement as reference. | `CURR:AC:NULL:VAL:AUTO ON` | 30-31 |
| `[SENSe:]CURRent:{AC\|DC}:NULL:VALue:AUTO?` | None | Query automatic current zero selection. | `CURR:AC:NULL:VAL:AUTO?` | 30-31 |
| `[SENSe:]CURRent:{AC\|DC}:RANGe {<range>\|MIN\|MAX\|DEF}` | `{200uA\|2mA\|20mA\|200mA\|2A\|10A\|AUTO}`; 200 uA and 2 mA DC-only; AC minimum 20 mA | Set AC/DC current measurement range. | `CURR:AC:RANG 2` | 31 |
| `[SENSe:]CURRent:{AC\|DC}:RANGe?` | None | Query current range. | `CURR:AC:RANG?` | 31 |
| `[SENSe:]CURRent:{AC\|DC}:RANGe:AUTO {OFF\|ON}` | Boolean | Enable/disable automatic current ranging. | `CURR:AC:RANG:AUTO ON` | 31 |
| `[SENSe:]CURRent:{AC\|DC}:RANGe:AUTO?` | None | Query automatic current ranging. | `CURR:AC:RANG:AUTO?` | 31 |
| `[SENSe:]CURRent:{AC\|DC}:NPLC {Slow\|Medium\|Fast}` | `Slow`, `Medium`, `Fast` | Set current measurement sampling rate. | `CURR:DC:NPLC FAST` | 32 |
| `[SENSe:]CURRent:{AC\|DC}:NPLC?` | None | Query current sampling rate. | `CURR:DC:NPLC?` | 32 |
| `[SENSe:]CURRent:{AC\|DC}:TERMinals {Small\|Big}` | `Small` or `Big`; default Small | Select current input terminals (200 mA or 10 A). | `CURR:AC:TERM BIG` | 32 |
| `[SENSe:]CURRent:{AC\|DC}:TERMinals?` | None | Query selected current terminals. | `CURR:AC:TERM?` | 32 |

#### 3.6.3 Frequency and period measurement

| CMD | Range / Parameters | Function | Sample | Page |
|---|---|---|---|---:|
| `[SENSe:]{FREQuency\|PERiod}:NULL[:STATe] {ON\|1\|OFF\|0}` | Boolean; shared by frequency and period | Enable/disable relative-zero function. | `FREQ:NULL:STAT ON` | 32-33 |
| `[SENSe:]{FREQuency\|PERiod}:NULL[:STATe]?` | None | Query relative-zero state. | `FREQ:NULL:STAT?` | 32-33 |
| `[SENSe:]{FREQuency\|PERiod}:NULL:VALue {<value>\|MIN\|MAX\|DEF}` | -1.2E6 to +1.2E6; default 0 | Set frequency/period zero value. | `FREQ:NULL:VAL 1kHz` | 33 |
| `[SENSe:]{FREQuency\|PERiod}:NULL:VALue?` | None | Query frequency/period zero value. | `FREQ:NULL:VAL?` | 33 |
| `[SENSe:]{FREQuency\|PERiod}:NULL:VALue:AUTO {ON\|1\|OFF\|0}` | Boolean | Enable/disable automatic zero selection. | `FREQ:NULL:VAL:AUTO ON` | 33-34 |
| `[SENSe:]{FREQuency\|PERiod}:NULL:VALue:AUTO?` | None | Query automatic zero selection. | `FREQ:NULL:VAL:AUTO?` | 33-34 |
| `[SENSe:]{FREQuency\|PERiod}:VOLTage:RANGe {<range>\|MIN\|MAX\|DEF}` | `{200mV\|2V\|20V\|200V\|750V}`; default 20 V | Set voltage range used for frequency/period measurement. | `FREQ:VOLT:RANG 20` | 34 |
| `[SENSe:]{FREQuency\|PERiod}:VOLTage:RANGe?` | None | Query frequency/period voltage range. | `FREQ:VOLT:RANG?` | 34 |
| `[SENSe:]{FREQuency\|PERiod}:VOLTage:RANGe:AUTO {ON\|1\|OFF\|0}` | Boolean | Enable/disable automatic voltage ranging for frequency/period. | `FREQ:VOLT:RANG:AUTO ON` | 34 |
| `[SENSe:]{FREQuency\|PERiod}:VOLTage:RANGe:AUTO?` | None | Query automatic voltage ranging. | `FREQ:VOLT:RANG:AUTO?` | 34 |

#### 3.6.4 Resistance measurement

| CMD | Range / Parameters | Function | Sample | Page |
|---|---|---|---|---:|
| `[SENSe:]{RESistance\|FRESistance}:NPLC {Slow\|Medium\|Fast}` | `Slow`, `Medium`, `Fast` | Set resistance sampling rate. | `RES:NPLC FAST` | 35 |
| `[SENSe:]{RESistance\|FRESistance}:NPLC?` | None | Query resistance sampling rate. | `RES:NPLC?` | 35 |
| `[SENSe:]{RESistance\|FRESistance}:NULL[:STATe] {ON\|1\|OFF\|0}` | Boolean; default OFF | Enable/disable resistance relative-zero function. | `RES:NULL:STAT ON` | 35 |
| `[SENSe:]{RESistance\|FRESistance}:NULL[:STATe]?` | None | Query resistance relative-zero state. | `RES:NULL:STAT?` | 35 |
| `[SENSe:]{RESistance\|FRESistance}:NULL:VALue {<value>\|MIN\|MAX\|DEF}` | -120 Mohm to +120 Mohm; default 0 | Set resistance zero value. | `RES:NULL:VAL 0.1` | 35-36 |
| `[SENSe:]{RESistance\|FRESistance}:NULL:VALue?` | None | Query resistance zero value. | `RES:NULL:VAL?` | 35-36 |
| `[SENSe:]{RESistance\|FRESistance}:NULL:VALue:AUTO {ON\|1\|OFF\|0}` | Boolean | Enable/disable automatic resistance zero selection. | `RES:NULL:VAL:AUTO ON` | 36 |
| `[SENSe:]{RESistance\|FRESistance}:NULL:VALue:AUTO?` | None | Query automatic resistance zero selection. | `RES:NULL:VAL:AUTO?` | 36 |
| `[SENSe:]{RESistance\|FRESistance}:RANGe {<range>\|MIN\|MAX\|DEF}` | `{200ohm\|2kohm\|20kohm\|200kohm\|2Mohm\|10Mohm\|100Mohm}`; default 2 kohm | Set 2-wire/4-wire resistance range. | `RES:RANG 2000` | 36 |
| `[SENSe:]{RESistance\|FRESistance}:RANGe?` | None | Query resistance range. | `RES:RANG?` | 36 |
| `[SENSe:]{RESistance\|FRESistance}:RANGe:AUTO {OFF\|ON}` | Boolean | Enable/disable automatic resistance ranging. | `RES:RANG:AUTO ON` | 36-37 |
| `[SENSe:]{RESistance\|FRESistance}:RANGe:AUTO?` | None | Query automatic resistance ranging. | `RES:RANG:AUTO?` | 36-37 |

#### 3.6.5 Temperature measurement

| CMD | Range / Parameters | Function | Sample | Page |
|---|---|---|---|---:|
| `[SENSe:]TEMPerature:NULL[:STATe] {ON\|1\|OFF\|0}` | Boolean; default OFF | Enable/disable temperature relative-zero function. | `TEMP:NULL:STAT ON` | 37 |
| `[SENSe:]TEMPerature:NULL[:STATe]?` | None | Query temperature relative-zero state. | `TEMP:NULL:STAT?` | 37 |
| `[SENSe:]TEMPerature:NULL:VALue {<value>\|MIN\|MAX\|DEF}` | -1.0E15 to +1.0E15; default 0 | Set temperature zero value. | `TEMP:NULL:VAL 25` | 37-38 |
| `[SENSe:]TEMPerature:NULL:VALue?` | None | Query temperature zero value. | `TEMP:NULL:VAL?` | 37-38 |
| `[SENSe:]TEMPerature:NULL:VALue:AUTO {ON\|1\|OFF\|0}` | Boolean | Enable/disable automatic temperature zero selection. | `TEMP:NULL:VAL:AUTO ON` | 38 |
| `[SENSe:]TEMPerature:NULL:VALue:AUTO?` | None | Query automatic temperature zero selection. | `TEMP:NULL:VAL:AUTO?` | 38 |
| `[SENSe:]TEMPerature:TRANsducer:TYPE {FRTD\|RTD\|FTHermistor\|THERmistor\|TCouple}` | Listed probe types; default FRTD | Select temperature probe type. | `TEMP:TRAN:TYPE RTD` | 38 |
| `[SENSe:]TEMPerature:TRANsducer:TYPE?` | None | Query probe type. | `TEMP:TRAN:TYPE?` | 38 |
| `[SENSe:]TEMPerature:TRANsducer:TCouple:RJUNction {<temperature>\|MIN\|MAX\|DEF}` | -20 °C to +80 °C; default 0 °C | Set fixed thermocouple reference-junction temperature. | `TEMP:TRAN:TC:RJUN 20.0` | 38-39 |
| `[SENSe:]TEMPerature:TRANsducer:TCouple:RJUNction?` | None | Query fixed reference-junction temperature. | `TEMP:TRAN:TC:RJUN?` | 38-39 |
| `[SENSe:]TEMPerature:TRANsducer:TCouple:RJUNction:OFFSet:ADJust {<temperature>\|MIN\|MAX\|DEF}` | -20 °C to +20 °C; default 0 °C | Apply temperature fine adjustment to correct internal reference measurement offset. | `TEMP:TRAN:TC:RJUN:OFFS:ADJ -5` | 39 |
| `[SENSe:]TEMPerature:TRANsducer:TCouple:RJUNction:OFFSet:ADJust?` | None | Query reference-junction offset adjustment. | `TEMP:TRAN:TC:RJUN:OFFS:ADJ?` | 39 |
| `[SENSe:]TEMPerature:TRANsducer:TCouple:RJUNction:TYPE {INTernal\|FIXed}` | `INTernal` or `FIXed`; default INT | Select internal or fixed thermocouple reference junction. | `TEMP:TRAN:TC:RJUN:TYPE FIX` | 39 |
| `[SENSe:]TEMPerature:TRANsducer:TCouple:RJUNction:TYPE?` | None | Query reference-junction type. | `TEMP:TRAN:TC:RJUN:TYPE?` | 39 |
| `[SENSe:]TEMPerature:TRANsducer:TCouple:TYPE {E\|J\|K\|N\|R\|T}` | E, J, K, N, R, or T; default J | Select thermocouple type. | `TEMP:TRAN:TC:TYPE K` | 39-40 |
| `[SENSe:]TEMPerature:TRANsducer:TCouple:TYPE?` | None | Query thermocouple type. | `TEMP:TRAN:TC:TYPE?` | 39-40 |

#### 3.6.6 Voltage measurement

| CMD | Range / Parameters | Function | Sample | Page |
|---|---|---|---|---:|
| `[SENSe:]VOLTage:{AC\|DC}:NULL[:STATe] {ON\|1\|OFF\|0}` | Boolean; AC/DC settings independent | Enable/disable voltage relative-zero function. | `VOLT:AC:NULL:STAT ON` | 40-41 |
| `[SENSe:]VOLTage:{AC\|DC}:NULL[:STATe]?` | None | Query voltage relative-zero state. | `VOLT:AC:NULL:STAT?` | 40-41 |
| `[SENSe:]VOLTage:{AC\|DC}:NULL:VALue {<value>\|MIN\|MAX\|DEF}` | -1200 V to +1200 V; default 0 | Set voltage zero value. | `VOLT:AC:NULL:VAL 100mV` | 41 |
| `[SENSe:]VOLTage:{AC\|DC}:NULL:VALue?` | None | Query voltage zero value. | `VOLT:AC:NULL:VAL?` | 41 |
| `[SENSe:]VOLTage:{AC\|DC}:NULL:VALue:AUTO {ON\|1\|OFF\|0}` | Boolean | Enable/disable automatic voltage zero selection. | `VOLT:AC:NULL:VAL:AUTO ON` | 41-42 |
| `[SENSe:]VOLTage:{AC\|DC}:NULL:VALue:AUTO?` | None | Query automatic voltage zero selection. | `VOLT:AC:NULL:VAL:AUTO?` | 41-42 |
| `[SENSe:]VOLTage:{AC\|DC}:RANGe {<range>\|MIN\|MAX\|DEF}` | `{200mV\|2V\|20V\|200V\|1000V DC / 750V AC}`; AC default 20 V; DC default 1000 V | Set AC/DC voltage range. | `VOLT:AC:RANG 2` | 42 |
| `[SENSe:]VOLTage:{AC\|DC}:RANGe?` | None | Query AC/DC voltage range. | `VOLT:AC:RANG?` | 42 |
| `[SENSe:]VOLTage:{AC\|DC}:RANGe:AUTO {ON\|1\|OFF\|0}` | Boolean | Enable/disable automatic AC/DC voltage ranging. | `VOLT:AC:RANG:AUTO ON` | 42-43 |
| `[SENSe:]VOLTage:{AC\|DC}:RANGe:AUTO?` | None | Query automatic voltage ranging. | `VOLT:AC:RANG:AUTO?` | 42-43 |
| `[SENSe:]VOLTage:{AC\|DC}:NPLC {Slow\|Medium\|Fast}` | `Slow`, `Medium`, `Fast` | Set voltage sampling rate. | `VOLT:DC:NPLC FAST` | 43 |
| `[SENSe:]VOLTage:{AC\|DC}:NPLC?` | None | Query voltage sampling rate. | `VOLT:DC:NPLC?` | 43 |
| `[SENSe:]VOLTage[:DC]:IMPedance:AUTO {ON\|1\|OFF\|0}` | Boolean; default OFF | Enable/disable automatic DC input impedance mode. | `VOLT:IMP:AUTO OFF` | 43 |
| `[SENSe:]VOLTage[:DC]:IMPedance:AUTO?` | None | Query automatic DC input impedance mode. | `VOLT:IMP:AUTO?` | 43 |

#### 3.6.7 Capacitance measurement

| CMD | Range / Parameters | Function | Sample | Page |
|---|---|---|---|---:|
| `[SENSe:]CAPacitance:NULL[:STATe] {ON\|1\|OFF\|0}` | Boolean; default OFF | Enable/disable capacitance relative-zero function. | `CAP:NULL:STAT ON` | 43-44 |
| `[SENSe:]CAPacitance:NULL[:STATe]?` | None | Query capacitance relative-zero state. | `CAP:NULL:STAT?` | 43-44 |
| `[SENSe:]CAPacitance:NULL:VALue {<value>\|MIN\|MAX\|DEF}` | -12 mF to +12 mF; default 0 | Set capacitance zero value. | `CAP:NULL:VAL 100nF` | 44 |
| `[SENSe:]CAPacitance:NULL:VALue?` | None | Query capacitance zero value. | `CAP:NULL:VAL?` | 44 |
| `[SENSe:]CAPacitance:NULL:VALue:AUTO {ON\|1\|OFF\|0}` | Boolean | Enable/disable automatic capacitance zero selection. | `CAP:NULL:VAL:AUTO ON` | 44-45 |
| `[SENSe:]CAPacitance:NULL:VALue:AUTO?` | None | Query automatic capacitance zero selection. | `CAP:NULL:VAL:AUTO?` | 44-45 |
| `[SENSe:]CAPacitance:RANGe {<range>\|MIN\|MAX\|DEF}` | `{2nF\|20nF\|200nF\|2uF\|20uF\|200uF\|2mF\|AUTO}`; default 2 uF | Set capacitance range. | `CAP:RANG 2E-6` | 45 |
| `[SENSe:]CAPacitance:RANGe?` | None | Query capacitance range. | `CAP:RANG?` | 45 |
| `[SENSe:]CAPacitance:RANGe:AUTO {OFF\|ON}` | Boolean | Enable/disable automatic capacitance ranging. | `CAP:RANG:AUTO ON` | 45 |
| `[SENSe:]CAPacitance:RANGe:AUTO?` | None | Query automatic capacitance ranging. | `CAP:RANG:AUTO?` | 45 |

#### 3.6.8 Continuity measurement

| CMD | Range / Parameters | Function | Sample | Page |
|---|---|---|---|---:|
| `[SENSe:]CONTinuity:THReshold:VALue {<value>\|MIN\|MAX\|DEF}` | 0 to 2000 ohm; default 2000 ohm | Set continuity beep threshold resistance. | `CONT:THR:VAL 2000` | 45-46 |
| `[SENSe:]CONTinuity:THReshold:VALue?` | None | Query continuity threshold. | `CONT:THR:VAL?` | 45-46 |

### 3.7 SYSTem subsystem

| CMD | Range / Parameters | Function | Sample | Page |
|---|---|---|---|---:|
| `SYSTem:ERRor[:NEXT]?` | None | Read and remove the first error from the error queue. Response format: `<error_code>,<error_string>`. | `SYST:ERR?` | 46 |
| `SYSTem:BEEPer:STATe {ON\|1\|OFF\|0}` | Boolean; default OFF or ON as described by manual | Enable/disable beeper for continuity, diode, probe-maintenance measurement, or instrument error. Does not affect key sounds. | `SYST:BEEP:STAT OFF` | 46 |
| `SYSTem:BEEPer:STATe?` | None | Query beeper state. | `SYST:BEEP:STAT?` | 46 |

### 3.8 TRIGger subsystem

| CMD | Range / Parameters | Function | Sample | Page |
|---|---|---|---|---:|
| `TRIGger:COUNt {<count>\|MIN\|MAX\|DEF}` | 1 to 2,147,483,647; default 1 | Set number of triggers accepted in one measurement sequence. Total readings = trigger count × sample count. | `TRIG:COUN 10` | 47 |
| `TRIGger:COUNt?` | None | Query trigger count. | `TRIG:COUN?` | 47 |
| `TRIGger:DELay {<seconds>\|MIN\|MAX\|DEF}` | 1 to 3600 seconds; default 1 second | Set delay between trigger and first measurement. | `TRIG:DEL 2` | 47-48 |
| `TRIGger:DELay?` | None | Query trigger delay. | `TRIG:DEL?` | 47-48 |
| `TRIGger:DELay:AUTO {ON\|1\|OFF\|0}` | Boolean | Enable/disable automatic trigger delay. | `TRIG:DEL:AUTO 1` | 48 |
| `TRIGger:DELay:AUTO?` | None | Query automatic trigger delay state. | `TRIG:DEL:AUTO?` | 48 |
| `TRIGger:SLOPe {POSitive\|NEGative}` | `POSitive` or `NEGative`; default NEGative | Select rising or falling edge of rear-panel external trigger input. | `TRIG:SLOP POS` | 48-49 |
| `TRIGger:SLOPe?` | None | Query trigger slope. | `TRIG:SLOP?` | 48-49 |
| `TRIGger:SOURce {IMMediate\|EXTernal\|BUS}` | `IMMediate`, `EXTernal`, or `BUS`; default IMMediate | Select immediate, external hardware, or bus trigger source. | `TRIG:SOUR EXT` | 49 |
| `TRIGger:SOURce?` | None | Query trigger source. | `TRIG:SOUR?` | 49 |

## 4. Measurement workflow notes

### 4.1 Configure and read

```text
CONF:VOLT:DC 10
SAMP:COUN 2
READ?
```

This configures DC voltage measurement, requests two samples per trigger, and starts/reads the measurement. See pages 17-22.

### 4.2 Initiate and fetch

```text
CONF:VOLT:DC
TRIG:SOUR EXT
INIT
FETC?
```

`INIT` arms the trigger system. The external trigger must arrive before `FETC?` can return the completed measurement data. `FETCh?` does not erase the readings from reading memory. See pages 4-5 and 17-18.

### 4.3 Trigger count and sample count

The manual states that total returned measurements equal `SAMPle:COUNt × TRIGger:COUNt`. The reading memory can hold up to 10,000 measurements. See pages 6-7 and 47.

## 5. Documentation notes and cautions

1. **Do not treat illustrative samples as additional commands.** Only syntax explicitly documented in the manual is cataloged above.
2. **Query forms:** A query form is listed only where the manual documents it. Do not assume every setting command has a query form.
3. **Optional syntax:** Square brackets and braces are notation only and must not be sent literally.
4. **Abbreviations:** Use the uppercase portion of a keyword for the documented short form. The manual warns that arbitrary truncations can cause errors.
5. **Manual inconsistencies:** Some printed descriptions contain apparent typographical or formatting errors. Where a range or syntax is ambiguous, the table preserves the manual's stated information and does not silently replace it with an external specification.
6. **Connection details:** The supplied programming manual is not a complete hardware/interface installation guide. Interface-specific connection information must be taken from the applicable hardware/user documentation, not guessed from this file.

## 6. Source

- **Document:** *UT8805E SCPI Programming Manual*
- **Manufacturer:** UNI-T
- **Length:** 49 printed pages
- **Source restriction:** This reference was prepared exclusively from the supplied manual. Page citations refer to its printed page numbering.
