# Keithley Model 2100 Calibration SCPI Command Reference

> **Source restriction:** Prepared only from the supplied `instruments\raw\Keithley_2100-user-manual.pdf`, which is actually the *Model 2100 6 1/2-Digit Resolution Digital Multimeter Calibration Manual*, document 2100-905-01 Rev. C, March 2021. No commands were added from the separate Model 2100 User's Manual or any external source.

## 1. Introduction

This document records the SCPI commands explicitly documented in the supplied calibration manual for the Keithley Model 2100 DMM. The manual focuses on calibration adjustment and performance verification, not the complete normal-operation command set. Therefore, this reference includes only the configuration, averaging, identification, and protected-calibration commands used by the calibration procedures.

The calibration procedures cover:

- Front- and rear-terminal zero calibration
- DC voltage adjustment: 100 mV, 1 V, 10 V, 100 V, and 1000 V
- AC voltage adjustment: 100 mV, 1 V, 10 V, 100 V, and 750 V RMS at 1 kHz
- Two-wire and four-wire resistance adjustment: 100 ohm to 100 Mohm
- DC current adjustment: 10 mA, 100 mA, and 1 A ranges
- AC current adjustment: 1 A and 3 A ranges at 1 kHz
- Calibration date, EEPROM save, and calibration lock

### 1.1 Syntax conventions

| Notation | Meaning | Example |
|---|---|---|
| Uppercase command text | The manual prints command mnemonics in uppercase. | `CONF:VOLT:DC` |
| `:` | Separates hierarchical command keywords. | `CAL:PROT:DC:STEP` |
| `,` | Separates multiple arguments. | `CAL:PROT:DC:STEP 1,10` |
| `<...>` | A required value or string must replace the placeholder. | `CAL:PROT:DATE <MM/DD/YYYY>` |
| `?` | Query form. | `*IDN?` |
| Scientific notation | Used for resistance values and actual calibrator outputs. | `1E6`, `0.9999615E6` |
| Quoted date string | Calibration date must be enclosed in double quotes. | `"01/05/2020"` |

**Limitation:** The supplied calibration manual does not define the complete SCPI grammar, abbreviation rules, optional keywords, terminators, query forms for setting commands, or all legal parameter values. These are not inferred.

## 2. Connections

| Item | Manual requirement | Manual reference |
|---|---|---:|
| Remote interface | Calibration SCPI commands are sent over USB. | 1-1 |
| Control application | Keithley KI-Tool; use `Tool > Command Control`, enter commands in `Send String`, then select `Write` or `Query`. | 1-2 to 1-3 |
| VISA layer choices | Keithley I/O Layer 5.0 or later; NI-VISA 3.1 or later; Agilent I/O Library Suite 14.2 or later. | 1-2 |
| Communications check | Connect the Model 2100 through USB, start KI-Tool, confirm the model, and verify response to function controls. | 1-2 |
| DC voltage | Shielded, low-thermal EMF copper leads from Fluke 5700A HI/LO to Model 2100 HI/LO. | 4-1 to 4-3 |
| AC voltage | Coaxial cable with dual banana terminals from Fluke 5700A HI/LO to Model 2100 HI/LO. | 4-4 to 4-5 |
| Resistance, 2-wire | Shielded, low-thermal leads from calibrator HI/LO to DMM HI/LO. | 5-1, 5-5 |
| Resistance, 4-wire | Connect calibrator output HI/LO and sense HI/LO to DMM input HI/LO and sense HI/LO. | 5-2 to 5-4 |
| Current | Connect Fluke 5725A current-output HI/LO to Model 2100 AMPS/LO. | 6-1 to 6-3 |
| Stabilization | Allow connections to stabilize for at least 5 minutes before adjustment. | 2-1 to 6-3 |
| Warm-up | Specifications and performance-verification limits require a 2-hour warm-up. | 1-4, 8-1 |

### 2.1 Calibration equipment

The manual recommends a Fluke 5700A calibrator and Fluke 5725A amplifier, or equivalent. Performance verification also requires a function generator with frequency accuracy of 25 ppm or better.

