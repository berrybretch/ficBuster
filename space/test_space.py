from scraper import Space
import pytest

link = "https://forums.spacebattles.com/threads/whatever-it-takes-lok-au-oc.883808/"


def test_validity():
    # on object creation with link.
    with pytest.raises(ValueError):
        assert Space("")
        assert Space("wrong_link")
    test_obj = Space(link)
    assert len(test_obj.data) == 5
    assert type(test_obj.data["oebps"]) == str
    assert type(test_obj.data["meta_inf"]) == str
    assert type(test_obj.data["uid"]) == str
    assert type(test_obj.data["threadmarks"]) == list
    assert type(test_obj.data["story"]) == dict
    del test_obj


def test_page_population():
    # on build
    test_obj = Space(link)
    test_obj._get_pages()
    assert len(test_obj.links) >= 1
    assert len(test_obj.data) == 8
    assert type(test_obj.data["lang"]) == str
    assert type(test_obj.data["docAuthor"]) == str
    assert type(test_obj.data["docTitle"]) == str
    assert len(test_obj.data["docAuthor"]) > 1
    assert len(test_obj.data["docTitle"]) > 1
    assert len(test_obj.data["lang"]) > 1


def test_run_population():
    test_obj = Space(link)
    test_obj.run()
    assert len(test_obj.data["story"].keys()) > 1
    for key in test_obj.data["story"].keys():
        assert len(test_obj.data["story"][key]) > 1
