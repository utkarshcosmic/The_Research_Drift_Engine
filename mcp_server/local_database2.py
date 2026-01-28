from mcp.server.fastmcp import FastMCP
from pathlib import Path
from typing import Optional, List
import PyPDF2
from camelot import io as camelot_io

mcp = FastMCP("PDF Folder Server")

# Set your PDF folder path
PDF_FOLDER = "/Users/utkarsh_verma/Codes/VS_CODE/The_Research_Drift_Engine/papers"

@mcp.tool()
def extract_pdf_from_folder(filename: str) -> str:
    
    pdf_path = Path(PDF_FOLDER) / filename
    
    if not pdf_path.exists():
        return f"Error: {filename} not found in {PDF_FOLDER}"
    
    text = []
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        
        page_nums = range(len(reader.pages))
        
        for page_num in page_nums:
            page = reader.pages[page_num]
            text.append(page.extract_text())
    
    return "\n".join(text)

@mcp.tool()
def list_pdfs_in_folder() -> list:
    """List all PDF files in the configured folder."""
    pdf_files = [f.name for f in Path(PDF_FOLDER).glob("*.pdf")]
    return pdf_files

if __name__ == "__main__":
    mcp.run()  # Uses stdio transport by default


