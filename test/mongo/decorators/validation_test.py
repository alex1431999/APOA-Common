from unittest import TestCase
from bson import ObjectId

from common.mongo.decorators.validation import validate_id, parse_parameter


class ValidationTests(TestCase):
    pass


class ValidateIdTests(ValidationTests):
    def test_validate_id_object_id(self):
        @validate_id("_id")
        def test(_id):
            return _id

        _id = ObjectId()
        _id_converted = test(_id)

        self.assertEqual(_id_converted, _id, "Should have done nothing")

    def test_validate_id_string(self):
        @validate_id("_id")
        def test(_id):
            return _id

        _id = ObjectId()
        _id_converted = test(str(_id))

        self.assertEqual(_id_converted, _id, "Should have casted the id")

    def test_validate_id_invalid_param(self):
        @validate_id("invalid_param")
        def test(_id):
            return _id

        _id = "some random parameter"
        _id_converted = test(_id)

        self.assertEqual(_id_converted, _id, "Should have done nothing")


class ParseParameterTests(ValidationTests):
    def test_parse_parameter_str(self):
        target_parameter = "test"
        param_names = ["hello", "test"]
        args = [1, 2]

        arg, position = parse_parameter(target_parameter, param_names, args, str)

        self.assertEqual(type(arg), str, "The arg should have been parsed")
        self.assertEqual(position, 1, "The correct arg position should have been found")

    def test_parse_parameter_object_id(self):
        target_parameter = "test"
        param_names = ["hello", "test"]
        args = [str(ObjectId()), str(ObjectId())]

        arg, position = parse_parameter(target_parameter, param_names, args, ObjectId)

        self.assertEqual(type(arg), ObjectId, "The arg should have been parsed")
        self.assertEqual(position, 1, "The correct arg position should have been found")

    def test_parse_parameter_invalid_target(self):
        target_parameter = "not in the list"
        param_names = ["hello", "test"]
        args = [str(ObjectId()), str(ObjectId())]

        arg, position = parse_parameter(target_parameter, param_names, args, ObjectId)

        self.assertIsNone(arg, "No arg should have been transformed")
        self.assertIsNone(position, "No arg should have been found")

    def test_parse_parameter_no_params(self):
        target_parameter = "not in the list"
        param_names = []
        args = []

        arg, position = parse_parameter(target_parameter, param_names, args, ObjectId)

        self.assertIsNone(arg, "No arg should have been transformed")
        self.assertIsNone(position, "No arg should have been found")
