"""
MoneyMentor - Data Loader
Handles loading and processing of financial documents (PDFs, text files)
"""
import fitz  # PyMuPDF
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'
)
logger = logging.getLogger(__name__)


class DataLoader:
    """
    Data loader for processing various document formats
    """
    
    def __init__(self, data_dir: str = "../data", output_dir: str = "./data/processed"):
        """
        Initialize data loader
        
        Args:
            data_dir: Directory containing source documents
            output_dir: Directory to save processed text files
        """
        self.data_dir = Path(data_dir)
        self.output_dir = Path(output_dir)
        
        # Create output directory if it doesn't exist
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def extract_text_from_pdf(self, file_path: Path) -> str:
        """
        Extract text from a PDF file using PyMuPDF
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            Extracted text as string
        """
        try:
            doc = fitz.open(file_path)
            text_content = []
            page_count = len(doc)
            
            for page_num, page in enumerate(doc, start=1):
                text = page.get_text()
                if text.strip():  # Only add non-empty pages
                    text_content.append(text)
            
            doc.close()
            
            full_text = "\n\n".join(text_content)
            logger.info(f"✅ Extracted {page_count} pages from {file_path.name}")
            
            return full_text
            
        except Exception as e:
            logger.error(f"❌ Error extracting PDF {file_path.name}: {e}")
            return ""
    
    def extract_text_from_txt(self, file_path: Path) -> str:
        """
        Read text from a .txt file
        
        Args:
            file_path: Path to text file
            
        Returns:
            File content as string
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            
            logger.info(f"✅ Loaded text file {file_path.name}")
            return text
            
        except Exception as e:
            logger.error(f"❌ Error reading text file {file_path.name}: {e}")
            return ""
    
    def save_processed_text(self, text: str, original_filename: str) -> Path:
        """
        Save extracted text to processed directory
        
        Args:
            text: Extracted text content
            original_filename: Original file name
            
        Returns:
            Path to saved file
        """
        # Create output filename (replace extension with .txt)
        output_filename = Path(original_filename).stem + ".txt"
        output_path = self.output_dir / output_filename
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(text)
            
            logger.info(f"💾 Saved processed text to {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"❌ Error saving processed text: {e}")
            return None
    
    def process_file(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """
        Process a single file (PDF or TXT)
        
        Args:
            file_path: Path to file
            
        Returns:
            Dictionary with file info and extracted text
        """
        if not file_path.exists():
            logger.error(f"❌ File not found: {file_path}")
            return None
        
        text = ""
        
        if file_path.suffix.lower() == '.pdf':
            text = self.extract_text_from_pdf(file_path)
        elif file_path.suffix.lower() == '.txt':
            text = self.extract_text_from_txt(file_path)
        else:
            logger.warning(f"⚠️  Unsupported file type: {file_path.name}")
            return None
        
        if not text.strip():
            logger.warning(f"⚠️  No text extracted from {file_path.name}")
            return None
        
        # Save processed text
        output_path = self.save_processed_text(text, file_path.name)
        
        return {
            "filename": file_path.name,
            "file_path": str(file_path),
            "text": text,
            "output_path": str(output_path) if output_path else None,
            "char_count": len(text),
            "word_count": len(text.split())
        }
    
    def process_all_files(self) -> List[Dict[str, Any]]:
        """
        Process all PDF and TXT files in the data directory
        
        Returns:
            List of processed file information
        """
        if not self.data_dir.exists():
            logger.error(f"❌ Data directory not found: {self.data_dir}")
            return []
        
        # Find all PDF and TXT files
        pdf_files = list(self.data_dir.glob("*.pdf"))
        txt_files = list(self.data_dir.glob("*.txt"))
        all_files = pdf_files + txt_files
        
        if not all_files:
            logger.warning(f"⚠️  No PDF or TXT files found in {self.data_dir}")
            return []
        
        logger.info(f"\n📂 Found {len(all_files)} file(s) to process:")
        logger.info(f"   - {len(pdf_files)} PDF file(s)")
        logger.info(f"   - {len(txt_files)} TXT file(s)\n")
        
        results = []
        for file_path in all_files:
            logger.info(f"Processing: {file_path.name}")
            result = self.process_file(file_path)
            if result:
                results.append(result)
            logger.info("")  # Blank line for readability
        
        logger.info(f"✨ Processing complete! {len(results)}/{len(all_files)} files processed successfully.\n")
        
        # Print summary
        if results:
            logger.info("📊 Summary:")
            total_chars = sum(r['char_count'] for r in results)
            total_words = sum(r['word_count'] for r in results)
            logger.info(f"   Total characters: {total_chars:,}")
            logger.info(f"   Total words: {total_words:,}")
            logger.info(f"   Output directory: {self.output_dir.absolute()}")
        
        return results
    
    # Legacy methods for compatibility (can be used later for chunking)
    def load_pdf(self, file_path: str) -> List[Dict[str, Any]]:
        """Legacy method - wrapper around process_file"""
        result = self.process_file(Path(file_path))
        return [result] if result else []
    
    def load_text(self, file_path: str) -> List[Dict[str, Any]]:
        """Legacy method - wrapper around process_file"""
        result = self.process_file(Path(file_path))
        return [result] if result else []
    
    def load_all_documents(self) -> List[Dict[str, Any]]:
        """Legacy method - wrapper around process_all_files"""
        return self.process_all_files()


if __name__ == "__main__":
    """
    CLI entrypoint for data extraction
    Run: python data_loader.py
    """
    print("=" * 60)
    print("MoneyMentor - Data Extraction Tool")
    print("=" * 60)
    
    # Initialize loader
    loader = DataLoader(data_dir="../data", output_dir="./data/processed")
    
    # Process all files
    results = loader.process_all_files()
    
    if results:
        print(f"\n✅ Successfully processed {len(results)} file(s)!")
        print(f"📁 Check output at: {loader.output_dir.absolute()}")
    else:
        print("\n⚠️  No files were processed.")
    
    print("=" * 60)

