"""
This module provides the `GoogleSheetClient` class for interacting with
Google Sheets via the Google Sheets API.
"""

import os
from dataclasses import dataclass, field
from google.oauth2.service_account import Credentials
import gspread
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)
from google_sheet_client import logging
from google_sheet_client.config import (
    DEFAULT_SCOPE,
    RETRY_ATTEMPTS,
    RETRY_MIN_WAIT,
    RETRY_MAX_WAIT,
)


logger = logging.getLogger(__name__)


@dataclass
class GoogleSheetConfig:
    """
    Configuration class for GoogleSheetClient.
    Reads values from environment variables.
    """

    service_account_file: str = os.getenv(
        "SERVICE_ACCOUNT_FILE", "service-account.json"
    )
    scopes: list[str] = field(
        default_factory=lambda: os.getenv("SCOPES", DEFAULT_SCOPE).split(",")
    )


class GoogleSheetClient:  # pylint: disable=too-few-public-methods
    """
    Class defining GoogleSheetClient with logging and retries.
    """

    def __init__(self, config: GoogleSheetConfig | None = None) -> None:
        """
        Initialize the client with the configurations.
        """
        self.config = config or GoogleSheetConfig()

        try:
            self.credentials = Credentials.from_service_account_file(
                self.config.service_account_file, scopes=self.config.scopes
            )
            self.client = gspread.authorize(self.credentials)
            logger.info("Successfully authenticated with Google Sheets API.")
        except Exception as e:
            logger.error("Failed to authenticate with Google Sheets API: %s", e)
            raise

    @retry(
        retry=retry_if_exception_type(Exception),
        wait=wait_exponential(multiplier=1, min=RETRY_MIN_WAIT, max=RETRY_MAX_WAIT),
        stop=stop_after_attempt(RETRY_ATTEMPTS),
        reraise=True,
    )
    def get_data_from_google_sheet(
        self, google_sheet_name: str
    ) -> list[dict[str, int | float | str]] | None:
        """
        Retrieves data from a Google Sheet.
        Implements retries with exponential backoff in case of failures.
        """
        try:
            logger.info("Fetching data from Google Sheet: %s", google_sheet_name)
            sheet = self.client.open(google_sheet_name).sheet1
            data = sheet.get_all_records()
            return data
        except Exception as e:
            logger.error("Error while getting data from the Google Sheet: %s", e)
            raise
