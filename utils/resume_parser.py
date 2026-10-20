import streamlit as st
import tempfile
import os
from pathlib import Path
from pypdf import PdfReader
from docx import Document
import re

class ResumeParser:
    """Parse resume files and extract text."""
    
    def __init__(self):
        pass
    
    def parse_pdf(self, file_path):
        """Parse PDF file and extract text."""
        try:
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += (page.extract_text() or "") + "\n"
            return text.strip()
        except Exception as e:
            st.error(f"Error parsing PDF: {str(e)}")
            return None
    
    def parse_docx(self, file_path):
        """Parse DOCX file and extract text."""
        try:
            doc = Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text.strip()
        except Exception as e:
            st.error(f"Error parsing DOCX: {str(e)}")
            return None
    
    def parse_resume(self, uploaded_file):
        """Main parser - handles both PDF and DOCX."""
        try:
            # Save temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file_path = tmp_file.name
            
            # Parse based on file type
            if uploaded_file.name.lower().endswith('.pdf'):
                text = self.parse_pdf(tmp_file_path)
            elif uploaded_file.name.lower().endswith('.docx'):
                text = self.parse_docx(tmp_file_path)
            else:
                st.error("Unsupported file format. Please upload PDF or DOCX.")
                text = None
            
            # Clean up
            os.unlink(tmp_file_path)
            
            return text
            
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
            return None