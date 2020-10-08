#test bad links
#test good links
#test empty string
#test error types
from validator import validate_url
import pytest


def test_bad_links():
    with pytest.raises(ValueError):
        assert validate_url('')#empty link
        assert validate_url('not_a_link')#random string
        assert validate_url('https://forums.spacebattles.com/threads/whatever-it-takes-lok-au-oc.883808/')#no reader path
        assert validate_url('http://forums.spacebattles.com/threads/whatever-it-takes-lok-au-oc.883808/reader')#bad scheme
        assert validate_url("https://forums.sufficientvelocity.com/threads/whatever-it-takes-lok-au-oc.883808/reader")#bad netloc

def test_good_links():
    good_link = "https://forums.spacebattles.com/threads/this-is-a-test-link.123456/reader"
    assert type(validate_url(good_link)) == str #returns a string
    assert validate_url(good_link) == good_link #returns the same link
    assert validate_url(good_link+'/') == good_link #removes trailing slash


