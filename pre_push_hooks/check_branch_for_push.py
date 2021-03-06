#
# Copyright 2019. Clumio, Inc.
#
# Follow the Google style guide, but with COLUMN_LIMIT=100.
# https://github.com/google/styleguide/blob/gh-pages/pyguide.md
# Indent is 4 spaces, no tabs.
# yapf --style='$GOPATH/src/cdf/yapf.yaml'

"""pre-push hook to limit pushes to specific branches."""
import argparse
import re
import sys
import os
from typing import AbstractSet
from typing import Optional
from typing import Sequence


def is_on_branch(
        patterns: AbstractSet[str] = frozenset(),
) -> bool:
    """Checks if the remote reference is in the list of allowed patterns"""
    print(os.environ['PRE_COMMIT_REMOTE_REF'])
    ref = os.environ['PRE_COMMIT_REMOTE_REF']
    if not ref:
        sys.exit(0)
    remote_ref = '/'.join(ref.strip().split('/')[2:])
    return not any(
        re.match(p, remote_ref) for p in patterns
    )

def main(argv: Optional[Sequence[str]] = None) -> int:
    """Reads the patterns from .pre-commit-config.yaml and 
    checks if the remote ref matches the pattern.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-p', '--pattern', action='append',
        help=(
            'regex pattern for branch name to allow pushes to, '
            'may be specified multiple times'
        ),
    )
    args = parser.parse_args(argv)

    patterns = frozenset(args.pattern or ())
    return int(is_on_branch(patterns))


if __name__ == '__main__':
    sys.exit(main())
