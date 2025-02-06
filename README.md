# GoogleSheetClient

GoogleSheetClient is a Python module for interacting with Google Sheets using the Google Sheets API. It supports authentication via a service account, retrieves sheet data, and includes retries with exponential backoff to handle API failures.

## Features
- Authenticate with Google Sheets API using a service account  
- Fetch data from Google Sheets with automatic retries  
- Handle API failures and errors gracefully  
- Uses environment variables for configuration  

## Installation

### Clone the Repository
```
git clone https://github.com/olivierbenard/google-sheet-client.git
cd google-sheet-client
```

### Install Poetry (if not already installed)
```
pip install poetry
```

### Install Dependencies
```
poetry install
```

## Configuration

### Set Up Your `.env` File
Create a `.env` file in the project root with the following variables:

```
# Google Service Account File (Path)
SERVICE_ACCOUNT_FILE=path/to/service-account.json
```

### Get Your Google Service Account JSON
1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Create a service account with Google Sheets API access.
3. Download the `.json` key file and set its path in `.env` (`SERVICE_ACCOUNT_FILE`).
4. Grant the Service Account (email) access to the Google Sheet.

## Usage

### Example: Fetch Data from a Google Sheet
```
from google_sheet_client.client import GoogleSheetClient

# Initialize the client
client = GoogleSheetClient()

# Fetch data from a sheet
data = client.get_data_from_google_sheet("MySheetName")
print(data)
```

### Expected Output
```
[
    {"name": "Napoléon", "age": 42},
    {"name": "De Gaulle", "age": 45}
]
```

## Error Handling

| Exception Type                | Cause                                  | Solution |
|--------------------------------|--------------------------------------|----------|
| `FileNotFoundError`            | Service account JSON file missing   | Verify file path in `.env` |
| `DefaultCredentialsError`      | Incorrect credentials format      | Regenerate JSON file in Google Cloud |
| `Exception: Google API Error`  | API request failure           | Check network connection, API quota |
| `Exception: Invalid Sheet Name`| Sheet name is incorrect     | Verify sheet name in Google Drive |

## Running Tests

### Install `pytest`
```
poetry add --dev pytest
```

### Run the Test Suite
```
poetry run pytest tests/ -v
```

## License
This project is licensed under the MIT License.

## Contributing
Contributions are welcome. To contribute:
1. Fork the repository.
2. Create a new feature branch (`git checkout -b feature-branch`).
3. Commit your changes and push the branch.
4. Submit a Pull Request (PR).

## Contact
**Olivier Bénard**  

* GitHub: [olivierbenard](https://github.com/olivierbenard)
* LinkedIn: [olivierbenard](https://www.linkedin.com/in/olivierbenard)
