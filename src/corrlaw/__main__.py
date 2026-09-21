import argparse
import os
from .experiment import load_config, run


def main():
    parser = argparse.ArgumentParser(description='CorrLaw finite-library research pilot')
    commands = parser.add_subparsers(dest='command', required=True)
    command = commands.add_parser('run')
    command.add_argument('--config', required=True)
    command.add_argument('--output', default=os.environ.get('CORRLAW_RESULT_DIR'))
    command.add_argument('--resume', action='store_true')
    args = parser.parse_args()
    if not args.output:
        parser.error('--output or CORRLAW_RESULT_DIR is required')
    config = load_config(args.config)
    raise SystemExit(1 if run(config, args.output, args.resume) else 0)


if __name__ == '__main__':
    main()
