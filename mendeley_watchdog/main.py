##
#   Copyright (c) 2021 Valentin Weber
#
#   This file is part of the software mendeley-watchdog.
#
#   The software is licensed under the European Union Public License
#   (EUPL) version 1.2 or later. You should have received a copy of
#   the english license text with the software. For your rights and
#   obligations under this license refer to the file LICENSE or visit
#   https://joinup.ec.europa.eu/community/eupl/og_page/eupl to view
#   official translations of the licence in another language of the EU.
##

"""Main Application module"""

import logging
import os
import sys
import time


class Watchdog:  # pylint: disable=too-few-public-methods
    """Monitors changes in last modification time for given file(s)"""

    def __init__(self, config: dict):

        self.bib_dir = config["bib_dir"]
        self.files = config["files"]
        self.interval = config.get("interval", 1)

        self.log = logging.getLogger("watchdog")
        self._last_modified_times = {}

    def run(self) -> None:
        """Check files until process is stopped manually"""

        while True:
            self._check_files()
            try:
                time.sleep(self.interval)
            except KeyboardInterrupt:
                self.log.info("Exiting Application")
                sys.exit()

    def _check_files(self) -> None:
        """Check last modified time and update target after change"""

        for source_file, dest in self.files:
            source = os.path.normpath(os.path.join(self.bib_dir, source_file))
            try:
                source_stat = os.stat(source)
            except OSError as exc:
                self.log.warning(exc)
                continue
            last_mtime = self._last_modified_times.get(source)
            if last_mtime is None or source_stat.st_mtime > last_mtime:
                self.log.info("%s changed", source)
                try:
                    self._overwrite(source, dest)
                    self._last_modified_times[source] = source_stat.st_mtime
                    self.log.info("mirrored contents to '%s'", dest)
                except OSError as exc:
                    self.log.warning("couldn't update %s, %s", dest, exc)

    def _overwrite(self, source, dest) -> None:
        """Write contents of source file to destination"""

        self.log.debug("reading contents of '%s'", source)
        with open(source, "rb") as source_file:
            source_contents = source_file.read()
        self.log.debug("writing contents to '%s'", dest)
        with open(dest, "wb") as dest_file:
            dest_file.write(source_contents)
