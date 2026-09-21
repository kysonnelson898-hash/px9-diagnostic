
def test_spn_accepts_19_bit_number():
    from j1939.spn import J1939Spn

    spn = J1939Spn(
        number=0x7FFFF,
        start_bit=0,
        bit_length=8,
    )

    assert spn.number == 0x7FFFF
