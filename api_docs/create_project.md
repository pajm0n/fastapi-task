#### Headers

-   `accept`: `application/json`
-   `Content-Type`: `multipart/form-data`

#### Parameters

1.  **area_of_interest** (GeoJSON file):
    
    -   **Description**: A file in `GeoJSON` format defining the project's area of interest.
    -   **Type**: File (`application/json`)
    -   **Required**: Yes
2.  **data** (JSON):
    
    -   **Description**: A JSON object containing project data adhering to the following schema.
    -   **Type**: Text JSON (`application/json`)
    -   **Required**: Yes

#### `data` Field Schema (JSON Format)

```json
{
  "name": "string (maximum 32 characters)",
  "date_range": {
    "start": "YYYY-MM-DD",
    "end": "YYYY-MM-DD"
  },
  "description": "string (optional, default is empty)"
}

```

##### Field Descriptions:

-   **name**:
    
    -   **Type**: String
    -   **Maximum Length**: 32 characters
    -   **Description**: The project name (required).
-   **date_range**:
    
    -   **Type**: JSON object
    -   **Description**: The date range for the project.
    -   **Contains**:
        -   **start**: Project start date in `YYYY-MM-DD` format (required).
        -   **end**: Project end date in `YYYY-MM-DD` format (required, must be equal to or later than `start`).
-   **description**:
    
    -   **Type**: String
    -   **Description**: Project description (optional).
    -   **Default Value**: Empty string.

#### Example Request

```bash
curl -X 'POST' \
  'http://localhost:8000/v1/project' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'area_of_interest=@geojson.json;type=application/json' \
  -F 'data={"date_range":{"end":"2024-12-11","start":"2024-12-10"},"name":"Sample Project"}'

```

