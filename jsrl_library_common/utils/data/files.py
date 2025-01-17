import os
import json
import uuid
import string
import tempfile

def get_random_name():
    """Generate a random name

    Returns:
        - string: the new name
    """
    return str(uuid.uuid4())


def get_file_content(filename,
                     mode='r'):
    """Get the content of file

    Args:
        - filename (string): the file name where the information will be extracted
        - mode (string): the read file mode

    Returns:
        - string: the file content
    """
    file = open(filename, mode)
    content = file.read()
    file.close()
    return content


def delete_file(filename):
    """Delete file

    Args:
        - filename (string): the file to delete name
    """
    os.remove(filename)


def save_file_content(filename,
                      content,
                      mode="w"):
    """Store the content into the filename

    Args:
        - filename (string): the name of file
        - content (string): the content to stored
        - mode (string): the stored mode
    """
    file = open(filename, mode)
    file.write(content)
    file.close()


def get_temp_dir():
    """Get the temporal folder path

    Returns:
        - string: the temporal folder path
    """
    return tempfile.gettempdir()


def get_temp_file_name_on_dir(dir_path):
    """Create a temporal file name into the directory

    Args:
        - dir_path (string): the directory path

    Returns:
        - string: the complete path of new temporal file
    """
    temp_file_name = get_random_name()
    return os.path.join(dir_path, temp_file_name)


def get_temp_file_name():
    """Get the complete path for new temporal file

    Retunrs:
        - string: the temporal file path
    """
    return get_temp_file_name_on_dir(get_temp_dir())


def export_to_json_file(data,
                        filename,
                        type_export='w'):
    """Export data to json file

    Args:
        - data (dict): the data to export
        - filename (string): the name of json file
        - type_export (string): the type of write to file. By default overwrite
    """
    json_string = json.dumps(data)
    export_file([json_string], f"{filename}.json", type_export)


def export_to_csv(data,
                  filename,
                  type_export='w',
                  delimiter=','):
    """Export data to csv file

    Args:
        - data (list[list|tuple]): the data to export
        - filename (string): the name of csv file
        - type_export (string): the type of write to file. By default overwrite
        - delimiter (char): the csv delimiter
    """
    data = [ f'{delimiter}'.join(row) for row in data ]
    export_file(data, f"{filename}.csv", type_export)


def export_file(data,
                filename,
                type_export='w'):
    """Export data to file

    Args:
        - data (list[string]): the data to export
        - filename (string): the name with extension of file to export
        - type_export (string): the type of write to file. By default overwrite
    """
    with open(f'{filename}', type_export) as file:
        for line in data:    
            file.write(line)
            file.write('\n')


def load_json_file(filename):
    """Load data from json file

    Args:
        - filename (string): the filename without the .json extension

    Returns:
        - dict|list: the data into the file
    """
    data = None
    with open(f'{filename}.json') as json_file:
        data = json.load(json_file)
    
    return data


def _get_value(field):
    if field is None:
        return ""
    try:
        return str(field).encode("ascii").decode("ascii")
    except UnicodeEncodeError:
        printable = set(string.printable)
        return "".join(filter(lambda x: x in printable, field)).encode("utf8").decode("utf8")
