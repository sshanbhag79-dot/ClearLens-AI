# BioFilter Technical Stack

## Core Technologies

### Frontend
-   **Streamlit**: Chosen for rapid prototyping and ease of use in a 24-hour hackathon context. Handles UI, camera input, and state.
    -   *Justification*: Allows building a functional data app in pure Python without complex JS frameworks.

### Backend
-   **FastAPI**: High-performance web framework for building APIs with Python 3.7+.
    -   *Justification*: Native async support (great for external API calls), automatic OpenAPI docs, type safety.

### AI & Logic Layer
-   **Google Gemini API**: The "Brain" of the operation.
    -   *Role*: Semantic analysis of ingredient lists against complex user queries (e.g., "Is 'casein' okay for a dairy allergy?").
    -   *Prompting Strategy*: Context-aware prompts injecting user profile and product ingredients.

### Data Sources
-   **Open Food Facts API**: Open database of food products.
    -   *Role*: resolving barcodes to ingredient lists and nutrition facts.
-   **OCR Fallback (Tesseract / Gemini Vision)**: For products not in the database.

## Development Tools
-   **Language**: Python 3.9+
-   **Package Manager**: `pip`
-   **Authentication**: None for MVP (Local session state).
-   **Testing**: `pytest`
-   **Version Control**: Git

## Libraries & Dependencies
-   `fastapi`
-   `uvicorn` (ASGI server)
-   `streamlit`
-   `google-generativeai` (Gemini SDK)
-   `requests` (HTTP client)
-   `python-dotenv` (Configuration)
