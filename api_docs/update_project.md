#### Headers

-   `accept`: `application/json`
-   `Content-Type`: `multipart/form-data`

#### Path Parameters

-   **project_id**:
    -   **Description**: The unique identifier of the project to be updated.
    -   **Type**: String
    -   **Required**: Yes

#### Parameters

1.  **area_of_interest** (GeoJSON file, optional):
    
    -   **Description**: A file in `GeoJSON` format defining the updated area of interest for the project.
    -   **Type**: File (`application/json`)
    -   **Required**: No
2.  **data** (JSON):
    
    -   **Description**: A JSON object containing the updated project data. Fields are optional and will only update the provided values.
    -   **Type**: Text JSON (`application/json`)
    -   **Required**: Yes

#### `data` Field Schema (JSON Format)

```json
{
  "name": "string (maximum 32 characters, optional)",
  "date_range": { // (optional)
    "start": "YYYY-MM-DD ",
    "end": "YYYY-MM-DD "
  },
  "description": "string (optional)"
}

```

##### Field Descriptions:

-   **name**:
    
    -   **Type**: String
    -   **Maximum Length**: 32 characters
    -   **Description**: Updated project name.
-   **date_range**:
    
    -   **Type**: JSON object
    -   **Description**: Updated date range for the project.
    -   **Contains**:
        -   **start**: Project start date in `YYYY-MM-DD` format.
        -   **end**: Project end date in `YYYY-MM-DD` format (must be equal to or later than `start` if provided).
-   **description**:
    
    -   **Type**: String
    -   **Description**: Updated project description.

#### Example Request

```bash
curl -X 'PATCH' \
  'http://localhost:8000/v1/project/54ba7341-cf97-4792-82b9-d053ddd464d6' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'data={"name":"new name"}
  ```
