# Prodigit 3315G Supported Remote Commands

> **Source:** `<File>3302G_Operation Manual_Rev E_EN_202610.pdf</File>`, P/N 9003302G02 Rev. E. Only commands marked for the **331XG** module family, applicable to the **3315G**, are included. Commands exclusive to 331XF, 333XF, 334XF/G, 3340XF/G, or LED-simulator modules are excluded.

## 1. Introduction

This reference covers the Prodigit 3315G DC electronic-load module installed in a 3302G mainframe.

| Model | Maximum current | Maximum voltage | Maximum power |
|---|---:|---:|---:|
| 3315G | 15 A | 60 V | 75 W |

The 3315G belongs to the manual's `331XG` command category and support CC, CR, CV, and CP modes. The module does not support LED mode.

## 2. Connections

The 3302G mainframe can be fitted with GPIB, RS-232, USB, or LAN interfaces.

| Interface | Manual setting |
|---|---|
| RS-232 | 9600 to 115200 baud, no parity, 8 data bits, 1 stop bit, hardware RTS/CTS |
| USB | USB-to-serial; manual example uses 115200 baud and hardware flow control |
| LAN | Serial I/O TCP port 4001; example configuration 115200, N, 8, 1, RS-232 RTS/CTS |
| GPIB | Address set from front panel; up to 15 devices; individual cable <=2 m; total cable length <20 m |

Accepted terminators are LF, LF with EOI, CR+LF, or CR+LF with EOI. Separate combined commands with `;`.

## 3. Supported command table

`[PRESet:]`, `[STATe:]`, and `[SYStem:]` are optional complex-format roots. The shorter simple-format form is valid.

### 3.1 Load setpoints and dynamic operation

| CMD | Range / Parameters | Function | Sample | Page |
|---|---|---|---|---:|
| `[PRESet:]RISE <NR2>` / `[PRESet:]RISE?` | mA/us | Set/query low-to-high current slew rate. Values above capability are clamped. | `RISE 0.5` | 36, 39, 48, 50, 54 |
| `[PRESet:]FALL <NR2>` / `[PRESet:]FALL?` | mA/us | Set/query high-to-low current slew rate. | `FALL 0.5` | 36, 39, 48, 50, 54 |
| `[PRESet:]{PERI|PERD}:{HIGH|LOW} <NR2>` / query | ms | Set/query high or low duration of a dynamic waveform. | `PERD:HIGH 10` | 36, 39, 48, 50, 54-55 |
| `[PRESet:]LDONv <NR2>` / `[PRESet:]LDONv?` | V | Set/query voltage threshold that automatically turns load on. | `LDONV 3.0` | 36, 39, 48, 50, 55 |
| `[PRESet:]LDOFfv <NR2>` / `[PRESet:]LDOFfv?` | V | Set/query voltage threshold that automatically turns load off. | `LDOFFV 2.5` | 36, 39, 48, 50, 55 |
| `[PRESet:]{CC|CURR}:{HIGH|LOW} <NR2>` / query | A; 0 to 15 A module capability | Set/query high or low current level. | `CURR:HIGH 5` | 36, 39, 48, 50, 55 |
| `[PRESet:]CP:{HIGH|LOW} <NR2>` / query | W; up to 75 W module capability | Set/query high or low constant-power level. | `CP:HIGH 50` | 36, 39, 48, 50, 56 |
| `[PRESet:]{CR|RES}:{HIGH|LOW} <NR2>` / query | ohm; model range applies | Set/query high or low resistance level. | `RES:LOW 10` | 36, 39, 48, 50, 56 |
| `[PRESet:]CV:{HIGH|LOW} <NR2>` / query | V; maximum module voltage 60 V | Set/query high or low constant-voltage level. | `CV:HIGH 12` | 36, 39, 48, 50, 57 |
| `[STATe:]LOAD {ON|OFF}` / `[STATe:]LOAD?` | Query: `0` off, `1` on | Control/query load input state. | `LOAD ON` | 41, 52, 68 |
| `[STATe:]MODE {CC|CR|CV|CP}` / `[STATe:]MODE?` | Query: `0` CC, `1` CR, `2` CV, `3` CP | Select/query operating mode. | `MODE CC` | 41, 52, 68-69 |
| `[STATe:]PRESet {ON|OFF}` / `[STATe:]PRESet?` | Query: `0` off, `1` on | Enable/query preset mode. | `PRESET OFF` | 41, 52, 69 |
| `[STATe:]SENSe {ON|AUTO}` / `[STATe:]SENSe?` | Query: `0` off/auto, `1` on | Select/query remote-sense operation. | `SENSE AUTO` | 41, 52, 69 |
| `[STATe:]{LEVel|LEV} {HIGH|LOW}` / query | Query: `0` low, `1` high | Select/query active preset level. | `LEVEL HIGH` | 41, 52, 69 |
| `[STATe:]DYNamic {ON|OFF}` / `[STATe:]DYNamic?` | Query: `0` dynamic, `1` static as printed | Enable/query dynamic operation. | `DYN ON` | 41, 52, 70 |
| `[STATe:]CCR {AUTO|R2}` | Auto range or forced range II | Select CC current range behavior. | `CCR R2` | 41, 52, 71 |
| `[STATe:]POLAR {POS|NEG}` | Positive or negative display polarity | Set voltage-meter display polarity. | `POLAR POS` | 41, 52, 71 |

