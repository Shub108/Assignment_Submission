from fastapi import FastAPI, Request, HTTPException, Response
import json
import database
import os

app = FastAPI()

database.init_db()

@app.post("/tests")
async def create_test(request: Request):
    try:
        body = await request.json()
    except Exception:
        return Response(content=json.dumps({"error": "Invalid JSON format"}), status_code=400)

    #  Manual validation 
    required_fields = ["test_id", "patient_id", "clinic_id", "test_type", "result"]
    for field in required_fields:
        if field not in body or not str(body[field]).strip():
            print(json.dumps({"endpoint": "POST /tests", "status": "failure", "reason": f"Missing field: {field}"}))
            raise HTTPException(status_code=400, detail=f"Field '{field}' is required and cannot be empty.")

    # database operation with transaction logic
    try:
        result = database.insert_test(body)
        
        if result == "EXISTS":
            print(json.dumps({"endpoint": "POST /tests", "status": "conflict", "id": body['test_id']}))
            return Response(content=json.dumps({"error": "Conflict: test_id already exists"}), status_code=409)
        
        print(json.dumps({"endpoint": "POST /tests", "status": "success", "id": body['test_id']}))
        return {"status": "success", "message": "Test recorded successfully"}

    except Exception as e:
        # Log failure reason
        print(json.dumps({"endpoint": "POST /tests", "status": "error", "reason": str(e), "id": body.get("test_id")}))
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/tests")
async def get_clinic_tests(clinic_id: str = None):
    # Handle missing query parameter
    if not clinic_id:
        raise HTTPException(status_code=400, detail="Missing query parameter: clinic_id")
    
    results = database.get_tests_by_clinic(clinic_id)
    
    # Handle empty result sets
    if not results:
        return {"clinic_id": clinic_id, "tests": [], "message": "No tests found for this clinic"}

    # Format the sql rows into a list of dicts
    formatted_results = []
    for r in results:
        formatted_results.append({
            "test_id": r[0], "patient_id": r[1], "clinic_id": r[2],
            "test_type": r[3], "result": r[4], "created_at": r[5]
        })

    return {"clinic_id": clinic_id, "count": len(formatted_results), "tests": formatted_results}