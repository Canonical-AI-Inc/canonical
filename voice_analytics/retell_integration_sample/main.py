from fastapi import FastAPI, HTTPException, Request
import datetime
from canonicalai_service import CanonicalAIService
import uvicorn

app = FastAPI(title="Retell AI Webhook Processor")

# Initialize Canonical service
canonical = CanonicalAIService()

@app.post("/webhook/retell")
async def process_retell_webhook(request: Request):
    """
    Process incoming webhook data from Retell AI.
    Only processes call_analyzed events to avoid duplicates.
    """
    try:
        data = await request.json()
        
        # Only process call_analyzed events
        event_type = data.get('event')
        if event_type != 'call_analyzed':
            return {
                "status": "skipped",
                "message": f"Skipped {event_type} event"
            }
                    
        # Send to Canonical AI
        try:
            await canonical.forward_call_analyzed(data)
        except Exception as e:
            print(f"Error forwarding to Canonical AI: {str(e)}")
            # Continue processing even if Canonical fails
        
        
        print("\n====== RETELL WEBHOOK DATA ======")
        print("Timestamp:", datetime.now().isoformat())
        print("Event Type:", event_type)
        
        return {
            "status": "success",
            "message": "Webhook data processed",
        }
        
    except Exception as e:
        print(f"Error processing webhook: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing webhook data: {str(e)}"
        )

@app.get("/health")
async def health_check():
    """Simple health check endpoint."""
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)