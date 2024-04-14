import pytest
from contextlib import nullcontext as does_not_raise
from hamcrest import assert_that, has_length, all_of
from src.main import PasswordGen, argparse


class TestPasswordGen:
    @classmethod
    def setup_class(cls):
        pass

    def setup_method(self):
        args = argparse.Namespace(
            use_lowercase=False,
            use_uppercase=False,
            use_digits=False,
            use_specials=False,
            use_unique=False,
            length=8
        )
        self.pwg = PasswordGen(args=args)


    def test_not_empty(self):
        password = self.pwg.generate()
        assert bool(password)


    def test_generate_default(self):
        password = self.pwg.generate()

        assert all(c.islower() for c in password)

        assert_that(list(password), all_of(
                has_length(8),
                )
        )


    def test_generate_with_lower(self):
        self.pwg.args.use_lowercase = True

        password = self.pwg.generate()
        assert any(c.islower() for c in password)


    def test_generate_with_upper(self):
        self.pwg.args.use_uppercase = True

        password = self.pwg.generate()
        assert any(c.isupper() for c in password)


    def test_generate_with_digit(self):
        self.pwg.args.use_digits = True

        password = self.pwg.generate()
        assert any(c.isdigit() for c in password)


    def test_generate_with_special(self):
        self.pwg.args.use_specials = True

        password = self.pwg.generate()
        assert any(c in '!@#$%^&*()-=_+[]{}|;:,.<>?' for c in password)


    @pytest.mark.parametrize(
        "length, exp", 
        [
            (6, does_not_raise()), 
            (10, does_not_raise()), 
            (200, pytest.raises(ValueError))
        ]
    )
    def test_generate_unique(self, length, exp):
        self.pwg.args.use_unique = True
        self.pwg.args.length = length

        with exp:
            password = self.pwg.generate()
            assert len(password) == len(set(password))  


    @pytest.mark.parametrize(
        "length, lower, upper, digits, specials", 
        [
            (12, True, True, True, True)
        ]
    )
    def test_generate_custom(self, length, lower, upper, digits, specials):
        args = argparse.Namespace(
            use_lowercase=lower,
            use_uppercase=upper,
            use_digits=digits,
            use_specials=specials,
            use_unique=False,
            length=length
        )
        self.pwg.args=args
        password = self.pwg.generate()

        assert len(password) == length

        pwd_lower = [c.isupper() for c in password]
        if lower:
            assert any(pwd_lower) 
        else:
            assert all(not pwd_lower)
        
        pwd_upper = [c.isupper() for c in password]
        if upper:
            assert any(pwd_upper) 
        else:
            assert all(not pwd_upper)
        
        pwd_digit = [c.isdigit() for c in password]
        if digits:
            assert any(pwd_digit) 
        else:
            assert all(not pwd_digit)
        
        pwd_specials = [c in '!@#$%^&*()-=_+[]{}|;:,.<>?' for c in password]
        if specials:
            assert any(pwd_specials) 
        else:
            assert all(not pwd_specials)

