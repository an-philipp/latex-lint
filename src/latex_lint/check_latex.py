import logging
from pathlib import Path
import re


logger = logging.getLogger("latex-lint")

class ValidationError(Exception):
    pass


def check_latex(document: Path) -> int:
    errors: int = 0
    logger.info(f"Check {document}")
    with open(document, 'r') as f:
        for i, line in enumerate(f):
            if line.startswith('%'):
                continue  # We can do whatever we want in comments, skip this line

            for label in re.findall(r"\\label{([^}]*)}", line):
                try:
                    check_label(label)
                except ValidationError as ex:
                    errors += 1
                    logger.error(f"(line {i+1}) found invalid label: {ex}")


            if re.search(r".*\\cite{([^}]*)}", line):
                try:
                    check_cite(line)
                except ValidationError as ex:
                    errors += 1
                    logger.error(f"(line {i+1}) found invalid citation: {ex}")


            if re.search(r".*\\ref{([^}]*)}", line):
                try:
                    check_ref(line)
                except ValidationError as ex:
                    errors += 1
                    logger.error(f"(line {i+1}) found invalid reference: {ex}")

    if errors:
        logger.error(f"{errors:02} errors in {document}")
    return errors

def check_ref(line: str) -> None:
    """
    Check that citation doesn't stand alone and that they are equipped with a protected space
    Also the label may contain :: as delimiters
    :param line: string to check
    :return:
    """

    accept = r"~\\ref\{[A-Za-z0-9_\-]+(?:::[A-Za-z0-9_\-]+)*\}"
    result = re.search(accept, line)
    if result:
        return
    raise ValidationError(f"Invalid reference: {line}")

def check_label(label: str) -> None:
    """
    make sure labels are in the form
    chapter::<chaptername>::<sectionname>::<subsectionname>
    """
    accept = r"(?:chapter|fig|tab|eq)::[a-z\-_]+(?:::[a-z_\-0-9]+){0,5}"
    result = re.match(accept, label)
    if result:
        return

    raise ValidationError(f'The label: {label} is not a valid label for chapters and sections, figures or tables')


def check_cite(line: str) -> None:
    """
    Check that citation don't stand alone and that they are equipped with a protected space
    :param line: string to check
    :return:
    """

    accept = r"~\\cite{[a-z0-9,-_ ]+}[?!., ]"

    result = re.search(accept, line)
    if result:
        return
    raise ValidationError(f"Invalid citation: {line}")


