# GW Instek GPD-3303S Remote Command Reference

> **Source restriction:** Prepared only from the supplied `gwinstek_gpd3303s_user-manual.pdf`. No commands, ranges, interfaces, or behaviors were added from external sources.

## 1. Introduction

The GW Instek GPD-3303S is a three-output regulated DC power supply. CH1 and CH2 are independently programmable from 0 to 30 V and 0 to 3 A. They can also operate in tracking-series mode, up to 60 V at 3 A, or tracking-parallel mode, up to 30 V at 6 A. CH3 is selected manually at 2.5 V, 3.3 V, or 5 V with a 3 A rating.

The GPD-3303S supports remote control through the rear-panel USB slave port. The manual documents a compact command set for setting and reading CH1/CH2 voltage and current, selecting operating mode, controlling output and beep state, managing four setup memories, identifying the instrument, reading status, and retrieving errors.

### 1.1 Command syntax rules

| Rule | Description | Example |
|---|---|---|
| Case sensitivity | Commands are not case-sensitive. | `VSET1:5.000`, `vset1:5.000` |
| `<X>` | Required output channel selector: `1` for CH1 or `2` for CH2. | `VSET1?` |
| `:` | Separator between the command/channel header and a set value. | `ISET1:2.000` |
| `<Boolean>` | Boolean value: `0` = off, `1` = on. | `OUT1` |
| `<NR1>` | Integer argument. | `TRACK2` |
| `<NR2>` | Decimal numeric argument. | `VSET1:20.345` |
| `?` | Query form; returns a setting, measured value, status, identification, help, or error. | `VOUT1?` |
| Command length | Command mnemonic must be 15 characters or fewer. | See manual error table. |

### 1.2 Instrument-dependent resolution

| Model | Voltage display/program example | Current display/program example |
|---|---:|---:|
| GPD-3303S | 1 mV resolution, e.g. `20.345 V` | 1 mA resolution, e.g. `2.234 A` |
| GPD-3303D | 100 mV resolution, e.g. `20.3 V` | 10 mA resolution, e.g. `2.23 A` |

## 2. Connections

| Item | Manual specification | Page |
|---|---|---:|
| Remote interface | Rear-panel USB slave port | 17, 36-37 |
| Optional cable | GTL-246, USB 2.0 A-B type | 48 |
| Baud rate | 9600 | 36 |
| Parity | None | 36 |
| Data bits | 8 | 36 |
| Stop bits | 1 | 36 |
| Flow control | None | 36 |
| Connection check | Send `*IDN?`; expected response contains manufacturer, model, serial number, and firmware. | 36, 43 |
| Enter remote mode | Connect USB; connection is automatic, display shows `USB...YES`, and front panel locks. | 37 |
| Leave remote mode | Disconnect USB; display shows `USB...NO`; hold Lock until unlocked. | 37 |

### 2.1 Remote identification response

The documented response format is:

```text
GW INSTEK,GPD-3303x,SN: xxxxxxxx,Vx.xx
```

The fields are manufacturer, model, serial number, and firmware version.

## 3. SCPI TABLE

> The manual calls these remote-control commands. The syntax is instrument-specific and is not a full hierarchical SCPI command tree.

