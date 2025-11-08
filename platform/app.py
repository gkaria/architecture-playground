"""Learning Platform FastAPI application."""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

# Initialize FastAPI app
app = FastAPI(
    title="Architecture Patterns Playground",
    description="Learn software architecture by example",
    version="1.0.0"
)

# Set up templates and static files
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")


# Architecture patterns data
ARCHITECTURES = [
    {
        "id": "monolith",
        "name": "Monolithic Architecture",
        "description": "All components in a single deployment unit with shared database",
        "complexity": "Low",
        "status": "implemented",
        "when_to_use": [
            "Starting a new project with unclear requirements",
            "Small team or solo developer",
            "Simple, well-understood domain",
            "Fast iteration is priority"
        ],
        "pros": [
            "Simple to develop and test",
            "Easy deployment",
            "No network latency between components",
            "Straightforward debugging"
        ],
        "cons": [
            "Tight coupling",
            "Difficult to scale independently",
            "Large codebase becomes hard to manage",
            "Technology stack lock-in"
        ],
        "port": 8001,
        "color": "blue"
    },
    {
        "id": "modular-monolith",
        "name": "Modular Monolith",
        "description": "Single deployment with clear module boundaries and interfaces",
        "complexity": "Medium",
        "status": "coming_soon",
        "when_to_use": [
            "Growing application needs better organization",
            "Want monolith benefits with better structure",
            "Planning potential future microservices"
        ],
        "pros": [
            "Better code organization",
            "Easier to understand and maintain",
            "Can evolve to microservices",
            "Enforced boundaries"
        ],
        "cons": [
            "Requires discipline to maintain boundaries",
            "Still a single deployment unit",
            "Can't scale modules independently"
        ],
        "port": 8002,
        "color": "green"
    },
    {
        "id": "microservices",
        "name": "Microservices Architecture",
        "description": "Independent services with separate databases and deployment",
        "complexity": "High",
        "status": "coming_soon",
        "when_to_use": [
            "Large, complex applications",
            "Need independent scaling",
            "Different teams own different services",
            "Polyglot requirements"
        ],
        "pros": [
            "Independent deployment and scaling",
            "Technology diversity",
            "Team autonomy",
            "Fault isolation"
        ],
        "cons": [
            "Increased complexity",
            "Distributed system challenges",
            "Network latency",
            "Data consistency issues"
        ],
        "port": 8003,
        "color": "purple"
    },
    {
        "id": "event-driven",
        "name": "Event-Driven Architecture",
        "description": "Asynchronous communication through events and message queues",
        "complexity": "High",
        "status": "coming_soon",
        "when_to_use": [
            "High scalability requirements",
            "Loose coupling is critical",
            "Asynchronous processing needed",
            "Complex event workflows"
        ],
        "pros": [
            "Highly scalable",
            "Loose coupling",
            "Flexibility in processing",
            "Excellent for real-time systems"
        ],
        "cons": [
            "Complex debugging",
            "Eventual consistency",
            "Message ordering challenges",
            "Infrastructure overhead"
        ],
        "port": 8004,
        "color": "red"
    },
    {
        "id": "layered",
        "name": "Layered Architecture",
        "description": "Organized in horizontal layers (presentation, business, data)",
        "complexity": "Low",
        "status": "coming_soon",
        "when_to_use": [
            "Traditional enterprise applications",
            "Clear separation of concerns needed",
            "Team has expertise in layered approach"
        ],
        "pros": [
            "Well understood pattern",
            "Clear separation of concerns",
            "Easy to organize teams",
            "Testability"
        ],
        "cons": [
            "Can lead to monolithic structure",
            "Layer isolation can be inefficient",
            "Changes may ripple through layers"
        ],
        "port": 8005,
        "color": "yellow"
    },
    {
        "id": "service-based",
        "name": "Service-Based Architecture",
        "description": "Coarse-grained services with shared database",
        "complexity": "Medium",
        "status": "coming_soon",
        "when_to_use": [
            "Middle ground between monolith and microservices",
            "Domain-driven bounded contexts",
            "Some independent deployment needed"
        ],
        "pros": [
            "More practical than microservices",
            "Domain-driven design",
            "Partial independent deployment",
            "Less complex than microservices"
        ],
        "cons": [
            "Shared database challenges",
            "Service boundaries can be unclear",
            "Some coupling remains"
        ],
        "port": 8006,
        "color": "indigo"
    }
]


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render the homepage."""
    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "architectures": ARCHITECTURES
        }
    )


@app.get("/architecture/{arch_id}", response_class=HTMLResponse)
async def architecture_detail(request: Request, arch_id: str):
    """Render the architecture detail page."""
    architecture = next((a for a in ARCHITECTURES if a["id"] == arch_id), None)

    if not architecture:
        return templates.TemplateResponse(
            "404.html",
            {"request": request},
            status_code=404
        )

    return templates.TemplateResponse(
        "architecture_detail.html",
        {
            "request": request,
            "architecture": architecture
        }
    )


@app.get("/comparison", response_class=HTMLResponse)
async def comparison(request: Request):
    """Render the architecture comparison page."""
    return templates.TemplateResponse(
        "comparison.html",
        {
            "request": request,
            "architectures": ARCHITECTURES
        }
    )


@app.get("/calm/{arch_id}")
async def get_calm_spec(arch_id: str):
    """Get CALM specification for an architecture."""
    calm_spec_path = Path(__file__).parent.parent / "calm-specs" / arch_id / "architecture.json"

    if not calm_spec_path.exists():
        return {"error": "CALM specification not found"}

    import json
    with open(calm_spec_path) as f:
        return json.load(f)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
