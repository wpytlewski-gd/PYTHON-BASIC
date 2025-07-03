"""
Create virtual environment and install Faker package only for this venv.
Write command line tool which will receive int as a first argument and one or more named arguments
 and generates defined number of dicts separated by new line.
Exec format:
`$python task_4.py NUMBER --FIELD=PROVIDER [--FIELD=PROVIDER...]`
where:
NUMBER - positive number of generated instances
FIELD - key used in generated dict
PROVIDER - name of Faker provider
Example:
`$python task_4.py 2 --fake-address=address --some_name=name`
{"some_name": "Chad Baird", "fake-address": "62323 Hobbs Green\nMaryshire, WY 48636"}
{"some_name": "Courtney Duncan", "fake-address": "8107 Nicole Orchard Suite 762\nJosephchester, WI 05981"}
"""

import argparse
import json
import sys
from unittest.mock import Mock, patch

from faker import Faker


def print_name_address(args: argparse.Namespace) -> None:
    fake = Faker()

    generated_dicts = []
    for _ in range(args.number):
        output_dict = {}

        for field, provider_name in args.field_providers:
            try:
                provider_method = getattr(fake, provider_name)
                output_dict[field] = provider_method()
            except AttributeError:
                print(
                    f"Error: Provider '{provider_name}' not found in Faker library. Skipping field '{field}'.",
                    file=sys.stderr,
                )
            except Exception as e:
                print(f"An unexpected error occurred with provider '{provider_name}': {e}", file=sys.stderr)

        if output_dict:
            generated_dicts.append(output_dict)

    for dict in generated_dicts:
        print(json.dumps(dict))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("number", type=int, help="The positive number of instances to generate.")
    try:
        known_args, unknown_args = parser.parse_known_args()
    except argparse.ArgumentError as e:
        print(f"Error: {e}")
        parser.print_help()
        sys.exit(1)

    if known_args.number <= 0:
        print("Error: NUMBER must be a positive integer.", file=sys.stderr)
        sys.exit(1)

    field_providers = []
    for arg in unknown_args:
        if arg.startswith("--") and "=" in arg:
            key, value = arg[2:].split("=", 1)
            field_providers.append((key, value))
        else:
            print(f"Warning: Ignoring malformed argument '{arg}'", file=sys.stderr)

    if not field_providers:
        print("Error: You must provide at least one --FIELD=PROVIDER argument.", file=sys.stderr)
        sys.exit(1)

    known_args.field_providers = field_providers

    print_name_address(known_args)

"""
Write test for print_name_address function
Use Mock for mocking args argument https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock
Example:
    >>> m = Mock()
    >>> m.method.return_value = 123
    >>> m.method()
    123
"""


@patch("task_4.Faker")
def test_prints_correct_json_output(mock_faker_class, capfd):
    mock_faker_instance = Mock()
    mock_faker_instance.name.return_value = "Pytest User"
    mock_faker_instance.address.return_value = "456 Fixture Ave"
    mock_faker_class.return_value = mock_faker_instance

    mock_args = Mock()
    mock_args.number = 1
    mock_args.field_providers = [("full_name", "name"), ("location", "address")]
    expected_dict = {"full_name": "Pytest User", "location": "456 Fixture Ave"}

    print_name_address(mock_args)

    captured = capfd.readouterr()
    output_lines = captured.out.strip().split("\n")

    assert len(output_lines) == 1
    assert json.loads(output_lines[0]) == expected_dict
    assert captured.err == ""


@patch("task_4.Faker")
def test_handles_invalid_provider(mock_faker_class, capsys):
    mock_faker_instance = Mock()
    bad_provider_mock = Mock(side_effect=AttributeError)
    mock_faker_instance.bad_provider = bad_provider_mock
    mock_faker_class.return_value = mock_faker_instance

    mock_args = Mock()
    mock_args.number = 1
    mock_args.field_providers = [("field", "bad_provider")]

    print_name_address(mock_args)

    captured = capsys.readouterr()
    expected_error = "Error: Provider 'bad_provider' not found in Faker library. Skipping field 'field'.\n"

    assert captured.err == expected_error
    assert captured.out == ""


@patch("task_4.Faker")
def test_prints_nothing_for_zero_count(mock_faker_class, capsys):
    mock_args = Mock()
    mock_args.number = 0
    mock_args.field_providers = [("name", "name")]

    print_name_address(mock_args)

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""
