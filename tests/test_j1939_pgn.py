from j1939.pgn import J1939Pgn


def test_pgn_reports_data_page():
    assert J1939Pgn(0x1F004).data_page == 1
    assert J1939Pgn(0x0F004).data_page == 0


def test_pgn_reports_pdu_format():
    assert J1939Pgn(0x00EF00).pdu_format == 0xEF
    assert J1939Pgn(0x00F004).pdu_format == 0xF0


def test_pgn_classifies_pdu1():
    pgn = J1939Pgn(0x00EF00)

    assert pgn.is_pdu1 is True
    assert pgn.is_pdu2 is False


def test_pgn_classifies_pdu2():
    pgn = J1939Pgn(0x00F004)

    assert pgn.is_pdu1 is False
    assert pgn.is_pdu2 is True
