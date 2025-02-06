import pytest
from unittest.mock import patch, MagicMock
from google.auth.exceptions import DefaultCredentialsError
from google_sheet_client.client import (
    GoogleSheetClient,
    GoogleSheetConfig,
)

MODULE_PATH = "google_sheet_client.client"
CREDS_PATH = f"{MODULE_PATH}.Credentials.from_service_account_file"
GSPREAD_PATH = f"{MODULE_PATH}.gspread.authorize"
CLIENT_PATH = f"{MODULE_PATH}.GoogleSheetClient.client"


@pytest.fixture
@patch(CREDS_PATH)
@patch(GSPREAD_PATH)
def mock_google_sheet_client(mock_gspread, mock_creds):
    """
    Fixture to create a mock GoogleSheetClient instance.
    """
    mock_creds.return_value = MagicMock()
    mock_gspread.return_value = MagicMock()

    config = GoogleSheetConfig(service_account_file="test-service-account.json")
    return GoogleSheetClient(config)


@patch(CREDS_PATH, side_effect=DefaultCredentialsError("Failed to authenticate"))
def test_google_sheet_client_authentication_failure(mock_creds):
    """
    Test failure during authentication.
    """

    with pytest.raises(DefaultCredentialsError, match="Failed to authenticate"):
        GoogleSheetClient()


def test_google_sheet_client_initialization(mock_google_sheet_client):
    """
    Test successful initialization of GoogleSheetClient.
    """
    assert mock_google_sheet_client is not None
    assert mock_google_sheet_client.client is not None


@patch.object(GoogleSheetClient, "client", create=True)  # patch the client instance
def test_get_data_from_google_sheet_success(mock_client, mock_google_sheet_client):
    """
    Test fetching data successfully from a Google Sheet.
    """
    mock_sheet = MagicMock()
    mock_sheet.get_all_records.return_value = [{"name": "Napoléon", "age": 42}]

    mock_google_sheet_client.client = (
        mock_client  # explicitly set mock_client to the instance attribute
    )
    mock_client.open.return_value.sheet1 = mock_sheet

    data = mock_google_sheet_client.get_data_from_google_sheet("TestSheet")

    assert data == [{"name": "Napoléon", "age": 42}]
    mock_client.open.assert_called_once_with("TestSheet")


@patch.object(GoogleSheetClient, "client", create=True)
def test_get_data_from_google_sheet_api_failure(mock_client, mock_google_sheet_client):
    """
    Test failure when fetching data from a Google Sheet.
    """
    mock_google_sheet_client.client = mock_client
    mock_client.open.side_effect = Exception("Google API Error")

    with pytest.raises(Exception, match="Google API Error"):
        mock_google_sheet_client.get_data_from_google_sheet("TestSheet")


@patch.object(GoogleSheetClient, "client", create=True)
def test_get_data_from_google_sheet_invalid_sheet(
    mock_client, mock_google_sheet_client
):
    """
    Test handling of invalid Google Sheet name.
    """
    mock_google_sheet_client.client = mock_client
    mock_client.open.side_effect = Exception("Invalid Sheet Name")

    with pytest.raises(Exception, match="Invalid Sheet Name"):
        mock_google_sheet_client.get_data_from_google_sheet("NonExistentSheet")
