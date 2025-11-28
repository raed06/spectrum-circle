"""
Data Collection and Structuring Module

This module provides the FinetuningDataCollector class, designed to collect 
and format autism-specific training data. The data is structured into the 
JSONL format required for fine-tuning large language models like Gemini.
"""

from typing import List, Dict
import json
from pathlib import Path
from datetime import datetime
from loguru import logger

class FinetuningDataCollector:
    """
    Manages the collection and formatting of data for Gemini fine-tuning.

    It collects structured examples (input, output, category, metadata) and 
    saves them into two files:
    1. A simplified JSONL file (for direct model training).
    2. A full JSON file (for archival and analysis, including metadata).

    Attributes:
        output_dir (Path): The directory where the dataset files will be saved.
        examples (List[Dict]): The internal list of collected training examples.
    """
    
    def __init__(self, output_dir: str = "./data/training") -> None:
        """
        Initializes the collector and ensures the output directory exists.
        
        Args:
            output_dir (str): Path to the directory for saving the dataset.
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.examples: List[Dict] = []
        
        logger.info(f"DataCollector initialized. Output directory: {self.output_dir.resolve()}")
    
    def add_example(
        self,
        input_text: str,
        output_text: str,
        category: str,
        metadata: Dict = None
    ) -> None:
        """
        Adds a single structured training example to the internal collection list.
        
        Args:
            input_text (str): The user query, prompt, or context provided to the model.
            output_text (str): The desired, high-quality AI response or instruction fulfillment.
            category (str): The thematic category (e.g., 'sensory', 'social', 'communication') 
                            for easier dataset analysis.
            metadata (Dict, optional): Additional tracking information (e.g., source URL, 
                                     author) related to the example. Defaults to None.
        """
        example = {
            'text_input': input_text,
            'output': output_text,
            'category': category,
            'metadata': metadata or {},
            'added_at': datetime.now().isoformat()
        }
        
        self.examples.append(example)
    
    def save_dataset(self, filename: str = "finetuning_dataset.jsonl") -> Path:
        """
        Saves the collected examples to disk in the required format.
        
        Saves two files:
        1. JSONL (Simplified: 'text_input' and 'output' only) for Gemini training.
        2. JSON (Full: includes 'category' and 'metadata') for reference.
        
        Args:
            filename (str): The base filename for the JSONL output.
        
        Returns:
            Path: The full path to the saved JSONL file.
        """
        output_path = self.output_dir / filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            for example in self.examples:
                formatted = {
                    'text_input': example['text_input'],
                    'output': example['output']
                }
                f.write(json.dumps(formatted) + '\n')
        
        logger.info(f"Saved {len(self.examples)} examples to {output_path.name}")
        
        metadata_path = self.output_dir / filename.replace('.jsonl', '_full.json')
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(self.examples, f, indent=2)
        
        logger.info(f"Saved full dataset archive to {metadata_path.name}")

        return output_path
    
    def get_statistics(self) -> Dict:
        """
        Calculates and returns key statistics about the collected dataset.

        Returns:
            Dict: A dictionary containing:
                - 'total_examples': Total number of records.
                - 'categories': Count of examples per category.
                - 'avg_input_length': Average character count of 'text_input'.
                - 'avg_output_length': Average character count of 'output'.
        """
        if not self.examples:
            return {
                'total_examples': 0, 
                'categories': {}, 
                'avg_input_length': 0, 
                'avg_output_length': 0
            }

        categories = {}
        for ex in self.examples:
            cat = ex.get('category', 'unknown')
            categories[cat] = categories.get(cat, 0) + 1
        
        total_input_len = sum(len(ex['text_input']) for ex in self.examples)
        total_output_len = sum(len(ex['output']) for ex in self.examples)
        count = len(self.examples)

        return {
            'total_examples': count,
            'categories': categories,
            'avg_input_length': total_input_len / count,
            'avg_output_length': total_output_len / count
        }


# Initialize collector
collector = FinetuningDataCollector()