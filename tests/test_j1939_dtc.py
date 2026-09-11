import pytest

from j1939.diagnostics.dtc import J1939Dtc


def test_valid_j1939_dtc():
    dtc = J1939Dtc(spn=190, fmi=1, occurrence_count=2, source_address=0, active=True)
    assert dtc.spn == 190
    assert dtc.fmi == 1
    assert dtc.occurrence_count == 2
    assert dtc.source_address == 0
    assert dtc.active is True


def test_dtc_rejects_invalid_spn():
    with pytest.raises(ValueError, match="SPN"):
        J1939Dtc(spn=32768, fmi=1)


def test_dtc_rejects_invalid_fmi():
    with pytest.raises(ValueError, match="FMI"):
        J1939Dtc(spn=190, fmi=32)


def test_dtc_rejects_invalid_occurrence_count():
    with pytest.raises(ValueError, match="occurrence count"):
        J1939Dtc(spn=190, fmi=1, occurrence_count=128)


def test_dtc_rejects_invalid_source_address():
    with pytest.raises(ValueError, match="source address"):
        J1939Dtc(spn=190, fmi=1, source_address=256)
