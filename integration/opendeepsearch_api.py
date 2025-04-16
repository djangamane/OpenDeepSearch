from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uvicorn
import os
from dotenv import load_dotenv
import asyncio
from opendeepsearch import OpenDeepSearchTool

# Load environment variables
load_dotenv()

# Initialize the FastAPI app
app = FastAPI(
    title="OpenDeepSearch PRD Generator",
    description="API for generating Product Requirement Documents (PRDs) using OpenDeepSearch",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize OpenDeepSearch tool
search_tool = OpenDeepSearchTool(
    model_name=os.getenv("LITELLM_SEARCH_MODEL_ID", os.getenv("LITELLM_MODEL_ID", "openrouter/google/gemini-2.0-flash-001")),
    reranker="jina",  # Use "infinity" for self-hosted option
    search_provider="serper",  # Use "searxng" for self-hosted search
)

# Ensure the tool is initialized
if not hasattr(search_tool, 'search_tool'):
    search_tool.setup()

# Define request models
class PRDRequest(BaseModel):
    query: str
    max_sources: int = 3
    pro_mode: bool = True

# Define response models
class PRDResponse(BaseModel):
    result: str
    sources: Optional[List[Dict[str, Any]]] = None

# Background task for warming up the model
@app.on_event("startup")
async def startup_event():
    # Warm up the model with a simple query
    try:
        prompt = "Generate a PRD for a simple to-do list application"
        search_tool.forward(construct_prd_prompt(prompt))
        print("OpenDeepSearch PRD generator initialized successfully")
    except Exception as e:
        print(f"Error initializing OpenDeepSearch tool: {e}")

# Helper function to construct PRD prompt
def construct_prd_prompt(query: str) -> str:
    return f"""
    Generate a comprehensive Product Requirements Document (PRD) for: {query}
    
    The PRD should be suitable for AI code generation and include:
    
    # {query} - Product Requirements Document
    
    ## Overview and Objectives
    [Provide a clear description of the product and its main goals]
    
    ## Target Users and User Stories
    [Define the target audience and key user stories]
    
    ## Functional Requirements
    [List all essential features and functionality in detail]
    
    ## Technical Requirements
    [Specify technologies, platforms, integrations, and technical constraints]
    
    ## User Interface and User Experience
    [Describe the UI/UX, including key screens, workflows, and design principles]
    
    ## Non-Functional Requirements
    [Include performance, scalability, security, and accessibility requirements]
    
    ## Implementation Phases
    [Outline development phases and priorities]
    
    ## Success Metrics and Acceptance Criteria
    [Define how to measure success and specific acceptance criteria]
    
    Make the PRD comprehensive, detailed, and immediately actionable for AI code generation.
    Include specific requirements rather than vague statements.
    """

# API endpoints
@app.get("/")
async def root():
    return {"message": "OpenDeepSearch PRD Generator is running"}

@app.post("/api/deep-research", response_model=PRDResponse)
async def generate_prd(request: PRDRequest):
    try:
        # Construct PRD prompt and use OpenDeepSearch
        prd_prompt = construct_prd_prompt(request.query)
        result = search_tool.forward(prd_prompt)
        
        return PRDResponse(
            result=result,
            sources=[]  # Placeholder for sources
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PRD generation error: {str(e)}")

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

# Run the server if the script is executed directly
if __name__ == "__main__":
    # Get port from environment or use default 8000
    port = int(os.getenv("PORT", 8000))
    
    # Run the server
    uvicorn.run("opendeepsearch_api:app", host="0.0.0.0", port=port) 