### 3.2 Test configuration, OCP, OPP, short, and BMS

| CMD | Range / Parameters | Function | Sample | Page |
|---|---|---|---|---:|
| `[PRESet:]TCONFIG {NORMAL|OCP|OPP|SHORT}` / query | Required test selection | Select/query test configuration. | `TCONFIG OCP` | 36, 39, 48, 50, 58 |
| `[PRESet:]OCP:START <NR2>` / query | A | Set/query OCP starting current. | `OCP:START 3` | 36, 39, 48, 50, 57-58 |
| `[PRESet:]OCP:STEP <NR2>` / query | A | Set/query OCP current increment. | `OCP:STEP 1` | 36, 48, 50, 58 |
| `[PRESet:]OCP:STOP <NR2>` / query | A | Set/query OCP stopping current. | `OCP:STOP 5` | 36, 48, 50, 58 |
| `[PRESet:]OPP:START <NR2>` / query | W | Set/query OPP starting power. | `OPP:START 20` | 36, 39, 48, 50, 58 |
| `[PRESet:]OPP:STEP <NR2>` / query | W | Set/query OPP power increment. | `OPP:STEP 5` | 36, 39, 48, 50, 58 |
| `[PRESet:]OPP:STOP <NR2>` / query | W | Set/query OPP stopping power. | `OPP:STOP 100` | 36, 39, 48, 50, 58 |
| `[PRESet:]VTH <NR2>` / `[PRESet:]VTH?` | V | Set/query minimum threshold voltage for OCP/OPP. | `VTH 0.6` | 36, 39, 48, 50, 58 |
| `[PRESet:]STIME <NR2>` / `[PRESet:]STIME?` | ms; `0` means continuous | Set/query short-circuit test time. | `STIME 500` | 36, 39, 48, 50, 59 |
| `[STATe:]SHORt {ON|OFF}` / `[STATe:]SHORt?` | Boolean | Control/query short-test state. | `SHORT ON` | 41, 52, 69 |
| `[STATe:]NGENABLE {ON|OFF}` | Boolean | Enable/disable NG limit checking. | `NGENABLE ON` | 41, 52 |
| `[STATe:]START` | None | Start selected OCP, OPP, or short test. | `START` | 41, 52, 71 |
| `[STATe:]STOP` | None | Stop active test. | `STOP` | 41, 52, 71 |
| `[STATe:]TESTING?` | `0` ended, `1` testing | Query test execution state. | `TESTING?` | 41, 52 |
| `OCP?` | Returns current | Read measured OCP trip/test current. | `OCP?` | 39, 64 |
| `OPP?` | Returns power | Read measured OPP trip/test power. | `OPP?` | 39, 64 |
| `[PRESet:]BMS {ON|OFF|1|0}` | Boolean | Enable/disable BMS test function. | `BMS ON` | 37, 49, 61 |
| `[PRESet:]BMS:STIME <NR2>` | 0.05-10 ms | Set BMS short time. | `BMS:STIME 1` | 37, 49, 61 |
| `[PRESet:]SHORT:ITH <NR2>` | A | Set BMS short-current threshold. | `SHORT:ITH 10` | 37, 49, 61 |
| `[PRESet:]OCP:ITH <NR2>` | A | Set BMS OCP current threshold. | `OCP:ITH 10` | 37, 49, 61 |
| `[PRESet:]OCP:TSTEP <NR2>` | 0.05-10 ms or 11-1000 ms, as documented | Set BMS OCP time step. | `OCP:TSTEP 1` | 37, 49, 61 |
| `[PRESet:]PROT:TIME?` | ms | Read BMS short/OCP protection time. | `PROT:TIME?` | 37, 49, 62 |
| `[PRESet:]PEAK:CURR?` | A | Read short-test peak current. | `PEAK:CURR?` | 37, 49, 62 |

