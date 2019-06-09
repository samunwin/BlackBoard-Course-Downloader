from blackboard import BlackBoardContent, BlackBoardClient, BlackBoardAttachment, BlackBoardEndPoints, BlackBoardCourse, \
    BlackBoardInstitute
import argparse
import sys
import json
import os
import getpass


def get_arguments():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument("-v", "--version", help="Displays Application Version", action="store_true")
    parser.add_argument("-g", "--gui", help="Use GUI instead of CLI", action="store_true")
    parser.add_argument("-m", "--mass-download", help="Download All Course Documents", action="store_true")
    parser.add_argument("-u", "--username", help="Username to Login With")
    parser.add_argument("-p", "--password", help="Password to Login With")
    parser.add_argument("-s", "--site", help="Base Website Where Institute Black Board is Located")
    parser.add_argument("-l", "--location", help="Local Path To Save Content", default='./')
    parser.add_argument("-c", "--course", help="Course ID to Download")
    parser.add_argument("-d", "--dump", help="Print/Dump All Course Data", action="store_true")
    parser.add_argument("-r", "--record", help="Create A Manifest For Downloaded Data", action="store_true",
                        default=True)
    parser.add_argument("-V", "--verbose", help="Print Program Runtime Information", action="store_true")
    parser.add_argument("-C", "--config", help="Location of Configuration File", default='./config.json')
    parser.add_argument("-i", "--ignore-input", help="Ignore Input at Runtime", action="store_true")
    return parser.parse_args()


def handle_arguments():
    args = get_arguments()
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    if args.version:
        print("Application Version: v{}".format("0.0.1"))
        sys.exit(0)

    config_content = {}
    if os.path.isfile(args.config):
        try:
            with open(args.config) as json_file:
                config_content = json.load(json_file)
        except IOError:
            print("Unable to Read File at Location: {}".format(args.config))
        except json.JSONDecodeError:
            print("Unable to Parse Configuration File: {}".format(args.config))

    # Command Line Arg -> Config File -> Input

    if args.username is None:
        possible_username = config_content.get('username', '')
        if not args.ignore_input:
            args.username = input("Enter Username [{}]: ".format(possible_username))
        if not args.username or not args.username.strip():
            if possible_username:
                args.username = possible_username
            else:
                print("No Username Supplied!")
                sys.exit(0)

    if args.password is None:
        possible_password = config_content.get('password', '')
        if not args.ignore_input:
            args.password = getpass.getpass("Enter Password{}: "
                                            .format(" [Config Password]" if possible_password else ""))
        if not args.password or not args.password.strip():
            if possible_password:
                args.password = possible_password
            else:
                print("No Password Supplied!")
                sys.exit(0)

    if args.site is None:
        possible_site = config_content.get('site', '')
        if not args.ignore_input:
            args.site = input("Enter Black Board Host Website [{} or 'c' to Search]: ".format(possible_site))
        if ((not args.site or not args.site.strip()) and not possible_site and not args.ignore_input) or \
                args.site == 'c':
            args.site = navigation(default=BlackBoardInstitute,
                                   options=BlackBoardInstitute.find(input("Institute Name: ")),
                                   attribute='name', sort=True).display_lms_host
            if args.site is None:
                print("No Site Supplied!")
                sys.exit(0)
        else:
            args.site = possible_site

    if args.location is None:
        pass

    if args.course is None:
        pass

    if args.mass_download:
        pass

    if args.record:
        pass

    if args.dump:
        pass

    # Run Actual Program
    if args.gui:
        # Insert GUI Function Here
        print("No GUI Currently Implemented")
        sys.exit(0)
    else:
        return main(args)


def main(args):
    bbc = BlackBoardClient(username=args.username, password=args.password, site=args.site)
    if bbc.login():
        course = navigation(default=BlackBoardCourse, options=bbc.courses(), attribute='name', sort=True)
        print(course.name)
    # save_config(args)
    return


def save_config(args):
    config = {
        'username': args.username,
        'password': args.password,
        'site': args.site
    }
    with open(args.config, 'w') as save:
        json.dump(config, save)


def navigation(**kwargs):
    # Handle kwargs
    options = kwargs.get('options', [])
    default = kwargs.get('default', object if not options else type(options[0]))
    input_text = kwargs.get('input', "Enter {} Number to Select ['c' to Exit]: ".format(default.__name__))
    attribute = kwargs.get('attribute', '__name__')
    sort = kwargs.get('sort', False)

    if sort:
        options = sorted(options, key=lambda element: getattr(element, attribute))
    if not options:
        print('No Options Present')
        return default()
    while True:
        for i in range(len(options)):
            print("[{}] {}".format(i + 1, getattr(options[i], attribute)))
        choice = input(input_text)
        if choice.isalpha():
            return default()
        try:
            choice = int(choice)
            if choice > len(options) or choice <= 0:
                raise TypeError
            return options[choice - 1]
        except TypeError:
            print("Invalid Selection")


if __name__ == "__main__":
    handle_arguments()
