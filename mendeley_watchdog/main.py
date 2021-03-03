"""Main entry point for mendeley-watchdog"""

import argparse  # noqa pylint: disable=unused-import
import logging
import os
import sys
import time


class MendeleyWatchdog:  # pylint: disable=too-few-public-methods
    """Application object"""

    def __init__(self, config: dict):

        self.bib_dir = config["bib_dir"]
        self.files = config["files"]
        self.interval = config.get("interval", 1)

        self.log = logging.getLogger("mendele-watchdog")
        self._last_modified_times = {}

    def run(self) -> None:
        """Check files until process is stopped manually"""

        while True:
            self._check_files()
            try:
                time.sleep(self.interval)
            except KeyboardInterrupt:
                print("exiting application")
                sys.exit()

    def _check_files(self) -> None:
        """Check last modified time and update target after change"""

        for source_file, dest in self.files:
            source = os.path.join(self.bib_dir, source_file)
            err = f"ERROR: {source_file}" + "{}"
            try:
                source_stat = os.stat(source)
            except OSError as exc:
                print(err.format(exc))
                continue
            last_mtime = self._last_modified_times.get(source)
            if last_mtime is None or source_stat.st_mtime > last_mtime:
                print(f"{source} changed")
                try:
                    self._overwrite(source, dest)
                    self._last_modified_times[source] = source_stat.st_mtime
                    print(f"updated {dest}")
                except OSError as exc:
                    print(err.format(f"couldn't update {dest}: {exc}"))

    def _overwrite(self, source, dest) -> None:  # pylint: disable=no-self-use
        """Write contents of source file to destination"""

        with open(source, "rb") as source_file:
            source_contents = source_file.read()
        with open(dest, "wb") as dest_file:
            dest_file.write(source_contents)


def main() -> None:
    """Main entry point for mendeley-watchdog"""

    default_path = os.path.join("p:", "books", "mendeley library", ".bib")
    path = os.getenv("MENDELEY_BIBTEX_DIR", default_path)
    latex_test_dir = os.path.expanduser("~/desktop/latex_template/resources")
    if path is None:
        raise ValueError("can't find bib file directory")

    config = {
        "interval": 1,
        "bib_dir": path,
        "files": [
            ("library.bib", os.path.join(latex_test_dir, "references.bib"))
        ]
    }
    observer = MendeleyWatchdog(config)
    observer.run()


if __name__ == "__main__":
    main()
