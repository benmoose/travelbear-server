from unittest.mock import Mock
import pytest

from .api_model import api_model


@pytest.fixture
def model():
    @api_model
    class Foo:
        __slots__ = ("foo", "bar")

        def get_validation_errors(self):
            errors = []
            if isinstance(self.foo, int) and isinstance(self.bar, int):
                if self.foo + self.bar == 10:
                    errors.append("foo and bar cannot sum to 10")
            return errors

    return Foo


def test_api_model_has_expected_fields(model):
    assert "__api_model__" in model.__dict__
    assert "_from_dict" in model.__dict__
    assert "from_dict" in model.__dict__
    assert "_from_db_model" in model.__dict__
    assert "from_db_model" in model.__dict__
    assert "get_validation_errors" in model.__dict__
    assert "_is_valid" in model.__dict__
    assert "is_valid" in model.__dict__

    assert model.__api_model__
    assert callable(model.get_validation_errors)


def test_post_init_called(model):
    mock = Mock()
    setattr(model, "__post_init__", mock)

    model()
    assert mock.call_count == 1
    model.from_dict({})
    assert mock.call_count == 2
    model.from_db_model({})
    assert mock.call_count == 3


def test_api_model_to_dict(model):
    assert model(1, 2).to_dict() == {"foo": 1, "bar": 2}
    assert model(1).to_dict() == {"foo": 1}
    assert model(bar=2).to_dict() == {"bar": 2}

    assert model(1).to_dict(keep_empty_fields=True) == {"foo": 1, "bar": None}
    assert model(bar=2).to_dict(keep_empty_fields=True) == {"foo": None, "bar": 2}


def test_api_model_from_dict(model):
    assert model.from_dict({"foo": 1, "bar": 2}).to_dict() == {"foo": 1, "bar": 2}


def test_is_valid(model):
    assert model(1, 2).is_valid

    assert not model(5, 5).is_valid
    assert model(5, 5).validation_errors == ["foo and bar cannot sum to 10"]

    assert not model.from_dict({"foo": 5, "bar": 5}).is_valid
    assert model.from_dict({"foo": 5, "bar": 5}).validation_errors == [
        "foo and bar cannot sum to 10"
    ]

    assert not model.from_db_model(model(5, 5)).is_valid
    assert model.from_db_model(model(5, 5)).validation_errors == [
        "foo and bar cannot sum to 10"
    ]