## 3. SCPI TABLE

### 3.1 Identification and calibration access

| CMD | Range / Parameters | Function | Sample | Manual reference |
|---|---|---|---|---:|
| `*IDN?` | None | Return instrument identification, including the firmware revision. Firmware 1.03 or 1.04 must be updated before the documented calibration procedure. | `*IDN?` | 1-5 |
| `CAL:PROT:CODE <code>` | Up to 8-character string; manual gives default `p8125652` | Unlock the protected calibration function. | `CAL:PROT:CODE p8125652` | 1-5 |
| `CAL:PROT:INIT` | None | Initiate the protected calibration routine after unlocking it. | `CAL:PROT:INIT` | 1-5 |

### 3.2 Measurement configuration commands used by calibration

| CMD | Range / Parameters documented here | Function | Sample | Manual reference |
|---|---|---|---|---:|
| `CONF:VOLT:DC <range>` | `{0.1|1|10|100|1000}` V | Configure the DC voltage range used for adjustment. | `CONF:VOLT:DC 10` | 4-2 to 4-3 |
| `CONF:VOLT:AC <range>` | `{0.1|1|10|100|750}` V RMS | Configure the AC voltage range used for adjustment. Calibration signals are at 1 kHz. | `CONF:VOLT:AC 0.1` | 4-4 to 4-5 |
| `CONF:RES <range>` | Documented calibration ranges: `1E6`, `10E6`, `100E6` ohm | Configure two-wire resistance for the selected calibration range. | `CONF:RES 10E6` | 5-1, 5-5 |
| `CONF:FRES <range>` | `{1E2|1E3|1E4|1E5|1E6|10E6}` ohm | Configure four-wire resistance for the selected calibration range. | `CONF:FRES 1E4` | 5-2 to 5-4 |
| `CONF:CURR:DC <range>` | `{0.01|0.1|1}` A | Configure the DC current adjustment range. | `CONF:CURR:DC 0.1` | 6-1 to 6-2 |
| `CONF:CURR:AC <range>` | `{1|3}` A | Configure the AC current adjustment range. | `CONF:CURR:AC 1` | 6-3 |
| `RES:NPLC <value>` | Documented value: `10` | Set the integration time for two-wire resistance calibration. | `RES:NPLC 10` | 5-1, 5-5 |
| `FRES:NPLC <value>` | Documented value: `10` | Set the integration time for four-wire resistance calibration. | `FRES:NPLC 10` | 5-2 to 5-4 |
| `CURR:NPLC <value>` | Documented value: `10` | Set the integration time for DC current calibration. | `CURR:NPLC 10` | 6-1 to 6-2 |
| `AVERAGE:COUNT <count>` | Documented values: `25` or `100` | Set averaging count for resistance adjustment. | `AVERAGE:COUNT 100` | 5-1 to 5-5 |

### 3.3 Protected DC calibration adjustment

| CMD | Range / Parameters | Function | Sample | Manual reference |
|---|---|---|---|---:|
| `CAL:PROT:DC:STEP 1,<range>` | Step `1`; second argument identifies active range | Adjust input offset for DC voltage, resistance, or DC current. The source must be set to zero as specified in the procedure. | `CAL:PROT:DC:STEP 1,10` | 4-2 to 6-2 |
| `CAL:PROT:DC:STEP 2,<actual>` | Step `2`; applied/reference value | Adjust full-scale or specified region using the applied calibrator value. For resistance, enter the actual calibrator output, commonly in scientific notation. | `CAL:PROT:DC:STEP 2,0.9999615E6` | 4-2 to 6-2 |
| `CAL:PROT:DC:STEP 3,0` | Fixed arguments shown | Perform front-panel zero calibration with a low-thermal four-wire short. | `CAL:PROT:DC:STEP 3,0` | 2-1 |
| `CAL:PROT:DC:STEP 4,0` | Fixed arguments shown | Perform rear-panel zero calibration with a low-thermal four-wire short. | `CAL:PROT:DC:STEP 4,0` | 3-1 |

After each adjustment command, wait for the Model 2100 display to show `Cali OK` before continuing.

