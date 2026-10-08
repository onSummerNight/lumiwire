"""Hand-built synthetic messages (demo spec). Test PANs only."""

# 0200: fields 2, 3, 4, 11, 35, 41
MSG_0200 = "".join([
    "30323030",                          # MTI "0200" (ASCII)
    "7020000020800000",                  # primary bitmap: bits 2,3,4,11,35,41
    "3136", "34313131313131313131313131313131",  # F2  llvar ASCII: len "16", "4111111111111111"
    "303030303030",                      # F3  "000000"
    "303030303030303031303030",          # F4  "000000001000"
    "000123",                            # F11 BCD "000123"
    "3238", "343131313131313131313131313131313d3235313231303130303030",  # F35 len "28", "4111111111111111=25121010000"
    "5445524d30303031",                  # F41 "TERM0001"
])
DECODED_0200 = {
    "mti": "0200",
    "fields": {2: "4111111111111111", 3: "000000", 4: "000000001000", 11: "000123",
               35: "4111111111111111=25121010000", 41: "TERM0001"},
}

# 0800: secondary bitmap, fields 11 and 70
MSG_0800 = "".join([
    "30383030",                          # MTI "0800" (ASCII)
    "8020000000000000",                  # primary bitmap: bit 1 (secondary present), bit 11
    "0400000000000000",                  # secondary bitmap: bit 70
    "000001",                            # F11 BCD "000001"
    "0001",                              # F70 BCD "001", left-padded to 2 bytes
])
DECODED_0800 = {"mti": "0800", "fields": {11: "000001", 70: "001"}}


def _swap(msg: str, old: str, new: str) -> str:
    assert msg.count(old) == 1, old
    return msg.replace(old, new)


# 0200 with field 39 added (bitmap bit 39, "00")
MSG_0200_F39 = _swap(_swap(MSG_0200, "7020000020800000", "7020000022800000"),
                     "5445524d30303031", "3030" + "5445524d30303031")

# Deliberately broken variants: (message, expected error substring)
BROKEN = {
    "truncated": (MSG_0200[:-4], "field 41"),
    "unknown_field_bit": (_swap(MSG_0200, "7020000020800000", "7820000020800000"),
                          "field 5: no entry in spec"),
    "bad_mti_version": (_swap(MSG_0200, "30323030", "39323030"), "version digit"),
    "bad_mti_nondigit": (_swap(MSG_0200, "30323030", "41323030"), "must be 4 digits"),
    "non_digit_in_n": (_swap(MSG_0200, "31313131" "303030303030" "303030", "31313131" "303041303030" "303030"),
                       "field 3 (Processing code): non-digit character 'A' in n field"),
    "bad_an_char": (_swap(MSG_0200_F39, "3030" "5445524d", "3021" "5445524d"),
                    "field 39 (Response code): non-alphanumeric character '!' in an field"),
    "bad_track_separator": (_swap(MSG_0200, "313d3235", "31583235"),
                            "field 35 (Track 2 data): invalid character in z field"),
}


# 2003 demo spec. 2100: fields 2, 3, 4, 11, 35, 41, 52 (binary), 55 (binary, llllvar)
MSG_2100 = "".join([
    "32313030",                          # MTI "2100" (ASCII)
    "7020000020801200",                  # primary bitmap: bits 2,3,4,11,35,41,52,55
    "3136", "34313131313131313131313131313131",  # F2  llvar ASCII: len "16", "4111111111111111"
    "303030303030",                      # F3  "000000"
    "303030303030303031303030",          # F4  "000000001000"
    "000123",                            # F11 BCD "000123"
    "3238", "343131313131313131313131313131313d3235313231303130303030",  # F35 len "28", track 2
    "5445524d30303031",                  # F41 "TERM0001"
    "0123456789abcdef",                  # F52 fixed, 8 raw bytes
    "30303034", "deadbeef",              # F55 llllvar: len "0004", 4 raw bytes
])
DECODED_2100 = {
    "mti": "2100",
    "fields": {2: "4111111111111111", 3: "000000", 4: "000000001000", 11: "000123",
               35: "4111111111111111=25121010000", 41: "TERM0001",
               52: "0123456789ABCDEF", 55: "DEADBEEF"},
}

# 2800: secondary bitmap, fields 11 and 70
MSG_2800 = "".join([
    "32383030",                          # MTI "2800" (ASCII)
    "8020000000000000",                  # primary bitmap: bit 1 (secondary present), bit 11
    "0400000000000000",                  # secondary bitmap: bit 70
    "000002",                            # F11 BCD "000002"
    "0001",                              # F70 BCD "001", left-padded to 2 bytes
])
DECODED_2800 = {"mti": "2800", "fields": {11: "000002", 70: "001"}}
