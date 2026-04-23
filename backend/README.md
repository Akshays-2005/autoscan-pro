# AutoDoc Align - Flask Backend

## Setup
```bash
cd backend
pip install -r requirements.txt
python app.py
```

Runs on http://localhost:5000

## Endpoint
`POST /process-document`  (multipart/form-data, field `image`)
Returns: scanned JPEG, or JSON `{ "error": "..." }`

## Connecting from the frontend
Set `VITE_API_URL=http://localhost:5000` (or your deployed URL) in the frontend env.