### 3.3 Battery, pulse, surge, MPPT, and analog input

| CMD | Range / Parameters | Function | Sample | Page |
|---|---|---|---|---:|
| `[PRESet:]BATT:TYPE <n>` | `1-5` | Select battery test type. | `BATT:TYPE 1` | 36, 48, 59 |
| `[PRESet:]BATT:UVP <NR2>` | V | Set battery under-voltage protection. | `BATT:UVP 3.0` | 36, 48, 59 |
| `[PRESet:]BATT:TIME <n>` | 1-99999 s | Set battery test time. | `BATT:TIME 3600` | 36, 48, 59 |
| `[PRESet:]BATT:STEP <n>` | Type 3: 1-3; Types 4/5: 1-9 | Set number of battery steps. | `BATT:STEP 3` | 36, 48, 59 |
| `[PRESet:]BATT:CCH<n> <NR2>` | n=1-3 | Set Type-3 high current level. | `BATT:CCH1 2` | 48, 59 |
| `[PRESet:]BATT:CCL<n> <NR2>` | n=1-3 | Set Type-3 low current level. | `BATT:CCL1 1` | 36, 48, 60 |
| `[PRESet:]BATT:TH<n> <NR2>` | n=1-3; ms | Set Type-3 high time. | `BATT:TH1 100` | 36, 48, 60 |
| `[PRESet:]BATT:TL<n> <NR2>` | n=1-3; ms | Set Type-3 low time. | `BATT:TL1 100` | 37, 48, 60 |
| `[PRESet:]BATT:CYCLE<n> <NR1>` | n=1-3; cycle 1-2000 | Set Type-3 cycle count. | `BATT:CYCLE1 100` | 37, 48, 60 |
| `[PRESet:]BATT:CC<n> <NR2>` | n=0-9 | Set Type-4 current step. | `BATT:CC0 1` | 37, 49, 60 |
| `[PRESet:]BATT:CV<n> <NR2>` | n=0-9 | Set Type-5 voltage step. | `BATT:CV0 4.2` | 37, 49, 60 |
| `[PRESet:]BATT:DTIME<n> <NR1>` | n=1-9; 0-6000 s | Set Type-4/5 delta time. | `BATT:DTIME1 60` | 37, 49, 60 |
| `[PRESet:]BATT:REPEAT <n>` | 0-9999 | Set Type-4/5 repeat count. | `BATT:REPEAT 10` | 37, 49, 60 |
| `[PRESet:]BATT:TEST {ON|OFF}` | Start/stop | Control battery test. | `BATT:TEST ON` | 37, 49, 61 |
| `[PRESet:]PULSE:CC <NR2>` | A | Set pulse current. | `PULSE:CC 10` | 37, 49, 62 |
| `[PRESet:]PULSE:TIME <NR2>` | 0.001-16383 s | Set pulse duration. | `PULSE:TIME 0.1` | 37, 49, 62 |
| `[PRESet:]PULSE:REP <n>` | 0-255 | Set pulse repeat count. | `PULSE:REP 10` | 37-38, 49, 62 |
| `[PRESet:]PULSE {ON|OFF}` | Start/stop | Control pulse operation. | `PULSE ON` | 37-38, 49, 62 |
| `[PRESet:]PULSE:RESULT?` | `nTRIP` or `TRIP,<time>,<repeat>` | Read pulse-test result. | `PULSE:RESULT?` | 38, 49, 62 |
| `[PRESet:]SURGE:SURI <NR2>` / query | A | Set/query surge current. | `SURGE:SURI 10` | 38-40, 50, 66 |
| `[PRESet:]SURGE:NORI <NR2>` / query | A | Set/query normal current. | `SURGE:NORI 2` | 38-40, 50, 66 |
| `[PRESet:]SURGE:TIME <NR2>` / query | 10-1000 ms | Set/query surge time. | `SURGE:TIME 100` | 38-40, 50, 66 |
| `[PRESet:]SURGE:STEP <n>` / query | 1-5 | Set/query surge decrement step. | `SURGE:STEP 2` | 38-40, 50, 66-67 |
| `[PRESet:]SURGE {ON|OFF}` / query | Start/stop | Control/query surge test. | `SURGE ON` | 38-40, 50, 67 |
| `[PRESet:]EXT:AIN {ON|OFF}` | Boolean | Enable/disable external analog input. | `EXT:AIN ON` | 38, 49, 62 |
| `[PRESet:]CVBW <n>` | 1-4, slow to fast | Set CV bandwidth/speed. | `CVBW 2` | 38, 49, 63 |
| `[PRESet:]TURBO {ON|OFF}` | Boolean | Enable/disable turbo function. | `TURBO ON` | 38, 49, 63 |
| `[PRESet:]MPPT {ON|OFF}` | Start/stop | Control basic 331XG MPPT operation. | `MPPT ON` | 36, 48, 63-64 |
| `[PRESet:]MPPTIME <n>` / query | 1000-60000 ms | Set/query MPP record interval. | `MPPTIME 5000` | 36, 39, 48, 50, 63-64 |
| `[PRESet:]MPP?` | Returns V/I/P or `END` | Read recorded maximum-power-point data. | `MPP?` | 39, 50, 64 |

