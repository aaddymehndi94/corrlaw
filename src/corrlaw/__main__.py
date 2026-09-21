"""Command-line entry points for reproducible research and saved explanations."""
import argparse
import json
import os
from pathlib import Path


def main():
    parser=argparse.ArgumentParser(description='CorrLaw symbolic-regression research')
    commands=parser.add_subparsers(dest='command',required=True)
    command=commands.add_parser('run',help='Run a declared finite-library, PySR or prior-control configuration')
    command.add_argument('--config',required=True)
    command.add_argument('--output',default=os.environ.get('CORRLAW_RESULT_DIR'))
    command.add_argument('--resume',action='store_true')
    explanation=commands.add_parser('explain',help='Render the first saved ambiguity witness, without hidden-error selection')
    explanation.add_argument('run')
    explanation.add_argument('--unit',required=True)
    explanation.add_argument('--budget',type=int,default=0)
    explanation.add_argument('--output',required=True)
    args=parser.parse_args()
    if not args.output:parser.error('--output or CORRLAW_RESULT_DIR is required')
    if args.command=='explain':
        from .explain import explain
        print(json.dumps(explain(args.run,args.unit,args.budget,args.output),indent=2))
        return
    engine=json.loads(Path(args.config).read_text()).get('engine')
    if engine=='finite_library':
        from .experiment import load_config,run
    elif engine=='pysr_feature_grammar':
        from .symbolic_experiment import load_config,run
    elif engine=='finite_library_prior_control':
        if args.resume:parser.error('prior controls use immutable new output directories; resume is not implemented')
        from .prior_experiment import run as run_prior
        run_prior(json.loads(Path(args.config).read_text()),args.output)
        return
    else:parser.error(f'unsupported research engine: {engine}')
    config=load_config(args.config)
    raise SystemExit(1 if run(config,args.output,args.resume) else 0)


if __name__=='__main__':main()
