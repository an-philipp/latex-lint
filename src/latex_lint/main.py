import argparse
import logging
import os
from latex_lint.check_latex import check_latex

logging.basicConfig(
    format='%(asctime)s | %(name)s [%(levelname)s] %(message)s',
    level=logging.INFO
)

logger = logging.getLogger("latex-lint")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check latex files for common formatting errors like not using portectec "
                    "spaces on refs and citatations"
    )

    parser.add_argument("root_folder", help="path to root folder in which the to be checked files are placed."
                                            "Only .tex files are processed")
    args = parser.parse_args()
    total_errors: int = 0
    total_files: int = 0
    for root, _, files in os.walk(args.root_folder):
        for f in files:
            total_files += 1
            path = os.path.join(root, f)
            total_errors += check_latex(path)

    if not total_errors:
        logger.info(f"Checked {total_files:02} files. All checks passed")
        return 0
    else:
        logger.error(f"Checked {total_files:02} files. {total_errors:02} errors found")
        return 1



if __name__ == '__main__':
    main()