| CMD | Range / Parameters | Function | Sample | Response time | Page |
|---|---|---|---|---:|---:|
| `ISET<X>:<NR2>` | `<X>` = `1` or `2`; CH1/CH2 setting range 0-3 A | Set the current limit for CH1 or CH2. | `ISET1:2.234` | Minimum 70 ms | 39-40 |
| `ISET<X>?` | `<X>` = `1` or `2` | Return the programmed current setting. | `ISET1?` | Minimum 80 ms | 39-40 |
| `VSET<X>:<NR2>` | `<X>` = `1` or `2`; CH1/CH2 setting range 0-30 V | Set the programmed output voltage. The error example states values must be `<=32 V`, while the rated operating output is 0-30 V. | `VSET1:20.345` | Minimum 70 ms | 38-40 |
| `VSET<X>?` | `<X>` = `1` or `2` | Return the programmed voltage setting. | `VSET1?` | Minimum 80 ms | 39, 41 |
| `IOUT<X>?` | `<X>` = `1` or `2` | Return actual output current. | `IOUT1?` | Minimum 80 ms | 39, 41 |
| `VOUT<X>?` | `<X>` = `1` or `2` | Return actual output voltage. | `VOUT1?` | Minimum 80 ms | 39, 41 |
| `TRACK<NR1>` | `0` = independent; `1` = tracking series; `2` = tracking parallel | Select CH1/CH2 operating mode. | `TRACK0` | Minimum 70 ms | 39, 41 |
| `BEEP<Boolean>` | `0` = off; `1` = on | Turn beep off or on. | `BEEP1` | Minimum 70 ms | 39, 42 |
| `OUT<Boolean>` | `0` = all outputs off; `1` = all outputs on | Turn CH1/CH2/CH3 outputs off or on. | `OUT1` | Minimum 70 ms | 39, 42 |
| `STATUS?` | Returns an 8-bit status value | Return CH1/CH2 CV/CC state, tracking mode, beep state, and output state. | `STATUS?` | Minimum 400 ms | 39, 42 |
| `*IDN?` | No parameter | Return manufacturer, model, serial number, and firmware version. | `*IDN?` | Minimum 300 ms | 36, 39, 43 |
| `RCL<NR1>` | `1-4` = memory 1-4 | Recall a stored panel setup. Output is recalled as off. | `RCL1` | Minimum 70 ms | 35, 39, 43 |
| `SAV<NR1>` | `1-4` = memory 1-4 | Save the current panel setup. Output is saved as off. | `SAV1` | Minimum 70 ms | 34, 39, 43 |
| `HELP?` | No parameter | Return the supported command list and meanings, excluding `HELP?` itself. | `HELP?` | Minimum 1000 ms | 39, 43-44 |
| `ERR?` | No parameter | Return the most recent instrument error message. | `ERR?` | Minimum 70 ms | 39, 44 |

### 3.1 `STATUS?` bit definition

The response contains eight status bits:

| Bit | Item | `0` meaning | `1` meaning / encoding |
|---:|---|---|---|
| 0 | CH1 regulation | CC mode | CV mode |
| 1 | CH2 regulation | CC mode | CV mode |
| 2-3 | Tracking mode | Encoded field | `01` independent, `11` tracking series, `10` tracking parallel |
| 4 | Beep | Off | On |
| 5 | Reserved | N/A | N/A |
| 6 | Output | Off | On |
| 7 | Reserved | N/A | N/A |

#### Example decoder logic

For an integer status value `s`:

- CH1 mode: `CV` if `s & 0x01`, otherwise `CC`.
- CH2 mode: `CV` if `s & 0x02`, otherwise `CC`.
- Tracking field: `(s >> 2) & 0x03`.
- Beep enabled: `bool(s & 0x10)`.
- Output enabled: `bool(s & 0x40)`.

## 4. Operating modes relevant to automation

| Mode | Command | Output capability | Automation note | Page |
|---|---|---|---|---:|
| Independent | `TRACK0` | CH1: 0-30 V/0-3 A; CH2: 0-30 V/0-3 A | CH1 and CH2 settings are controlled independently. | 23-24, 41 |
| Tracking series | `TRACK1` | Combined: 0-60 V/0-3 A | CH1 is master. Without a common terminal, actual combined voltage is twice the CH1 reading. | 27-31, 41 |
| Tracking parallel | `TRACK2` | Combined: 0-30 V/0-6 A | CH1 controls combined output. Actual combined current is twice the CH1 current reading. CH2 control is disabled. | 32-33, 41 |
| CH3 independent | No remote voltage-selection command documented | 2.5/3.3/5 V, 3 A | Voltage is selected from the front panel. `OUT0/1` controls all outputs, including CH3. | 25-26, 42 |

**Important:** Changing independent/series/parallel mode, saving a setup, or recalling a setup automatically turns the output off.

## 5. Error messages

| Error message | Meaning | Example / condition | Page |
|---|---|---|---:|
| `Program mnemonic too long` | Command mnemonic exceeds 15 characters. | Shorten the command. | 38 |
| `Invalid character` | An unsupported character or symbol was entered. | `VOUT#` | 38 |
| `Missing parameter` | A required set value is absent. | `VSET:` | 38 |
| `Data out of range` | Numeric value exceeds the accepted range. | Manual example: `VSET:33` | 38 |
| `Command not allowed` | Command is invalid in the current operating mode. | Setting CH2 while tracking mode is active. | 38 |
| `Undefined header` | Command does not exist or syntax is incorrect. | Misspelled command. | 38 |

Use `ERR?` after a rejected command to retrieve the latest error.