**MPPT limitation:** The manual states that the 3310G series does not support the later MPPT CC/CR/CV scan command group (`MPPT:MODE`, `MPPT:CC:*`, `MPPT:CR:*`, `MPPT:CV:*`, etc.). Those commands are therefore excluded.

### 3.4 Limits, status, measurement, memory, and mainframe

| CMD | Range / Parameters | Function | Sample | Page |
|---|---|---|---|---:|
| `[LIMit:]CURRent:{HIGH|LOW} <NR2>` / query; aliases `IH`/`IL` | A | Set/query current NG limits. | `IH 10` | 40, 51, 67 |
| `[LIMit:]POWer:{HIGH|LOW} <NR2>` / query; aliases `WH`/`WL` | W | Set/query power NG limits. | `WH 100` | 40, 51, 67 |
| `[LIMit:]VOLTage:{HIGH|LOW} <NR2>` / query; aliases `VH`/`VL` | V | Set/query voltage NG limits. | `VH 15` | 40, 51, 68 |
| `[LIMit:]{SVH|SVL} <NR2>` / query | V | Set/query short-test voltage limits. | `SVH 1` | 40, 51, 68 |
| `[STATe:]CLR` | None | Clear error and protection registers. | `CLR` | 41, 52, 70 |
| `[STATe:]ERRor?` | Error bit register | Query module errors. | `ERROR?` | 41, 52, 70 |
| `[STATe:]NG?` | `0` GO, `1` NG | Query NG result. | `NG?` | 41, 52, 70 |
| `[STATe:]PROTect?` | Protection bit register | Query OPP/OTP/OVP/OCP status. | `PROTECT?` | 41, 52, 70-71 |
| `MEASure:CURRent?` | A | Read load current. | `MEAS:CURR?` | 42, 53, 73 |
| `MEASure:VOLTage?` | V | Read load voltage. | `MEAS:VOLT?` | 42, 53, 73 |
| `MEASure:POWer?` | W | Read load power. | `MEAS:POW?` | 42, 53, 73 |
| `MEAS:VC?` | Returns `voltage,current` | Read voltage and current in one response. | `MEAS:VC?` | 42, 53, 74 |
| `[SYStem:]RECall <state>[,<bank>]` | state 1-10; bank 1-15 optional | Recall stored setup. | `RECALL 2,15` | 42, 53, 72 |
| `[SYStem:]STORe <state>[,<bank>]` | state 1-10; bank 1-15 optional | Store current setup. | `STORE 2,15` | 42, 53, 72-73 |
| `[SYStem:]REMOTE` | RS-232/USB/LAN | Enter remote control. | `REMOTE` | 42, 53, 73 |
| `[SYStem:]LOCAL` | RS-232/USB/LAN | Return to local control. | `LOCAL` | 42, 53, 73 |
| `[SYStem:]NAME?` | Returns model string | Identify installed module, `3315G`. | `NAME?` | 42, 53, 72-73 |
| `*RST` | None | Reset 330XG mainframe. | `*RST` | 42, 53, 73 |

