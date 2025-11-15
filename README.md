# LinkedIn Leads Automation — API

This repository provides the backend API for the LinkedIn Leads Automation project. It handles OAuth with LinkedIn, stores leads and settings, exposes REST endpoints used by the React UI, and runs background processes for scraping/automation.

> Pairing UI: https://github.com/faaizazizpf/linkedIn-leads-automation-reactjs

## Table of contents
- Features
- Prerequisites
- Environment variables
- Installation
- Running locally
- Docker
- API overview
- OAuth (LinkedIn) flow
- Connecting the React UI
- Testing
- Troubleshooting
- Contributing
- License

## Features
- OAuth 2.0 authentication with LinkedIn
- Persisting and querying generated leads
- REST endpoints for leads, campaigns, and account settings
- Webhooks or polling support for background tasks
- JWT-based session/auth for UI and API requests

## Prerequisites
- Node.js (>= 16)
- npm or yarn
- MongoDB (local or managed like Atlas)
- LinkedIn Developer app (Client ID / Client Secret)

## Environment variables
Create a `.env` file in the project root (do not commit). Example variables:

PORT=4000
MONGO_URI=mongodb+srv://user:password@cluster0.mongodb.net/linkedInLeads?retryWrites=true&w=majority
JWT_SECRET=replace_with_strong_random_secret
LINKEDIN_CLIENT_ID=your_linkedin_client_id
LINKEDIN_CLIENT_SECRET=your_linkedin_client_secret
LINKEDIN_REDIRECT_URI=https://your-domain.com/api/auth/linkedin/callback
FRONTEND_URL=http://localhost:3000
NODE_ENV=development

Optional (for Docker / production):
LOG_LEVEL=info

## Installation
1. Clone the repo
   git clone https://github.com/faaizazizpf/linkedIn-leads-automation-api.git
   cd linkedIn-leads-automation-api

2. Install dependencies
   npm install
   # or
   yarn install

3. Create `.env` with required variables (see above).

## Running locally
Start the server:
npm run dev
# or
yarn dev

By default the API runs on `http://localhost:4000` (or the PORT in your .env). You can change the port in the .env.

## Docker
Build and run with Docker:
docker build -t linkedIn-leads-api .
docker run -e MONGO_URI="your_mongo_uri" -e JWT_SECRET="secret" -e LINKEDIN_CLIENT_ID="id" -e LINKEDIN_CLIENT_SECRET="secret" -p 4000:4000 linkedIn-leads-api

Or add a docker-compose.yml that wires Mongo and the API service.

## API overview (examples)
Note: adjust paths to match your implemented routes. These are examples to document expected endpoints.

Authentication:
- GET /api/auth/linkedin - Redirects to LinkedIn OAuth consent
- GET /api/auth/linkedin/callback?code=... - OAuth callback endpoint
- POST /api/auth/refresh - Exchange refresh token for new access

Leads:
- GET /api/leads - List leads (supports query params: page, limit, campaign)
- GET /api/leads/:id - Get lead details
- POST /api/leads - Create a lead (admin/manual ingestion)
- PUT /api/leads/:id - Update lead
- DELETE /api/leads/:id - Delete lead

Campaigns & Settings:
- GET /api/campaigns
- POST /api/campaigns
- GET /api/settings
- PUT /api/settings

Webhook / Background:
- POST /api/webhooks/linkedin - (Optional) endpoint for inbound webhook-style integration

Examples (curl):
curl -H "Authorization: Bearer <JWT>" http://localhost:4000/api/leads
curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer <JWT>" -d '{"name":"John Doe","profileUrl":"https://linkedin.com/in/johndoe"}' http://localhost:4000/api/leads

## OAuth (LinkedIn) flow
1. User clicks "Sign in with LinkedIn" in the front-end, which opens:
   GET /api/auth/linkedin (this redirects to LinkedIn's auth URL).
2. LinkedIn redirects back to: LINKEDIN_REDIRECT_URI with `code` parameter.
3. Backend exchanges `code` for an access token using LINKEDIN_CLIENT_ID and LINKEDIN_CLIENT_SECRET.
4. Backend stores tokens & issues its own JWT for sessions (JWT_SECRET).
5. Periodically refresh LinkedIn tokens if needed.

Important:
- Ensure LINKEDIN_REDIRECT_URI matches the redirect set in your LinkedIn app settings.
- Use secure storage for CLIENT_SECRET and JWT_SECRET.

## Connecting the React UI
The React UI (linkedIn-leads-automation-reactjs) should be configured to call this API. Example environment variables for the UI:
REACT_APP_API_URL=http://localhost:4000
REACT_APP_LINKEDIN_CLIENT_ID=your_linkedin_client_id
REACT_APP_REDIRECT_URI=http://localhost:4000/api/auth/linkedin/callback (or your deployed redirect)

The UI will call the `GET /api/auth/linkedin` endpoint to start OAuth and the API will handle the redirect flow.

## Testing
Add unit/integration tests using your preferred framework (Jest / Supertest).
Example:
npm test
# or
yarn test

## Troubleshooting
- 401 when calling API: verify JWT_SECRET matches what the UI uses (if signed client-side) and that tokens are being issued correctly.
- OAuth redirect mismatch: ensure LinkedIn app redirect URIs exactly match environment variable.
- Mongo connection issues: verify MONGO_URI and network/whitelist.

## Contributing
- Create an issue describing the change.
- Create a branch: git checkout -b feat/your-feature
- Open a PR with description and testing instructions.

## Security & Privacy
- If you have added your secrets, Do NOT commit secrets to source control.
- Use HTTPS in production.
- Comply with LinkedIn's API terms and user privacy expectations.
