from embroi_link.src.embrodery_obj import EmbroderyObj


def test_constructor():
    obj = EmbroderyObj()

    assert obj.cv_image == None
