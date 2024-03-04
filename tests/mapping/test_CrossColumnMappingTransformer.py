from collections import OrderedDict

import pandas as pd
import pytest
import test_aide as ta

import tests.test_data as d
from tests.mapping.test_BaseMappingTransformer import (
    BaseMappingTransformerInitTests,
    BaseMappingTransformerTransformTests,
    GenericFitTests,
    OtherBaseBehaviourTests,
)
from tubular.mapping import CrossColumnMappingTransformer


class TestInit(BaseMappingTransformerInitTests):
    """Tests for CrossColumnMappingTransformer.init()."""

    @classmethod
    def setup_class(cls):
        """Defines which transformer look up in conftest.py fixtures for inherited tests.
        setup_class is called by pytest at class level before all test methods are called."""
        cls.transformer_name = "CrossColumnMappingTransformer"

    def test_adjust_columns_non_string_error(self):
        """Test that an exception is raised if adjust_column is not a string."""
        with pytest.raises(
            TypeError,
            match="CrossColumnMappingTransformer: adjust_column should be a string",
        ):
            CrossColumnMappingTransformer(mappings={"a": {"a": 1}}, adjust_column=1)

    def test_mappings_not_ordered_dict_error(self):
        """Test that an exception is raised if mappings is not an ordered dict if more than 1 mapping is defined ."""
        with pytest.raises(
            TypeError,
            match="CrossColumnMappingTransformer: mappings should be an ordered dict for 'replace' mappings using multiple columns",
        ):
            CrossColumnMappingTransformer(
                mappings={"a": {"a": 1}, "b": {"b": 2}},
                adjust_column="c",
            )


class TestFit(GenericFitTests):
    """Generic tests for CrossColumnMappingTransformer.fit()"""

    @classmethod
    def setup_class(cls):
        cls.transformer_name = "CrossColumnMappingTransformer"


class TestTransform(BaseMappingTransformerTransformTests):
    """Tests for the transform method on CrossColumnMappingTransformer."""

    @classmethod
    def setup_class(cls):
        cls.transformer_name = "CrossColumnMappingTransformer"

    def expected_df_1():
        """Expected output for test_expected_output."""
        return pd.DataFrame(
            {"a": [1, 2, 3, 4, 5, 6], "b": ["aa", "bb", "cc", "dd", "ee", "ff"]},
        )

    def expected_df_2():
        """Expected output for test_non_specified_values_unchanged."""
        return pd.DataFrame(
            {"a": [1, 2, 3, 4, 5, 6], "b": ["aa", "bb", "cc", "d", "e", "f"]},
        )

    def expected_df_3():
        """Expected output for test_multiple_mappings_ordered_dict."""
        return pd.DataFrame(
            {
                "a": [4, 2, 2, 1, 3],
                "b": ["x", "z", "y", "x", "x"],
                "c": ["cc", "dd", "bb", "cc", "cc"],
            },
        )

    def test_adjust_col_not_in_x_error(self):
        """Test that an exception is raised if the adjust_column is not present in the dataframe."""
        df = d.create_df_1()

        mapping = {"a": {1: "aa", 2: "bb", 3: "cc", 4: "dd", 5: "ee", 6: "ff"}}

        x = CrossColumnMappingTransformer(mappings=mapping, adjust_column="c")

        with pytest.raises(
            ValueError,
            match="CrossColumnMappingTransformer: variable c is not in X",
        ):
            x.transform(df)

    @pytest.mark.parametrize(
        ("df", "expected"),
        ta.pandas.adjusted_dataframe_params(d.create_df_1(), expected_df_1()),
    )
    def test_expected_output(self, df, expected):
        """Test that transform is giving the expected output."""
        mapping = {"a": {1: "aa", 2: "bb", 3: "cc", 4: "dd", 5: "ee", 6: "ff"}}

        x = CrossColumnMappingTransformer(mappings=mapping, adjust_column="b")

        df_transformed = x.transform(df)

        ta.equality.assert_frame_equal_msg(
            actual=df_transformed,
            expected=expected,
            msg_tag="expected output from cross column mapping transformer",
        )

    @pytest.mark.parametrize(
        ("df", "expected"),
        ta.pandas.adjusted_dataframe_params(d.create_df_1(), expected_df_2()),
    )
    def test_non_specified_values_unchanged(self, df, expected):
        """Test that values not specified in mappings are left unchanged in transform."""
        mapping = {"a": {1: "aa", 2: "bb", 3: "cc"}}

        x = CrossColumnMappingTransformer(mappings=mapping, adjust_column="b")

        df_transformed = x.transform(df)

        ta.equality.assert_frame_equal_msg(
            actual=df_transformed,
            expected=expected,
            msg_tag="expected output from cross column mapping transformer",
        )

    @pytest.mark.parametrize(
        ("df", "expected"),
        ta.pandas.adjusted_dataframe_params(d.create_df_7(), expected_df_3()),
    )
    def test_multiple_mappings_ordered_dict(self, df, expected):
        """Test that mappings by multiple columns using an ordered dict gives the expected output in transform."""
        mapping = OrderedDict()

        mapping["a"] = {1: "aa", 2: "bb"}
        mapping["b"] = {"x": "cc", "z": "dd"}

        x = CrossColumnMappingTransformer(mappings=mapping, adjust_column="c")

        df_transformed = x.transform(df)

        ta.equality.assert_frame_equal_msg(
            actual=df_transformed,
            expected=expected,
            msg_tag="expected output from cross column mapping transformer",
        )

    def test_mappings_unchanged(self):
        """Test that mappings is unchanged in transform."""
        df = d.create_df_1()

        mapping = {"a": {1: "aa", 2: "bb", 3: "cc", 4: "dd", 5: "ee", 6: "ff"}}

        x = CrossColumnMappingTransformer(mappings=mapping, adjust_column="b")

        x.transform(df)

        ta.equality.assert_equal_dispatch(
            expected=mapping,
            actual=x.mappings,
            msg="CrossColumnMappingTransformer.transform has changed self.mappings unexpectedly",
        )


class TestOtherBaseBehaviour(OtherBaseBehaviourTests):
    """
    Class to run tests for BaseTransformerBehaviour outside the three standard methods.

    May need to overwite specific tests in this class if the tested transformer modifies this behaviour.
    """

    @classmethod
    def setup_class(cls):
        cls.transformer_name = "CrossColumnMappingTransformer"