### 3.4 Protected AC calibration adjustment

| CMD | Range / Parameters | Function | Sample | Manual reference |
|---|---|---|---|---:|
| `CAL:PROT:AC:STEP 1,<value>` | Step `1`; applied low-region value | Adjust 10% of AC voltage range, 10% of 1 A AC current range, or the documented lower region of 3 A range. | `CAL:PROT:AC:STEP 1,0.1` | 4-4 to 4-5, 6-3 |
| `CAL:PROT:AC:STEP 2,<value>` | Step `2`; applied upper/full-scale value | Adjust full-scale AC voltage/current or the upper region of the 3 A range. | `CAL:PROT:AC:STEP 2,1` | 4-4 to 4-5, 6-3 |
| `CAL:PROT:AC:STEP 3,0.01` | Fixed documented AC-current point: 0.01 A | Adjust 1% of the 1 A AC current range at 1 kHz. | `CAL:PROT:AC:STEP 3,0.01` | 6-3 |

### 3.5 Calibration completion commands

| CMD | Range / Parameters | Function | Sample | Manual reference |
|---|---|---|---|---:|
| `CAL:PROT:DATE <MM/DD/YYYY>` | Date string enclosed in double quotes | Set the calibration date. The due date is automatically calculated for 12 months. | `CAL:PROT:DATE "01/05/2020"` | 7-1 |
| `CAL:PROT:SAVE` | None | Save calibration constants in EEPROM. | `CAL:PROT:SAVE` | 7-1 |
| `CAL:PROT:LOCK` | None | Lock the calibration function after saving. | `CAL:PROT:LOCK` | 7-1 |

## 4. Calibration range matrix

### 4.1 DC voltage

| DMM range | Zero/offset source | Full-scale source | Configuration | Adjustment commands | Manual reference |
|---:|---:|---:|---|---|---:|
| 0.1 V | 0 V DC | 0.1 V DC | `CONF:VOLT:DC 0.1` | `CAL:PROT:DC:STEP 1,0.1`; `CAL:PROT:DC:STEP 2,0.1` | 4-2 to 4-3 |
| 1 V | 0 V DC | 1 V DC | `CONF:VOLT:DC 1` | `CAL:PROT:DC:STEP 1,1`; `CAL:PROT:DC:STEP 2,1` | 4-2 |
| 10 V | 0 V DC | 10 V DC | `CONF:VOLT:DC 10` | `CAL:PROT:DC:STEP 1,10`; `CAL:PROT:DC:STEP 2,10` | 4-2 |
| 100 V | 0 V DC | 100 V DC | `CONF:VOLT:DC 100` | `CAL:PROT:DC:STEP 1,100`; `CAL:PROT:DC:STEP 2,100` | 4-3 |
| 1000 V | 0 V DC | 1000 V DC | `CONF:VOLT:DC 1000` | `CAL:PROT:DC:STEP 1,1000`; `CAL:PROT:DC:STEP 2,1000` | 4-3 |

### 4.2 AC voltage at 1 kHz

| DMM range | Low point | Full-scale point | Configuration | Adjustment commands | Manual reference |
|---:|---:|---:|---|---|---:|
| 0.1 V | 0.01 V | 0.1 V | `CONF:VOLT:AC 0.1` | `CAL:PROT:AC:STEP 1,0.01`; `CAL:PROT:AC:STEP 2,0.1` | 4-4 |
| 1 V | 0.1 V | 1 V | `CONF:VOLT:AC 1` | `CAL:PROT:AC:STEP 1,0.1`; `CAL:PROT:AC:STEP 2,1` | 4-4 |
| 10 V | 1 V | 10 V | `CONF:VOLT:AC 10` | `CAL:PROT:AC:STEP 1,1`; `CAL:PROT:AC:STEP 2,10` | 4-4 to 4-5 |
| 100 V | 10 V | 100 V | `CONF:VOLT:AC 100` | `CAL:PROT:AC:STEP 1,10`; `CAL:PROT:AC:STEP 2,100` | 4-5 |
| 750 V | 75 V | 750 V | `CONF:VOLT:AC 750` | `CAL:PROT:AC:STEP 1,75`; `CAL:PROT:AC:STEP 2,750` | 4-5 |

