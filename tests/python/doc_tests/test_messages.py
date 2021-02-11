from doc.messages import requiredFieldMissing, unknownValue

def test_RequiredFieldMissing_WhenHappyPath_ThenReturnsCorrect():
    msg = requiredFieldMissing("testfield")
    assert "testfield is required" in msg

def test_UnknownValue_WhenHappyPath_ThenReturnsCorrect():
    msg = unknownValue("testfield", "testvalue")
    assert "Unrecognized testfield" in msg
    assert "testvalue" in msg
