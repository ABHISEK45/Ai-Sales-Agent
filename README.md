# AI Sales Agent

An AI-powered conversational sales agent for **Northstar One**, a residential real-estate project in Sector 79, Gurugram.

The agent is designed to handle natural customer conversations, answer project-related questions, progressively qualify leads, handle site-visit requests, maintain conversation context, and generate structured lead analytics.

## Project Overview

The Northstar AI Sales Agent acts as a conversational first point of contact for prospective customers.

Instead of forcing customers through a fixed questionnaire, the agent follows the conversation naturally and collects useful information progressively.

The agent can:

- Answer project and pricing questions
- Understand customer requirements
- Capture configuration and budget
- Understand purchase timeline and interest level
- Handle objections and uncertainty
- Support English, Hindi, and Hinglish conversations
- Suggest a site visit when purchase intent is strong
- Schedule a simulated site visit
- Handle unavailable booking slots
- Capture follow-up requirements
- Handle opt-out requests
- Escalate conversations when required
- Maintain conversation context
- Generate structured lead analytics


## Architecture

```text
                    ┌─────────────────────────┐
                    │        Frontend         │
                    │     HTML / CSS / JS     │
                    └────────────┬────────────┘
                                 │
                                 │ HTTP
                                 ▼
                    ┌─────────────────────────┐
                    │        FastAPI          │
                    │       /chat /health     │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │    Northstar Agent      │
                    │                         │
                    │  Gemini + System Prompt │
                    │       + Tool Calling    │
                    └───────┬─────────┬───────┘
                            │         │
                 ┌──────────┘         └───────────┐
                 ▼                                ▼
       ┌──────────────────┐             ┌──────────────────┐
       │    Lead State    │             │  Site Visit Tool │
       │     / Session    │             │   Mock Booking   │
       └────────┬─────────┘             └──────────────────┘
                │
                ▼
       ┌──────────────────┐
       │     Analytics    │
       │  Structured Lead │
       │     Insights     │
       └──────────────────┘
```


## Tech Stack

- **Python**
- **FastAPI** — backend API
- **Google Gemini API** — conversational reasoning and tool calling
- **Pydantic** — structured data models and validation
- **HTML / CSS / JavaScript** — frontend
- **pytest** — automated testing
- **python-dotenv** — environment variable management


## Project Structure

```text
northstar-ai-agent/
│
├── backend/
│   ├── __init__.py
│   ├── agent.py
│   ├── analytics.py
│   ├── main.py
│   ├── models.py
│   ├── prompts.py
│   └── tools.py
│
├── frontend/
│   ├── app.js
│   ├── index.html
│   └── style.css
│
├── tests/
│   ├── test_analytics.py
│   ├── test_models.py
│   └── test_tools.py
│
├── .env.example
├── .gitignore
├── pytest.ini
├── README.md
└── requirements.txt
```

### Backend Components

| File | Responsibility |
|---|---|
| `agent.py` | Gemini agent, conversation orchestration, tool execution, and session handling |
| `prompts.py` | System prompt and sales-agent behavioral rules |
| `tools.py` | Site-visit booking tool and mock availability |
| `models.py` | Lead state, session, request, and response models |
| `analytics.py` | Structured lead analytics generation |
| `main.py` | FastAPI application and API endpoints |

### Frontend Components

| File | Responsibility |
|---|---|
| `index.html` | Application interface |
| `style.css` | UI styling and responsive layout |
| `app.js` | Chat interaction and backend communication |


## Key Features

### 1. Natural Conversation

The agent is designed to answer the customer's current question before attempting qualification.

For example, if the customer asks:

> "What is the starting price?"

The agent answers the pricing question directly rather than immediately asking multiple qualification questions.


### 2. Progressive Lead Qualification

The agent collects lead information naturally throughout the conversation.

The lead state can contain:

- Name
- Preferred configuration
- Budget
- Purchase timeline
- Interest level
- Site-visit interest/status
- Site-visit date
- Site-visit time
- Follow-up requirement
- Preferred language
- Escalation requirement
- Opt-out status
- Conversation status

