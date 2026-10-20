import re
import json
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

class SkillExtractor:
    """Extract skills from resume text using LLM."""
    
    def __init__(self, groq_api_key):
        self.llm = ChatGroq(
            groq_api_key=groq_api_key,
            model="llama-3.3-70b-versatile",  # Naya model
            temperature=0.1,
            max_tokens=2000
        )
        
        self.prompt = PromptTemplate(
            input_variables=["resume_text"],
            template="""Analyze the following resume and extract ALL skills mentioned.
            
Resume:
{resume_text}

Extract skills in these categories:
1. Technical Skills (Programming languages, frameworks, tools, databases, cloud services)
2. Soft Skills (Communication, leadership, teamwork, problem-solving)
3. Domain Skills (Industry-specific knowledge)
4. Certifications (Any professional certifications)

Return in JSON format:
{{
    "technical_skills": ["skill1", "skill2"],
    "soft_skills": ["skill1", "skill2"],
    "domain_skills": ["skill1", "skill2"],
    "certifications": ["cert1", "cert2"]
}}
"""
        )
        
        self.llm_chain = self.prompt | self.llm
    
    def extract_skills(self, resume_text):
        """Extract skills from resume."""
        try:
            result = self.llm_chain.invoke({"resume_text": resume_text})
            
            if hasattr(result, 'content'):
                result_text = result.content
            else:
                result_text = str(result)
            
            result_text = result_text.strip()
            match = re.search(r'\{.*\}', result_text, re.DOTALL)
            if match:
                result_text = match.group(0)
            
            skills_dict = json.loads(result_text)
            return skills_dict
            
        except Exception as e:
            return self.extract_skills_fallback(resume_text)
    
    def extract_skills_fallback(self, resume_text):
        tech_skills = [
            'python', 'java', 'javascript', 'typescript', 'react', 'node', 'angular',
            'sql', 'mongodb', 'mysql', 'postgresql', 'aws', 'azure', 'gcp', 'docker',
            'kubernetes', 'machine learning', 'deep learning', 'nlp', 'computer vision',
            'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy', 'langchain',
            'llm', 'rag', 'fastapi', 'django', 'flask', 'git', 'linux', 'ci/cd'
        ]
        
        soft_skills = [
            'communication', 'leadership', 'teamwork', 'problem solving',
            'analytical', 'project management', 'time management', 'critical thinking'
        ]
        
        text_lower = resume_text.lower()
        
        found_tech = [skill for skill in tech_skills if skill in text_lower]
        found_soft = [skill for skill in soft_skills if skill in text_lower]
        
        return {
            "technical_skills": found_tech,
            "soft_skills": found_soft,
            "domain_skills": [],
            "certifications": []
        }