### 3.5 Global and auto-sequence commands

| CMD | Range / Parameters | Function | Sample | Page |
|---|---|---|---|---:|
| `GLOBe:[STATe:]PRESet {ON|OFF|1|0}` | Boolean | Apply preset state globally. | `GLOB:PRES ON` | 42-43, 53 |
| `GLOBe:[STATe:]LOAD {ON|OFF|1|0}` | Boolean | Apply load state globally. | `GLOB:LOAD OFF` | 42-43, 53 |
| `GLOBe:[STATe:]MODE {CC|CR|CV|CP}` | Required mode | Apply operating mode globally. | `GLOB:MODE CC` | 42-43, 53 |
| `GLOBe:[STATe:]SHORt {ON|OFF|1|0}` | Boolean | Apply short state globally. | `GLOB:SHOR ON` | 42-43, 53 |
| `GLOBe:[STATe:]DYNamic {ON|OFF|1|0}` | Boolean | Apply dynamic state globally. | `GLOB:DYN ON` | 42-43, 53 |
| `GLOBe:[STATe:]LEVel {HIGH|LOW|1|0}` | Level | Apply active level globally. | `GLOB:LEV HIGH` | 42-43, 53 |
| `GLOBe:MEASure:CURRent?` | A | Read global current. | `GLOB:MEAS:CURR?` | 42-43, 53 |
| `GLOBe:MEASure:VOLTage?` | V | Read global voltage. | `GLOB:MEAS:VOLT?` | 42-43, 53 |
| `FILE <n>` | 1-9 | Select auto-sequence file. | `FILE 1` | 47 |
| `STEP <n>` | 1-16 | Select sequence step. | `STEP 1` | 47 |
| `TOTSTEP <n>` | 1-16 | Set total number of steps. | `TOTSTEP 8` | 47 |
| `SB <state>,<bank>` | state 1-10; bank 1-15 | Assign memory setup to the selected step. | `SB 1,3` | 47 |
| `T1 <NR2>` / `T2 <NR2>` | 0.1-9.9 s | Set execution and NG-check times. | `T1 0.1` | 47 |
| `SAVE` | None | Save selected sequence file. | `SAVE` | 47 |
| `REPEAT <n>` | 0-9999 | Set sequence repeat count. | `REPEAT 10` | 47 |
| `RUN F<n>` | n=1-9 | Run sequence; response `PASS` or `FAIL:<step>`. | `RUN F1` | 47 |

## 4. Excluded commands

The following manual command families are not listed because they are not supported by the 3315G according to the model columns or explicit notes:

- LED mode and LED-simulator commands: `VO`, `VD`, `RD`, `IO`, `RR`, `FREQ`, `DIM`, `DUTY`, `BW`, `AVG`, `LEDNO`
- `CHAN A|B`, because 3311G and 3315G are single-channel modules
- Later MPPT CC/CR/CV scanning commands: `MPPT:MODE`, `MPPT:CC:*`, `MPPT:CR:*`, `MPPT:CV:*`, `MPPT:SCAN:*`, `MPPT:PO:*`, `MPPT:SRATE`, and `MPPT:SCOUNT`
- Commands marked only for 331XF, 333XF, 334XF/G, or 3340XF/G

## 5. Notes

1. Values above module capability are documented as being clamped to the maximum supported value.
2. The 3315G limits used by the driver are 15 A, 60 V, and 75 W; the documented slew-rate unit is mA/us. Use `NAME?` to confirm that the installed module is `3315G` before applying these limits.
3. The manual's summary shows `FALL` without a numeric parameter in some rows, but its detailed description states that a numeric value is required. This reference follows the detailed description.
4. Always terminate commands with an accepted line terminator. Use semicolons only to combine commands on one line.
