"""Deterministic CLI for the Agent Work Model source."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

from awm import __version__
from awm.generate import check_generated, write_generated
from awm.lint import lint_model
from awm.loader import LoadError, load_model
from awm.paths import DEFAULT_GENERATED_DIR, DEFAULT_MODEL_DIR, DEFAULT_SCHEMA_DIR
from awm.validate import SchemaLoadError, load_schemas, validate_model


def _add_common(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--model-dir",
        type=Path,
        default=DEFAULT_MODEL_DIR,
        help="Canonical model directory (default: repository model/)",
    )
    parser.add_argument(
        "--schema-dir",
        type=Path,
        default=DEFAULT_SCHEMA_DIR,
        help="JSON Schema directory (default: repository schema/)",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="awm",
        description="Validate, lint, and generate the Agent Work Model.",
    )
    parser.add_argument("--version", action="version", version=f"awm {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    validate = sub.add_parser("validate", help="Validate the canonical source against JSON Schema 2020-12")
    _add_common(validate)

    lint = sub.add_parser("lint", help="Run semantic lint against the canonical source")
    _add_common(lint)

    generate = sub.add_parser("generate", help="Write generated glossary, reference, and normalized JSON")
    _add_common(generate)
    generate.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_GENERATED_DIR,
        help="Directory for generated artifacts (default: repository generated/)",
    )
    generate.add_argument(
        "--check",
        action="store_true",
        help="Detect generated drift without writing files",
    )

    check = sub.add_parser("check", help="Validate, lint, and detect generated drift without writing")
    _add_common(check)
    check.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_GENERATED_DIR,
        help="Directory of generated artifacts to compare",
    )
    return parser


def _print_issues(label: str, issues: Sequence[str], stream=sys.stderr) -> None:
    if not issues:
        return
    print(f"{label}: {len(issues)} issue(s)", file=stream)
    for item in issues:
        print(f"  {item}", file=stream)


def cmd_validate(args: argparse.Namespace) -> int:
    try:
        model = load_model(args.model_dir)
        schemas = load_schemas(args.schema_dir)
    except (LoadError, SchemaLoadError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    issues = validate_model(model, schemas)
    if issues:
        _print_issues("validate", [issue.format() for issue in issues])
        return 1
    print("validate: ok")
    return 0


def cmd_lint(args: argparse.Namespace) -> int:
    try:
        model = load_model(args.model_dir)
    except LoadError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    result = lint_model(model)
    errors = [issue.format() for issue in result.issues if issue.level == "error"]
    warnings = [issue.format() for issue in result.issues if issue.level != "error"]
    if warnings:
        _print_issues("lint warnings", warnings, stream=sys.stdout)
    if errors:
        _print_issues("lint", errors)
        return 1
    print("lint: ok")
    return 0


def cmd_generate(args: argparse.Namespace) -> int:
    try:
        model = load_model(args.model_dir)
    except LoadError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if args.check:
        drifts = check_generated(model, args.output_dir)
        if drifts:
            _print_issues("generate --check", drifts)
            return 1
        print("generate --check: ok")
        return 0
    written = write_generated(model, args.output_dir)
    for name in sorted(written):
        print(f"wrote {written[name]}")
    return 0


def cmd_check(args: argparse.Namespace) -> int:
    try:
        model = load_model(args.model_dir)
        schemas = load_schemas(args.schema_dir)
    except (LoadError, SchemaLoadError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    status = 0
    schema_issues = validate_model(model, schemas)
    if schema_issues:
        _print_issues("validate", [issue.format() for issue in schema_issues])
        status = 1
    else:
        print("validate: ok")

    lint_result = lint_model(model)
    errors = [issue.format() for issue in lint_result.issues if issue.level == "error"]
    warnings = [issue.format() for issue in lint_result.issues if issue.level != "error"]
    if warnings:
        _print_issues("lint warnings", warnings, stream=sys.stdout)
    if errors:
        _print_issues("lint", errors)
        status = 1
    else:
        print("lint: ok")

    drifts = check_generated(model, args.output_dir)
    if drifts:
        _print_issues("generate --check", drifts)
        status = 1
    else:
        print("generate --check: ok")
    return status


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    dispatch = {
        "validate": cmd_validate,
        "lint": cmd_lint,
        "generate": cmd_generate,
        "check": cmd_check,
    }
    return dispatch[args.command](args)
