"""
Memory Compression and Summarization

This module provides techniques for compressing and summarizing stored knowledge
to reduce token usage and storage requirements while preserving essential information.
"""

from typing import Dict, List, Any, Optional, Tuple, Union
from datetime import datetime
import json
import re


class MemoryCompressor:
    """
    Memory compression and summarization system for efficient storage.
    
    Features:
    - Progressive summarization of large text entries
    - Code-specific compression techniques
    - Version tracking for compressed knowledge
    - Information density analysis
    """
    
    def __init__(self, 
                compression_level: str = "balanced", 
                preserve_code: bool = True,
                max_summary_ratio: float = 0.5):
        """
        Initialize the memory compressor.
        
        Args:
            compression_level: Compression aggressiveness ('minimal', 'balanced', 'aggressive')
            preserve_code: Whether to preserve code blocks during compression
            max_summary_ratio: Maximum ratio of summary to original content (0.0-1.0)
        """
        self.compression_level = compression_level
        self.preserve_code = preserve_code
        self.max_summary_ratio = max_summary_ratio
        
        # Stats tracking
        self.total_items_compressed = 0
        self.total_chars_before = 0
        self.total_chars_after = 0
        
        # Default summarization parameters for different compression levels
        self.summarization_params = {
            "minimal": {
                "paragraph_ratio": 0.9,  # Keep 90% of paragraphs
                "sentence_ratio": 0.8,   # Keep 80% of sentences in kept paragraphs
                "remove_examples": False,
                "preserve_headings": True,
                "preserve_lists": True
            },
            "balanced": {
                "paragraph_ratio": 0.7,  # Keep 70% of paragraphs
                "sentence_ratio": 0.7,   # Keep 70% of sentences in kept paragraphs
                "remove_examples": False,
                "preserve_headings": True,
                "preserve_lists": True
            },
            "aggressive": {
                "paragraph_ratio": 0.5,  # Keep 50% of paragraphs
                "sentence_ratio": 0.5,   # Keep 50% of sentences in kept paragraphs
                "remove_examples": True,
                "preserve_headings": True,
                "preserve_lists": False
            }
        }
    
    def compress_item(self, 
                     item: Dict[str, Any], 
                     item_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Compress a memory item while preserving essential information.
        
        Args:
            item: The memory item to compress
            item_type: Type of item ('text', 'code', 'mixed')
            
        Returns:
            Compressed item with original preserved in metadata
        """
        if not item_type:
            item_type = self._determine_item_type(item)
            
        # Create a working copy
        compressed_item = item.copy()
        
        # Store original size for analysis
        original_content = item.get('content', '')
        original_size = len(original_content)
        self.total_chars_before += original_size
        
        # Save original version if not already present
        if 'original_version' not in compressed_item:
            compressed_item['original_version'] = {
                'content': original_content,
                'size': original_size,
                'timestamp': item.get('timestamp', datetime.now().isoformat())
            }
        
        # Apply compression based on item type
        if item_type == 'code':
            compressed_content = self._compress_code(original_content)
        elif item_type == 'text':
            compressed_content = self._compress_text(original_content)
        else:  # mixed
            compressed_content = self._compress_mixed(original_content)
            
        # Update content and metadata
        compressed_item['content'] = compressed_content
        compressed_item['compression'] = {
            'type': item_type,
            'level': self.compression_level,
            'original_size': original_size,
            'compressed_size': len(compressed_content),
            'compression_ratio': len(compressed_content) / max(original_size, 1),
            'timestamp': datetime.now().isoformat()
        }
        
        # Update stats
        self.total_items_compressed += 1
        self.total_chars_after += len(compressed_content)
        
        return compressed_item
    
    def _determine_item_type(self, item: Dict[str, Any]) -> str:
        """
        Determine the type of content in the item.
        
        Args:
            item: The memory item
            
        Returns:
            Content type: 'text', 'code', or 'mixed'
        """
        content = item.get('content', '')
        
        # Check for explicit type in metadata
        if 'content_type' in item:
            return item['content_type']
            
        # Check category
        category = item.get('category', '').lower()
        if 'code' in category or 'implementation' in category:
            return 'code'
            
        # Count code markers
        code_block_pattern = r'```[a-z]*\n[\s\S]*?\n```'
        inline_code_pattern = r'`[^`]+`'
        
        code_blocks = re.findall(code_block_pattern, content)
        inline_code = re.findall(inline_code_pattern, content)
        
        total_chars = len(content)
        code_chars = sum(len(block) for block in code_blocks) + sum(len(code) for code in inline_code)
        
        # If more than 30% is code, consider it mixed or code
        if total_chars > 0 and code_chars / total_chars > 0.3:
            if code_chars / total_chars > 0.7:
                return 'code'
            else:
                return 'mixed'
                
        return 'text'
    
    def _compress_text(self, content: str) -> str:
        """
        Compress text content through summarization techniques.
        
        Args:
            content: The text content to compress
            
        Returns:
            Compressed text content
        """
        # Get parameters based on compression level
        params = self.summarization_params[self.compression_level]
        
        # Split into paragraphs (preserve newlines)
        paragraphs = re.split(r'(\n\s*\n)', content)
        
        # Identify important paragraphs (for now, simplified)
        paragraph_scores = self._score_paragraphs(paragraphs)
        
        # Determine how many paragraphs to keep
        total_paragraphs = len(paragraph_scores)
        paragraphs_to_keep = max(1, int(total_paragraphs * params["paragraph_ratio"]))
        
        # Get indices of top paragraphs
        top_indices = sorted(range(len(paragraph_scores)), 
                            key=lambda i: paragraph_scores[i], 
                            reverse=True)[:paragraphs_to_keep]
        top_indices.sort()  # Resort in original order
        
        # Build compressed content
        compressed_paragraphs = []
        
        # Counter for skipped paragraphs
        skipped_count = 0
        
        for i, paragraph in enumerate(paragraphs):
            # Skip empty paragraphs
            if not paragraph.strip():
                compressed_paragraphs.append(paragraph)
                continue
                
            # If it's a heading or important paragraph, include it
            is_heading = paragraph.strip().startswith('#') or paragraph.strip().startswith('<h')
            is_list = bool(re.match(r'(\s*[-*]\s+|\s*\d+\.\s+)', paragraph.strip()))
            
            if i in top_indices or (is_heading and params["preserve_headings"]) or (is_list and params["preserve_lists"]):
                # For important paragraphs, compress sentences if they're long enough
                if len(paragraph.split('.')) > 3 and not is_heading and not is_list:
                    compressed_paragraphs.append(self._compress_paragraph(paragraph, params["sentence_ratio"]))
                else:
                    compressed_paragraphs.append(paragraph)
                skipped_count = 0
            else:
                skipped_count += 1
                # Add an indicator for multiple skipped paragraphs
                if skipped_count == 1:
                    compressed_paragraphs.append("... [content summarized] ...")
        
        # Join everything back together
        result = ''.join(compressed_paragraphs)
        
        # Check if the compression ratio meets our target
        if len(result) / len(content) > self.max_summary_ratio:
            # If compression wasn't effective enough, try more aggressive parameters
            if self.compression_level != "aggressive":
                temp_level = self.compression_level
                self.compression_level = "aggressive"
                result = self._compress_text(content)
                self.compression_level = temp_level
                
        return result
    
    def _score_paragraphs(self, paragraphs: List[str]) -> List[float]:
        """
        Score paragraphs by importance for summarization.
        
        Args:
            paragraphs: List of paragraph strings
            
        Returns:
            List of importance scores for each paragraph
        """
        scores = []
        
        # Important linguistic markers
        important_phrases = [
            "key", "important", "essential", "critical", "necessary", "crucial",
            "significant", "fundamental", "vital", "main", "primary", "core",
            "in summary", "to summarize", "in conclusion", "therefore", "thus",
            "consequently", "as a result", "finally", "notably", "specifically"
        ]
        
        for paragraph in paragraphs:
            # Skip empty paragraphs
            if not paragraph.strip():
                scores.append(0.0)
                continue
                
            score = 0.0
            
            # Position bias - first and last paragraphs often contain key information
            position_score = 0.0
            
            # Length score - not too short, not too long
            word_count = len(paragraph.split())
            length_score = min(1.0, word_count / 30) if word_count < 150 else 150 / word_count
            
            # Importance markers
            marker_score = 0.0
            for phrase in important_phrases:
                if phrase in paragraph.lower():
                    marker_score += 0.2
            marker_score = min(1.0, marker_score)
            
            # Information density estimate (unique words ratio)
            words = paragraph.lower().split()
            if words:
                density_score = len(set(words)) / len(words)
            else:
                density_score = 0.0
                
            # Combine scores with weights
            score = (
                0.2 * position_score +
                0.3 * length_score +
                0.3 * marker_score +
                0.2 * density_score
            )
            
            scores.append(score)
            
        return scores
    
    def _compress_paragraph(self, paragraph: str, sentence_ratio: float) -> str:
        """
        Compress a paragraph by removing less important sentences.
        
        Args:
            paragraph: The paragraph to compress
            sentence_ratio: Ratio of sentences to keep
            
        Returns:
            Compressed paragraph
        """
        # Split into sentences (handle abbreviations and decimals carefully)
        sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s', paragraph)
        
        if len(sentences) <= 2:
            return paragraph  # Don't compress very short paragraphs
            
        # Score sentences
        sentence_scores = []
        for sentence in sentences:
            # Length score (penalize very short or very long)
            word_count = len(sentence.split())
            length_score = min(1.0, word_count / 10) if word_count < 30 else 30 / word_count
            
            # Position score (first and last sentences are important)
            position_score = 0.0
            
            # Information density
            words = sentence.lower().split()
            if words:
                unique_ratio = len(set(words)) / len(words)
            else:
                unique_ratio = 0.0
                
            # Combined score
            score = 0.5 * length_score + 0.3 * position_score + 0.2 * unique_ratio
            sentence_scores.append(score)
            
        # Determine sentences to keep
        sentences_to_keep = max(1, int(len(sentences) * sentence_ratio))
        top_indices = sorted(range(len(sentence_scores)), 
                            key=lambda i: sentence_scores[i], 
                            reverse=True)[:sentences_to_keep]
        
        # Always include first and last sentences if not already included
        if 0 not in top_indices and len(sentences) > 0:
            top_indices.append(0)
        if len(sentences) - 1 not in top_indices and len(sentences) > 1:
            top_indices.append(len(sentences) - 1)
            
        top_indices.sort()  # Resort in original order
        
        # Build compressed paragraph
        result = []
        skipped_marker_added = False
        
        for i, sentence in enumerate(sentences):
            if i in top_indices:
                result.append(sentence)
                skipped_marker_added = False
            elif not skipped_marker_added:
                result.append("...")
                skipped_marker_added = True
                
        return ' '.join(result)
    
    def _compress_code(self, content: str) -> str:
        """
        Compress code content while preserving functionality.
        
        Args:
            content: The code content to compress
            
        Returns:
            Compressed code content
        """
        # If we're set to preserve code, don't compress it
        if self.preserve_code:
            return content
            
        # Identify code blocks
        code_block_pattern = r'```([a-z]*)\n([\s\S]*?)\n```'
        code_blocks = re.findall(code_block_pattern, content)
        
        if not code_blocks:
            # Try to treat entire content as code
            if "def " in content or "function " in content or "class " in content:
                return self._compress_code_block(content)
            return content
            
        # Compress each code block
        for lang, block in code_blocks:
            compressed_block = self._compress_code_block(block)
            # Replace in original
            content = content.replace(f"```{lang}\n{block}\n```", 
                                     f"```{lang}\n{compressed_block}\n```")
                                     
        return content
    
    def _compress_code_block(self, code: str) -> str:
        """
        Compress a code block while preserving functionality.
        
        Args:
            code: The code block to compress
            
        Returns:
            Compressed code block
        """
        # Remove extra whitespace
        code = re.sub(r'\n\s*\n', '\n', code)
        
        # Remove most comments except important ones
        lines = code.split('\n')
        result_lines = []
        
        important_comment_markers = ['todo', 'note', 'important', 'warning', 'fixme', 'hack']
        
        for line in lines:
            stripped = line.strip()
            
            # Keep non-comment lines
            if not stripped.startswith('#') and not stripped.startswith('//'):
                result_lines.append(line)
                continue
                
            # Check for important comments
            comment_lower = stripped.lower()
            is_important = any(marker in comment_lower for marker in important_comment_markers)
            
            if is_important:
                result_lines.append(line)
                
        # Join back together
        return '\n'.join(result_lines)
    
    def _compress_mixed(self, content: str) -> str:
        """
        Compress mixed text and code content.
        
        Args:
            content: The mixed content to compress
            
        Returns:
            Compressed mixed content
        """
        # Split content into text and code parts
        code_block_pattern = r'(```[a-z]*\n[\s\S]*?\n```)'
        parts = re.split(code_block_pattern, content)
        
        compressed_parts = []
        
        for part in parts:
            if part.startswith('```') and part.endswith('```'):
                # This is a code block
                if self.preserve_code:
                    compressed_parts.append(part)
                else:
                    # Extract language and code content
                    match = re.match(r'```([a-z]*)\n([\s\S]*?)\n```', part)
                    if match:
                        lang, code = match.groups()
                        compressed_code = self._compress_code_block(code)
                        compressed_parts.append(f"```{lang}\n{compressed_code}\n```")
                    else:
                        compressed_parts.append(part)
            else:
                # This is text content
                compressed_parts.append(self._compress_text(part))
                
        # Join everything back together
        return ''.join(compressed_parts)
    
    def decompress_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Restore the original uncompressed version of an item.
        
        Args:
            item: The compressed memory item
            
        Returns:
            Decompressed item with original content
        """
        if 'original_version' not in item:
            # Item is not compressed or original was not saved
            return item
            
        # Create a copy
        decompressed_item = item.copy()
        
        # Restore original content
        original = item['original_version']
        decompressed_item['content'] = original['content']
        
        # Update metadata
        if 'compression' in decompressed_item:
            decompressed_item['compression']['decompressed'] = True
            decompressed_item['compression']['decompression_timestamp'] = datetime.now().isoformat()
            
        return decompressed_item
    
    def get_compression_stats(self) -> Dict[str, Any]:
        """
        Get compression statistics.
        
        Returns:
            Dictionary with compression statistics
        """
        if self.total_chars_before == 0:
            compression_ratio = 0
        else:
            compression_ratio = self.total_chars_after / self.total_chars_before
            
        chars_saved = self.total_chars_before - self.total_chars_after
        
        return {
            "items_compressed": self.total_items_compressed,
            "total_chars_before": self.total_chars_before,
            "total_chars_after": self.total_chars_after,
            "chars_saved": chars_saved,
            "compression_ratio": compression_ratio,
            "compression_percentage": (1 - compression_ratio) * 100
        }
    
    def set_compression_level(self, level: str) -> None:
        """
        Set the compression level.
        
        Args:
            level: New compression level ('minimal', 'balanced', 'aggressive')
        """
        if level in self.summarization_params:
            self.compression_level = level 