The agent avoids asking every qualification question upfront.

It asks the smallest useful question based on the current conversation.


### 3. Configuration and Budget Matching

The agent can understand customer requirements such as:

```text
"I'm looking for a 3 BHK."

"My budget is around 2 crore."
```

The information is captured into the structured lead state.

Example:

```json
{
  "configuration": "3 BHK",
  "budget": "around 2 crore",
  "interest_level": "high"
}
```


### 4. Site-Visit Booking

Site visits are handled through a dedicated function tool.

The agent only attempts to book a visit after both:

- Date
- Time

are available.

Example:

```text
Customer:
I'd like to visit this Saturday at 11 AM.

Agent:
Your site visit has been successfully scheduled for Saturday
at 11:00 AM.
```


### 5. Booking Availability Handling

The project currently uses a simulated booking system.

Available mock slots:

```text
11:00 AM
3:00 PM
```

If the requested time is unavailable, the booking tool returns a failure result and the agent can suggest another time.

This demonstrates both successful and unsuccessful tool execution.


### 6. Conversation Memory

Each conversation is associated with a `session_id`.

The application maintains:

- Gemini interaction context
- Structured lead information

This allows the agent to maintain context across multiple messages in the same session.

The current implementation uses an **in-memory session manager**.


### 7. Multilingual Conversation

The system prompt allows the agent to adapt naturally to:

- English
- Hindi
- Hinglish

The agent should respond in the language/style used by the customer where appropriate.


### 8. Customer Intent Handling

The agent is designed to handle different customer situations, including:

- Basic information requests
- Genuine purchase interest
- Budget discussion
- Configuration requirements
- Objections
- Customers who are only exploring
- Customers who are busy
- Customers who want to be contacted later
- Customers who do not want further communication
- Customers requiring human assistance


### 9. Site-Visit Recommendation Logic

A site visit should not be pushed after every customer message.

The agent can suggest a site visit when:

- The customer demonstrates clear interest
- The customer explicitly wants to visit
- The customer demonstrates stronger purchase intent
- A site visit naturally follows the conversation

A budget or configuration alone is treated as a **qualification signal**, not automatically as a reason to push a site visit.


## Lead State

Lead information is represented using a structured Pydantic model.

Example:

```json
{
  "name": null,
  "configuration": "3 BHK",
  "budget": "2 crore",
  "purchase_timeline": null,
  "interest_level": "high",
  "site_visit_status": null,
  "site_visit_date": null,
  "site_visit_time": null,
  "follow_up_required": false,
  "preferred_language": null,
  "escalation_required": false,
  "opted_out": false,
  "conversation_ended": false
}
```

This structured state is separate from the natural-language response shown to the customer.


## Analytics

The application includes a deterministic analytics layer that converts the structured lead state into an analytics object.

Tracked information includes:

- Configuration
- Budget
- Purchase timeline
- Interest level
- Site-visit status
- Site-visit date
- Site-visit time
- Follow-up requirement
- Preferred language
- Escalation requirement
- Opt-out status
- Conversation status

Example:

```json
{
  "configuration": "3 BHK",
  "budget": "2 crore",
  "purchase_timeline": null,
  "interest_level": "high",
  "site_visit_status": "booked",
  "site_visit_date": null,
  "site_visit_time": null,
  "follow_up_required": false,
  "preferred_language": null,
  "escalation_required": false,
  "opted_out": false,
  "conversation_ended": false
}
```

The analytics layer does not make another Gemini API call.


## API

### Health Check

```http
GET /health
```

Example:

```bash
curl http://127.0.0.1:8000/health
```

Response:

```json
{
  "status": "ok"
}
```


### Chat

```http
POST /chat
```

Request:

```json
{
  "session_id": "customer-001",
  "message": "I'm interested in a 3 BHK."
}
```

Response:

```json
{
  "response": "The 3 BHK at Northstar One starts at ₹1.75 crore onwards.",
  "lead_state": {
    "configuration": "3 BHK"
  },
  "analytics": {
    "configuration": "3 BHK"
  }
}
```


## Local Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd northstar-ai-agent
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

On Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=your_gemini_model
```

A `.env.example` file is included in the repository.

**Do not commit the `.env` file or expose the API key.**


## Running the Backend

Start the FastAPI server:

```bash
python -m uvicorn backend.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Health check:

```bash
curl http://127.0.0.1:8000/health
```


## Running the Frontend

Start the FastAPI backend first.

Then open:

```text
frontend/index.html
```

in a browser.

The frontend communicates with the FastAPI `/chat` endpoint.


## Testing

The project includes automated tests for deterministic application components.

Run:

```bash
python -m pytest
```

The test suite currently covers:

- Pydantic models
- Site-visit booking logic
- Booking availability/failure behavior
- Analytics generation

Example:

```text
5 passed
```

The Gemini-powered conversational flow is intentionally not part of the regular pytest suite so that automated testing does not unnecessarily consume Gemini API quota.


## Prompt Design

The system prompt is one of the core components of the application.

The prompt focuses on:

1. Answering the customer's current question first
2. Avoiding unnecessary sales pressure
3. Progressive lead qualification
4. Asking one useful question at a time
5. Maintaining conversation context
6. Supporting English, Hindi, and Hinglish
7. Handling objections naturally
8. Preventing unsupported claims
9. Using tools only when their conditions are satisfied
10. Transitioning toward a site visit when customer intent is strong

The prompt also distinguishes between **qualification** and **purchase intent**.

For example, a customer providing a budget does not automatically mean that the agent should push for a site visit.


## AI Tools Used

### Google Gemini

Gemini is used for:

- Natural-language understanding
- Conversational responses
- Context-aware reasoning
- Lead qualification decisions
- Function/tool calling

### AI-Assisted Development

AI assistance was used during development for:

- Prompt design and iteration
- Code generation and refinement
- Debugging
- Architecture discussion
- Test development
- UI development


## Assumptions

- Northstar One project information is provided through the system prompt.
- Pricing and project information are based on the information defined for this assignment.
- Site-visit booking is simulated using predefined availability.
- No real CRM or property-management system is connected.
- Sessions are stored in memory.
- The application is intended for assignment/demo purposes rather than production deployment.


## Known Limitations

### In-Memory Sessions

Conversation sessions are stored in memory and will be lost when the backend restarts.

A production implementation would use persistent storage such as PostgreSQL or Redis.

### Simulated Booking

Site-visit availability is currently simulated.

A production system would connect to a real calendar, CRM, or property-management system.

### No Authentication

The current application does not implement user authentication or authorization.

### Gemini API Quotas

The conversational functionality depends on the configured Gemini API account and its available quota/rate limits.

### Local Development

The current application is designed primarily for local execution and demonstration.


## Future Improvements

Potential production improvements include:

- Persistent database-backed sessions
- CRM integration
- Real-time property inventory
- Real site-visit availability
- Calendar integration
- Authentication and authorization
- Voice input/output
- Lead-management dashboard
- Production deployment
- Monitoring and observability
- More comprehensive integration tests


## Example Conversation

```text
Customer:
I'm looking for a 3 BHK in Gurugram.

Agent:
Northstar One in Sector 79, Gurugram offers 3 BHK apartments
starting at ₹1.75 crore onwards.

Customer:
My budget is around 2 crore.

Agent:
That fits well with the available 3 BHK options.
Are you looking to purchase in the near future?

Customer:
Yes, probably in the next few months.

Agent:
Would you like to schedule a site visit to explore the project?

Customer:
Yes, this Saturday at 11 AM.

Agent:
Your site visit has been successfully scheduled for Saturday
at 11:00 AM.
```


## Project Status

The current implementation includes:

- Conversational AI agent
- Structured lead capture
- Conversation memory
- Site-visit function calling
- Booking success/failure handling
- Customer intent handling
- Lead analytics
- FastAPI backend
- Web frontend
- Automated tests
- Environment configuration
- Documentation

The project is intended as an AI sales-agent demonstration for Northstar One.


## License

This project was developed as part of an AI sales-agent assignment and is intended for demonstration and evaluation purposes.
