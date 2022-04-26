import argparse
import os
import string
import sys
import datetime


def convert_line_to_csv(line: string):
    result = ''
    inside_quote = False
    delimiters = ['"', '[', ']']
    for character in line:
        if character not in delimiters and character != ' ':
            result += character
        else:
            if character in delimiters:
                inside_quote = not inside_quote
                if character == '"':
                    result += character
            elif character == ' ':
                if inside_quote:
                    result += ' '
                else:
                    result += ','

    return result


def remove_first_two_lines(lines):
    result = ["sep=,\n","BucketOwner,Bucket,Time,RemoteIP,Requester,RequestId,Operation,Key,Request-URI,HttpStatus,ErrorCode,BytesSent,ObjectSize,TotalTime,Turn-AroundTime,Referrer,User-Agent,VersionId\n"]
    for i, line in enumerate(lines):
        if i != 0 and i != 1 and line is not None:
            result.append(convert_line_to_csv(line))
    return result


def read_lines(file_path: string):
    lines = []
    with open(file_path, 'r') as fp:
        lines = fp.readlines()
    return lines


def build_target_file_name(filepath: string):
    base_path = os.path.dirname(os.path.abspath(filepath))
    filename = os.path.basename(filepath)
    tmp_new_file_name = f'{filename}-{datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")}'
    new_file_name = f'{tmp_new_file_name}.csv'
    result = os.path.join(base_path, new_file_name)
    return result


def main(file_path: string, override_original_file: bool):
    result = read_lines(file_path)
    result = remove_first_two_lines(result)

    if override_original_file:
        try:
            os.remove(file_path)
        except OSError:
            print("$ Couldn't remove original file!")
        target_file = f'{file_path}.csv'
    else:
        target_file = build_target_file_name(file_path)
    print(f'$ Writing file to: {target_file}')
    with open(target_file, 'w') as fp:
        for line in result:
            fp.write(line)


def prompt_user_for_file_name():
    file_entered = False
    while not file_entered:
        result = input("$ Enter the path/prefix of your log file(s): ")
        if result:
            return result


def prepare_parser():
    my_parser = argparse.ArgumentParser(
        description='Bucket Logs converter (Athena Substitute): '
                    'This tool will convert the bucket log files to a csv format that can be used with csv tools (exp: Excel)',
        )

    my_parser.add_argument('-p', '--path',
                           metavar='path',
                           type=str,
                           help='The path to the bucket log file',
                           required=False
                           )

    my_parser.add_argument('--override',
                           metavar='override',
                           type=bool,
                           help='Override the same file instead of creating a new one (old file will be deleted and a new one created with the same name plus the csv file extention)',
                           required=False,
                           action=argparse.BooleanOptionalAction
                           )

    my_parser.add_argument('-s', '--similar',
                           metavar='similar',
                           type=bool,
                           help='Indicates that the specified path is a prefix and not the exact path to the file.',
                           required=False,
                           action=argparse.BooleanOptionalAction
                           )

    arguments = my_parser.parse_args()
    return arguments


if __name__ == '__main__':
    args = prepare_parser()

    input_path = args.path

    override = False
    if args.override:
        override = True

    scan_similar_files = False

    if args.similar:
        scan_similar_files = True

    if not input_path:
        input_path = prompt_user_for_file_name()

    if not scan_similar_files:
        if not os.path.exists(input_path):
            print('The path specified does not exist')
            sys.exit()
        if input_path.endswith(".csv"):
            print("$ Cannot convert a csv file. It's probably already converted")
            sys.exit()
        main(input_path, override)
    else:
        base_path = os.path.dirname(os.path.abspath(input_path))
        filename = os.path.basename(input_path)
        file_converted = False
        number_of_converted_files = 0
        for file in os.listdir(base_path):
            if file.startswith(filename) and not file.endswith(".csv"):
                file_converted = True
                current_file_path = os.path.join(base_path, file)
                print(f'$ Converting file: {current_file_path}')
                main(current_file_path, override)
                number_of_converted_files += 1

        if file_converted:
            print(f'$ Converted {number_of_converted_files} file(s)')
        else:
            print(f'$ No file converted using the prefix "{os.path.join(base_path, filename)}"')
