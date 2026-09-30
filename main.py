import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="AI Resume Tailoring Engine")

class TailorRequest(BaseModel):
    job_description: str
    master_resume_summary: str

class TailorResponse(BaseModel):
    missing_keywords: list[str]
    tailored_summary: str
    match_score: int

@app.post("/api/v1/tailor", response_model=TailorResponse)
def tailor_resume(payload: TailorRequest):
    if not payload.job_description or not payload.master_resume_summary:
        raise HTTPException(status_code=400, detail="Missing job description or summary.")
    
    # Core logic: Extract keywords and match score (mock implementation for quick push)
    jd_words = set(payload.job_description.lower().split())
    resume_words = set(payload.master_resume_summary.lower().split())
    
    missing = list(jd_words - resume_words)[:5]
    match_score = min(100, int((len(resume_words & jd_words) / max(1, len(jd_words))) * 100) + 40)
    
    tailored = f"{payload.master_resume_summary} Proficient in {', '.join(missing[:3]) if missing else 'required skills'}."
    
    return TailorResponse(
        missing_keywords=missing,
        tailored_summary=tailored,
        match_score=match_score
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
