import re
import json
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

class JobMatcher:
    """Match resume with job description."""
    
    def __init__(self, groq_api_key, model="openai/gpt-oss-120b"):
        self.llm = ChatGroq(
            groq_api_key=groq_api_key,
            model=model,
            temperature=0.2,
            max_tokens=4000
        )
        
        self.prompt = PromptTemplate(
            input_variables=["resume_text", "job_description"],
            template="""You are an AI career advisor. Analyze the following resume and job description.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Provide a detailed analysis:

1. Match Score (0-100):
2. Required Skills Missing:
3. Strengths:
4. Weaknesses:
5. Recommendations:

Return in JSON format:
{{
    "match_score": 85,
    "missing_skills": ["skill1", "skill2"],
    "strengths": ["strength1", "strength2"],
    "weaknesses": ["weakness1", "weakness2"],
    "recommendations": ["rec1", "rec2"],
    "summary": "Brief summary of fit"
}}
"""
        )
        
        self.llm_chain = self.prompt | self.llm
    
    def analyze_match(self, resume_text, job_description):
        """Analyze match between resume and job."""
        try:
            result = self.llm_chain.invoke({
                "resume_text": resume_text,
                "job_description": job_description
            })
            
            if hasattr(result, 'content'):
                result_text = result.content
            else:
                result_text = str(result)
            
            result_text = result_text.strip()
            match = re.search(r'\{.*\}', result_text, re.DOTALL)
            if match:
                result_text = match.group(0)
            
            return json.loads(result_text)
            
        except Exception as e:
            return {
                "error": str(e),
                "match_score": 0,
                "missing_skills": [],
                "strengths": [],
                "weaknesses": [],
                "recommendations": [],
                "summary": f"Analysis incomplete: {str(e)}"
            }