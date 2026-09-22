from __future__ import annotations

import argparse
import sys
from pathlib import Path

from photogrammetry_capture_research.experiments import (
    ExperimentError,
    create_manifest,
    write_comparison,
    write_experiment,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pcr", description="Photogrammetry capture research experiment tools"
    )
    commands = parser.add_subparsers(dest="command", required=True)
    create = commands.add_parser("create", help="Create an immutable experiment manifest")
    create.add_argument("--id", required=True, help="Lowercase kebab-case experiment ID")
    create.add_argument(
        "--baseline", type=Path, required=True, help="Full-data ReconCheck Quality Report"
    )
    create.add_argument(
        "--output", type=Path, default=Path("experiments"), help="Experiment output root"
    )
    create.add_argument("--strategy", choices=["stride", "random", "sector-removal"], required=True)
    create.add_argument("--every", type=int, help="Keep every Nth image for stride selection")
    create.add_argument("--count", type=int, help="Number of images for random selection")
    create.add_argument("--seed", type=int, help="Required fixed seed for random selection")
    create.add_argument("--sector", type=int, help="Sector 0–7 to remove")
    create.add_argument(
        "--scene", type=Path, help="ReconCheck scene manifest; required for sector removal"
    )
    create.add_argument("--hypothesis", default="", help="Condition-specific hypothesis")
    compare = commands.add_parser(
        "compare", help="Validate and compare a completed experiment Quality Report"
    )
    compare.add_argument("--experiment", type=Path, required=True, help="Experiment directory")
    compare.add_argument(
        "--quality-report",
        type=Path,
        required=True,
        help="ReconCheck report from the selected/derived images",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "create":
            manifest = create_manifest(
                experiment_id=args.id,
                baseline_path=args.baseline,
                strategy=args.strategy,
                every=args.every,
                count=args.count,
                seed=args.seed,
                sector=args.sector,
                scene_path=args.scene,
                hypothesis=args.hypothesis,
            )
            directory = write_experiment(manifest, args.output)
            print(f"Created experiment manifest: {directory / 'experiment-manifest.json'}")
            print(
                "Selected "
                f"{len(manifest['selection']['selected_image_ids'])} "
                f"of {len(manifest['source_images'])} images"
            )
        elif args.command == "compare":
            path = write_comparison(args.experiment, args.quality_report)
            print(f"Wrote comparison: {path}")
        return 0
    except ExperimentError as error:
        print(f"pcr: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