## 6. Practical ATE command sequences

### 6.1 Connection and identity check

```text
*IDN?
ERR?
```

Allow at least 300 ms for `*IDN?` according to the manual.

### 6.2 Configure independent CH1 and enable output

```text
OUT0
TRACK0
VSET1:5.000
ISET1:0.500
VSET1?
ISET1?
OUT1
```

Use the setting queries before enabling output to verify accepted values. Allow at least 70 ms after each set command and at least 80 ms before reading each setting query response.

### 6.3 Read actual CH1 output

```text
VOUT1?
IOUT1?
STATUS?
```

`VOUT1?` and `IOUT1?` return actual readback values. `STATUS?` determines whether CH1 is in CV or CC regulation.

### 6.4 Safe mode transition to series tracking

```text
OUT0
TRACK1
VSET1:12.000
ISET1:1.000
OUT1
STATUS?
```

The combined output can reach approximately 24 V when CH1 is set to 12 V in series tracking. The manual states that mode changes automatically turn output off, but explicitly issuing `OUT0` first makes the automation sequence unambiguous.

### 6.5 Store and recall a setup

```text
OUT0
TRACK0
VSET1:3.300
ISET1:0.500
SAV1
RCL1
VSET1?
ISET1?
```

The output state is always saved and recalled as off.

## 7. Timing and driver-design notes

1. **Respect documented minimum response times.** Set commands generally require at least 70 ms; setting/readback queries require at least 80 ms; `*IDN?` requires at least 300 ms; `STATUS?` at least 400 ms; and `HELP?` at least 1000 ms.
2. **Do not program CH2 in tracking mode.** The manual explicitly gives this as a `Command not allowed` condition.
3. **Separate setpoint from readback.** `VSET<X>?` and `ISET<X>?` return programmed settings. `VOUT<X>?` and `IOUT<X>?` return actual output values.
4. **Treat mode changes and memory operations as output-off events.** Independent/series/parallel changes and save/recall operations automatically turn the output off.
5. **CH3 is not remotely programmable in this command set.** No documented command selects 2.5 V, 3.3 V, or 5 V. Only the global `OUT<Boolean>` command affects CH3 remotely.
6. **Warm-up for accuracy.** The manual specifies at least 30 minutes powered on at 20-30 degrees C before applying accuracy specifications.
7. **Use rated operating limits.** CH1/CH2 are rated 0-30 V and 0-3 A independently. Although the error example mentions `<=32 V`, it should not be treated as a rated 32 V operating capability.

## 8. Electrical and metrology summary

| Parameter | GPD-3303S specification | Page |
|---|---|---:|
| CH1/CH2 independent | 0-30 V, 0-3 A each | 47 |
| Series tracking | 0-60 V, 0-3 A | 47 |
| Parallel tracking | 0-30 V, 0-6 A | 47 |
| CH3 | 2.5 V/3.3 V/5.0 V, 3 A | 47 |
| Voltage programming accuracy | +/- (0.03% of reading + 10 mV) | 48 |
| Current programming accuracy | +/- (0.3% of reading + 10 mA) | 48 |
| Voltage readback accuracy | +/- (0.03% of reading + 10 mV) | 48 |
| Current readback accuracy | +/- (0.3% of reading + 10 mA) | 48 |
| Voltage ripple/noise | <=1 mVrms, 5 Hz-1 MHz | 47 |
| Current ripple/noise | <=3 mArms | 47 |
| Recovery time | <=100 us for 50% load change, minimum load 0.5 A | 47 |
| Tracking error | <=0.5% + 10 mV of master | 47 |

## 9. Manual references

- **Manufacturer:** Good Will Instrument Co., Ltd. / GW Instek
- **Equipment:** GPD-3303 Series DC Power Supply
- **Models covered:** GPD-3303D and GPD-3303S
- **Remote-control setup:** pages 36-37
- **Command syntax and errors:** page 38
- **Command list:** page 39
- **Command details:** pages 40-44
- **Specifications:** pages 47-48
- **Source file:** `gwinstek_gpd3303s_user-manual.pdf`

## 10. Documentation cautions

The manual contains several model-name typographical variations such as `GPS-3303D` where the surrounding document identifies the product as `GPD-3303D`. This reference preserves the supported command behavior while using the consistent GPD model name. It does not infer a terminator character, USB driver name, VISA resource string, or commands not explicitly documented in the supplied manual.
