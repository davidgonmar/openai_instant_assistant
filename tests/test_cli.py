from openai_instant_assistant.cli import get_file_paths
from unittest import mock
import os


topdir = os.path.join("path", "to", "test", "directory")
subdir = os.path.join("path", "to", "test", "directory", "subdirectory")


mocked_walk_result = [
    (topdir, ["subdirectory"], ["file1.txt", "file2.txt", "invalid.invalid_file_type"]),
    (
        subdir,
        [],
        [
            "file3.txt",
            "file4.txt",
            "file5.txt",
            "file6.md",
            "file7.md",
            "file8.md",
            "file9.md",
            "file10.md",
            "file11.md",
            "file12.md",
            "file13.md",
            "file14.md",
            "file15.md",
            "file16.md",
            "file17.md",
            "file18.md",
            "file19.md",
            "file20.md",
        ],
    ),
]


def mocked_getsize_function(path):
    dict = {
        "file1.txt": 1024 * 1024 * 1,  # 1MB
        "file2.txt": 1024 * 1024 * 2,  # 2MB
        "file3.txt": 1024 * 1024 * 3,  # 3MB
        "file4.txt": 1024 * 1024 * 4,  # 4MB
        "file5.txt": 1024 * 1024 * 5,  # 5MB
        "invalid.invalid_file_type": 1024 * 1024 * 1,  # 1MB
        "file6.md": 1024 * 1024 * 1,  # 1MB
    }
    return dict.get(os.path.basename(path), 1024 * 1024 * 1)


@mock.patch("os.walk")
@mock.patch("os.path.getsize")
def test_get_file_paths(mocked_getsize, mocked_walk):
    # Mock OS function calls
    mocked_walk.return_value = mocked_walk_result
    mocked_getsize.side_effect = mocked_getsize_function

    # Define test case
    test_directory = topdir
    test_extensions = [".txt", ".md"]
    test_max_number_files = 10
    test_max_file_size = 1024 * 1024 * 3  # 1MB

    # Run the function
    result = get_file_paths(
        test_directory, test_extensions, test_max_number_files, test_max_file_size
    )

    # There should be 10 files in the result, all with the correct extensions and under the specified size
    expected_output = [
        os.path.join("path", "to", "test", "directory", "file1.txt"),
        os.path.join("path", "to", "test", "directory", "file2.txt"),
        os.path.join("path", "to", "test", "directory", "subdirectory", "file3.txt"),
        os.path.join("path", "to", "test", "directory", "subdirectory", "file6.md"),
        os.path.join("path", "to", "test", "directory", "subdirectory", "file7.md"),
        os.path.join("path", "to", "test", "directory", "subdirectory", "file8.md"),
        os.path.join("path", "to", "test", "directory", "subdirectory", "file9.md"),
        os.path.join("path", "to", "test", "directory", "subdirectory", "file10.md"),
        os.path.join("path", "to", "test", "directory", "subdirectory", "file11.md"),
        os.path.join("path", "to", "test", "directory", "subdirectory", "file12.md"),
    ]
    assert result == expected_output