### 4.3 DC current

| DMM range | Offset point | Calibration point(s) | Configuration | Manual reference |
|---:|---:|---:|---|---:|
| 0.01 A | 0 A | 0.01 A full scale | `CONF:CURR:DC 0.01`; `CURR:NPLC 10` | 6-1 |
| 0.1 A | 0 A | 0.06 A mid-region; 0.12 A full-scale adjustment | `CONF:CURR:DC 0.1`; `CURR:NPLC 10` | 6-2 |
| 1 A | 0 A | 1 A full scale | `CONF:CURR:DC 1`; `CURR:NPLC 10` | 6-2 |

### 4.4 AC current at 1 kHz

| DMM range | Calibration points | Configuration | Adjustment commands | Manual reference |
|---:|---|---|---|---:|
| 1 A | 0.1 A, 1 A, 0.01 A | `CONF:CURR:AC 1` | `STEP 1,0.1`; `STEP 2,1`; `STEP 3,0.01` | 6-3 |
| 3 A | 0.2 A and 2 A | `CONF:CURR:AC 3` | `STEP 1,0.2`; `STEP 2,2` | 6-3 |

## 5. Required calibration workflow

1. Warm up the Model 2100 and standards. Specifications require 2 hours.
2. Verify firmware with `*IDN?`. Firmware 1.03 or 1.04 must be updated before using this procedure.
3. Connect the correct source, cables, and DMM terminals. Allow at least 5 minutes for thermal stabilization.
4. Unlock with `CAL:PROT:CODE <code>`.
5. Start calibration using `CAL:PROT:INIT`.
6. Configure the required measurement range and, where specified, NPLC and averaging count.
7. Place the calibrator in `OPERATE` only after connections and settings are ready.
8. Send the appropriate `CAL:PROT:DC:STEP` or `CAL:PROT:AC:STEP` command.
9. Wait for `Cali OK` after every adjustment before changing the source or range.
10. Return the calibrator to `STANDBY` before rewiring or changing sensitive configurations.
11. Set the calibration date, save constants to EEPROM, and lock calibration.
12. Perform the documented performance verification after adjustment.

## 6. Important cautions

1. **This is a calibration manual, not the full programming manual.** Do not treat this file as a complete list of Model 2100 measurement commands.
2. **Calibration changes instrument constants.** Restrict these commands to authorized calibration workflows with traceable standards.
3. **Maximum voltage:** The manual warns not to apply more than 1000 V peak to the Model 2100.
4. **No switching equipment:** The manual instructs not to connect calibration equipment through a scanner or other switching equipment.
5. **Thermal EMF control:** Use copper, shielded, low-thermal EMF connections and keep drafts away from low-thermal shorts.
6. **Use actual calibrator output for resistance.** For example, enter `0.9999615E6` rather than assuming exactly `1E6` when that is the standard's actual output.
7. **Wait for status:** Do not proceed until `Cali OK` appears after each adjustment command.
8. **High-resistance ambiguity:** The manual prints `CAL:PROT:DC:STEP 2,99.99750` for the 100 Mohm step. This reference records it as printed and does not infer a missing exponent.
9. **Calibration due date:** The manual states that the due date is calculated automatically for 12 months after setting the calibration date.

## 7. Manual references

- **Manufacturer:** Keithley Instruments, LLC
- **Instrument:** Model 2100 6 1/2-Digit Resolution Digital Multimeter
- **Document:** Calibration Manual
- **Document number:** 2100-905-01 Rev. C
- **Revision:** March 2021
- **Calibration controls and software:** Section 1, pages 1-1 to 1-5
- **Front/rear zero calibration:** Sections 2 and 3
- **Voltage adjustment:** Section 4
- **Resistance adjustment:** Section 5
- **Current adjustment:** Section 6
- **Calibration date/save/lock:** Section 7
- **Performance verification:** Section 8
- **Separate manual named by this source but not used:** Model 2100 User's Manual, document 2100-900-01
