"""
Relevance Scoring for Memory Items

This module provides sophisticated scoring mechanisms to evaluate the relevance and
quality of memory items, enabling more effective retrieval and prioritization.
"""

from typing import Dict, List, Any, Optional, Tuple, Union, Callable
from datetime import datetime
import math


class RelevanceScorer:
    """
    Advanced relevance scoring system for memory items.
    
    Features:
    - Multi-factor scoring based on semantic relevance, recency, usage, and quality
    - Contextual weighting based on query type
    - Confidence scoring for retrieval reliability
    - Feedback mechanism for continuous improvement
    """
    
    def __init__(self):
        """Initialize the relevance scorer with default weights."""
        # Base weights for different factors (can be adjusted)
        self.weights = {
            "semantic_similarity": 0.35,  # How closely the content matches semantically
            "recency": 0.15,              # How recently the item was created/updated
            "usage_count": 0.10,          # How frequently the item has been used
            "success_rate": 0.25,         # How successful the solutions have been
            "complexity_match": 0.15      # How well complexity matches the problem
        }
        
        # Track feedback for continuous learning
        self.feedback_history = {}
        
        # Thresholds for determining quality of answers
        self.confidence_thresholds = {
            "high": 0.75,    # Above this is high confidence
            "medium": 0.5,   # Above this is medium confidence
            "low": 0.3       # Above this is low confidence, below is insufficient
        }
        
        # Query type recognizers (simple keyword-based approach)
        self.query_type_patterns = {
            "code": ["how to", "code", "function", "class", "implement", "error", "bug"],
            "concept": ["what is", "explain", "concept", "define", "mean"],
            "comparison": ["difference", "compare", "better", "versus", "vs"],
            "troubleshooting": ["fix", "error", "isn't working", "problem", "debug"],
            "opinion": ["should", "best practice", "recommend", "opinion"]
        }
    
    def score_item(self, 
                  item: Dict[str, Any], 
                  query: str, 
                  semantic_similarity: float = None, 
                  context: Dict[str, Any] = None) -> float:
        """
        Calculate a comprehensive relevance score for a memory item.
        
        Args:
            item: The memory item to score
            query: The user query
            semantic_similarity: Pre-calculated semantic similarity (0.0-1.0)
            context: Additional context for scoring
            
        Returns:
            Relevance score from 0.0 to 1.0
        """
        if context is None:
            context = {}
            
        # Use custom weights if provided in context
        weights = context.get("weights", self.weights)
        
        # Calculate individual factor scores
        factor_scores = {}
        
        # 1. Semantic similarity (if not provided, default to 0.0)
        factor_scores["semantic_similarity"] = semantic_similarity or 0.0
        
        # 2. Recency score
        factor_scores["recency"] = self._calculate_recency_score(item)
        
        # 3. Usage count score
        factor_scores["usage_count"] = self._calculate_usage_score(item)
        
        # 4. Success rate score
        factor_scores["success_rate"] = self._calculate_success_score(item)
        
        # 5. Complexity match score
        factor_scores["complexity_match"] = self._calculate_complexity_match(item, query, context)
        
        # Calculate weighted sum of factor scores
        relevance_score = sum(factor_scores[factor] * weights[factor] for factor in weights)
        
        # Apply any query-specific adjustments
        query_type = self._determine_query_type(query)
        relevance_score = self._adjust_for_query_type(relevance_score, query_type, factor_scores)
        
        # Normalize to 0.0-1.0 range (just in case)
        relevance_score = max(0.0, min(1.0, relevance_score))
        
        # Store the detailed scoring for explanation if needed
        item["_score_details"] = {
            "factor_scores": factor_scores,
            "final_score": relevance_score,
            "query_type": query_type
        }
        
        return relevance_score
    
    def _calculate_recency_score(self, item: Dict[str, Any]) -> float:
        """
        Calculate a score based on how recent the item is.
        
        Args:
            item: The memory item
            
        Returns:
            Recency score from 0.0 to 1.0
        """
        # Get timestamp from item
        timestamp_str = item.get("timestamp")
        if not timestamp_str:
            return 0.5  # Default if no timestamp
            
        try:
            # Parse timestamp
            timestamp = datetime.fromisoformat(timestamp_str)
            
            # Calculate age in days
            age_days = (datetime.now() - timestamp).days
            
            # Score calculation (newer items get higher scores)
            # Uses a decay function: score = 1.0 * e^(-age_days/180)
            # This gives items:
            # - 1 day old: 0.995 score
            # - 30 days old: 0.85 score
            # - 180 days old: 0.37 score
            # - 365 days old: 0.13 score
            decay_rate = 180  # Half-life in days
            recency_score = math.exp(-age_days / decay_rate)
            
            return min(1.0, max(0.0, recency_score))
            
        except (ValueError, TypeError):
            # If timestamp parsing fails
            return 0.5
    
    def _calculate_usage_score(self, item: Dict[str, Any]) -> float:
        """
        Calculate a score based on how frequently the item has been used.
        
        Args:
            item: The memory item
            
        Returns:
            Usage score from 0.0 to 1.0
        """
        # Get usage count from item
        usage_count = item.get("usage_count", 0)
        
        # Calculate score using a logarithmic function
        # This rewards frequently used items but with diminishing returns
        # score = min(1.0, 0.2 + 0.4 * ln(1 + usage_count))
        if usage_count <= 0:
            return 0.2  # Base score for unused items
            
        usage_score = min(1.0, 0.2 + 0.4 * math.log(1 + usage_count))
        
        return usage_score
    
    def _calculate_success_score(self, item: Dict[str, Any]) -> float:
        """
        Calculate a score based on how successful the item has been when used.
        
        Args:
            item: The memory item
            
        Returns:
            Success score from 0.0 to 1.0
        """
        # Get success metrics from item
        successes = item.get("success_count", 0)
        failures = item.get("failure_count", 0)
        total_uses = successes + failures
        
        if total_uses == 0:
            return 0.5  # Default score for items without feedback
            
        # Calculate success rate
        success_rate = successes / total_uses
        
        # Apply confidence adjustment based on sample size
        # Small sample sizes get pulled toward the neutral 0.5
        confidence_factor = min(1.0, total_uses / 10)  # Reaches 1.0 at 10+ uses
        adjusted_rate = 0.5 + (success_rate - 0.5) * confidence_factor
        
        return adjusted_rate
    
    def _calculate_complexity_match(self, 
                                   item: Dict[str, Any], 
                                   query: str, 
                                   context: Dict[str, Any]) -> float:
        """
        Calculate how well the item's complexity matches the query complexity.
        
        Args:
            item: The memory item
            query: The user query
            context: Additional context
            
        Returns:
            Complexity match score from 0.0 to 1.0
        """
        # Estimate query complexity by length and structure
        query_length = len(query)
        query_complexity = min(1.0, query_length / 200)  # Normalize to 0.0-1.0
        
        # If context provides an explicit complexity assessment, use it
        if "query_complexity" in context:
            query_complexity = context["query_complexity"]
        
        # Get item complexity
        item_complexity = item.get("complexity", 0.5)  # Default to medium
        
        # Calculate match score based on difference
        # Perfect match = 1.0, worst match = 0.0
        complexity_diff = abs(query_complexity - item_complexity)
        complexity_match = 1.0 - complexity_diff
        
        return complexity_match
    
    def _determine_query_type(self, query: str) -> str:
        """
        Determine the type of query based on content analysis.
        
        Args:
            query: The user query
            
        Returns:
            Query type string
        """
        query_lower = query.lower()
        
        # Check for each query type pattern
        matches = {}
        for query_type, patterns in self.query_type_patterns.items():
            matches[query_type] = sum(1 for pattern in patterns if pattern in query_lower)
        
        # Get query type with most matches
        if any(matches.values()):
            return max(matches.items(), key=lambda x: x[1])[0]
        
        # Default if no matches
        return "general"
    
    def _adjust_for_query_type(self, 
                              score: float, 
                              query_type: str, 
                              factor_scores: Dict[str, float]) -> float:
        """
        Adjust relevance score based on query type.
        
        Args:
            score: Base relevance score
            query_type: Identified query type
            factor_scores: Individual factor scores
            
        Returns:
            Adjusted relevance score
        """
        # Apply query-type specific adjustments
        if query_type == "code":
            # For code queries, success rate is critical
            if factor_scores["success_rate"] < 0.4:
                score *= 0.8  # Penalize items with low success rates
                
        elif query_type == "troubleshooting":
            # For troubleshooting, recency is more important
            if factor_scores["recency"] > 0.8:
                score *= 1.2  # Boost very recent solutions
                score = min(1.0, score)  # Cap at 1.0
                
        elif query_type == "opinion":
            # For opinion queries, usage count matters more
            if factor_scores["usage_count"] > 0.7:
                score *= 1.15  # Boost widely used opinions
                score = min(1.0, score)
        
        return score
    
    def get_confidence_level(self, score: float) -> str:
        """
        Determine confidence level from a relevance score.
        
        Args:
            score: Relevance score (0.0-1.0)
            
        Returns:
            Confidence level string
        """
        if score >= self.confidence_thresholds["high"]:
            return "high"
        elif score >= self.confidence_thresholds["medium"]:
            return "medium"
        elif score >= self.confidence_thresholds["low"]:
            return "low"
        else:
            return "insufficient"
    
    def record_feedback(self, item_id: str, query: str, was_helpful: bool) -> None:
        """
        Record user feedback for a memory item to improve future scoring.
        
        Args:
            item_id: ID of the memory item
            query: The query that retrieved this item
            was_helpful: Whether the item was helpful
        """
        if item_id not in self.feedback_history:
            self.feedback_history[item_id] = []
            
        self.feedback_history[item_id].append({
            "query": query,
            "was_helpful": was_helpful,
            "timestamp": datetime.now().isoformat()
        })
    
    def adjust_weights(self, weight_updates: Dict[str, float]) -> None:
        """
        Update the scoring weights based on performance data.
        
        Args:
            weight_updates: Dictionary of weight updates
        """
        for factor, weight in weight_updates.items():
            if factor in self.weights:
                # Ensure weight is valid
                weight = max(0.0, min(1.0, weight))
                self.weights[factor] = weight
                
        # Normalize weights to sum to 1.0
        total = sum(self.weights.values())
        if total > 0:
            for factor in self.weights:
                self.weights[factor] /= total 