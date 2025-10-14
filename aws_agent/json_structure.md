# Boto3 Documentation JSON Structure

## Overview

This JSON file contains a comprehensive scrape of the AWS Boto3 documentation, including all available services and their methods with full documentation.

## File Structure

```json
{
  "services": {
    "<ServiceName>": {
      "url": "<service_documentation_url>",
      "methods": {
        "<method_name>": {
          "url": "<method_documentation_url>",
          "title": "<method_title>",
          "description": "<method_description>",
          "syntax": "<code_syntax_example>",
          "parameters": [
            {
              "name": "<parameter_name>",
              "description": "<parameter_description>"
            }
          ],
          "returns": "<return_type_and_description>",
          "examples": ["<code_example_1>", "<code_example_2>"],
          "full_text": "<complete_documentation_text>"
        }
      }
    }
  }
}
```

## Schema Details

### Root Level
- **`services`** (object): Container for all AWS services

### Service Level
Each service is keyed by its display name (e.g., "S3", "EC2", "Lambda") and contains:
- **`url`** (string): Direct link to the service's documentation page
- **`methods`** (object): Collection of all methods available for this service

### Method Level
Each method is keyed by its name (e.g., "abort_multipart_upload", "create_bucket") and contains:

- **`url`** (string): Direct link to the method's documentation page
- **`title`** (string): The formatted title of the method
- **`description`** (string): Brief description of what the method does (usually the first paragraph)
- **`syntax`** (string): Code example showing the method signature and usage
- **`parameters`** (array): List of parameter objects, each with:
  - **`name`** (string): Parameter name
  - **`description`** (string): What the parameter does and its constraints
- **`returns`** (string): Description of the return type and what it contains
- **`examples`** (array of strings): Additional code examples beyond the syntax
- **`full_text`** (string): Complete unstructured text from the documentation page

## Example

```json
{
  "services": {
    "S3": {
      "url": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html",
      "methods": {
        "create_bucket": {
          "url": "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/create_bucket.html",
          "title": "create_bucket",
          "description": "Creates a new S3 bucket. To create a bucket, you must register with Amazon S3...",
          "syntax": "response = client.create_bucket(\n    Bucket='string',\n    CreateBucketConfiguration={...}\n)",
          "parameters": [
            {
              "name": "Bucket",
              "description": "(string) [REQUIRED] The name of the bucket to create."
            }
          ],
          "returns": "dict - Response Syntax with Location and other metadata",
          "examples": ["# Example 1\nbucket = s3.create_bucket(...)"],
          "full_text": "create_bucket\n\nCreates a new S3 bucket..."
        },
        "delete_bucket": {
          "url": "...",
          "title": "...",
          ...
        }
      }
    },
    "EC2": {
      "url": "...",
      "methods": {...}
    }
  }
}
```

## Usage

This JSON file can be used for:

1. **Building documentation search tools** - Full-text search across all AWS services
2. **Creating AI/ML training datasets** - Structured API documentation for model training
3. **Generating code completion tools** - Method signatures and parameter information
4. **Building internal wikis** - Offline access to Boto3 documentation
5. **API analysis** - Understanding AWS service coverage and capabilities

## Notes

- The scraper captures both structured data (parameters, syntax) and unstructured data (full_text)
- Some methods may have incomplete structured fields if the documentation format varies
- The `full_text` field always contains the complete documentation as a fallback
- Services may also include Paginators and Waiters in addition to Client methods
- File size can be very large (100MB+) when scraping all services and methods

## Maintenance

This JSON structure is based on the Boto3 documentation as of the scraping date. AWS regularly updates their services, so periodic re-scraping is recommended to keep documentation current.
