"""
AI client for process legitimacy analysis.
Uses OpenAI-compatible API (configurable via environment).
"""

import json
import logging
from typing import Any

from openai import OpenAI

from app.config import settings
from app.models import ProcessInfo, LegitimacyStatus
from app.ai.prompts import SYSTEM_PROMPT, create_batch_prompt
from app.ai.rate_limiter import SyncRateLimiter, RateLimitConfig


logger = logging.getLogger(__name__)


class AIClient:
    """
    AI client for analyzing process legitimacy.
    Uses the configured OpenAI-compatible API endpoint.
    """
    
    def __init__(self):
        self.client = OpenAI(
            base_url=settings.openai_base_url,
            api_key=settings.openai_api_key,
        )
        self.model = settings.openai_model
        
        # Rate limiter
        self.rate_limiter = SyncRateLimiter(RateLimitConfig(
            requests_per_minute=settings.ai_rate_limit_requests,
            batch_size=settings.ai_batch_size,
        ))
        
        # Stats tracking
        self.total_requests = 0
        self.total_tokens = 0
        self.failed_requests = 0
    
    def analyze_processes(
        self,
        processes: list[ProcessInfo],
        only_flagged: bool = True
    ) -> list[ProcessInfo]:
        """
        Analyze processes using AI and update their assessments.
        
        Args:
            processes: List of ProcessInfo to analyze
            only_flagged: If True, only analyze processes that were flagged by rules
            
        Returns:
            Updated list of ProcessInfo with AI assessments
        """
        # Filter to flagged processes if requested
        to_analyze = [p for p in processes if not only_flagged or p.is_flagged]
        
        if not to_analyze:
            logger.info("No processes to analyze with AI")
            return processes
        
        logger.info(f"Analyzing {len(to_analyze)} processes with AI")
        
        # Process in batches
        batch_size = settings.ai_batch_size
        pid_to_process = {p.pid: p for p in processes}
        
        for i in range(0, len(to_analyze), batch_size):
            batch = to_analyze[i:i + batch_size]
            
            try:
                assessments = self._analyze_batch(batch)
                
                # Update processes with AI assessments
                for assessment in assessments:
                    pid = assessment.get("pid")
                    if pid and pid in pid_to_process:
                        self._apply_assessment(pid_to_process[pid], assessment)
                        
            except Exception as e:
                logger.error(f"AI batch analysis failed: {e}")
                self.failed_requests += 1
        
        return processes
    
    def _analyze_batch(self, processes: list[ProcessInfo]) -> list[dict]:
        """Analyze a batch of processes and return assessments."""
        # Wait for rate limit
        self.rate_limiter.acquire()
        
        # Prepare process data for prompt
        process_dicts = [self._process_to_dict(p) for p in processes]
        prompt = create_batch_prompt(process_dicts)
        
        logger.debug(f"Sending batch of {len(processes)} processes to AI")
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=4000,
            )
            
            self.total_requests += 1
            
            # Track token usage
            if hasattr(response, 'usage') and response.usage:
                self.total_tokens += response.usage.total_tokens
            
            # Parse response
            content = response.choices[0].message.content
            return self._parse_ai_response(content, processes)
            
        except Exception as e:
            logger.error(f"AI API error: {e}")
            self.failed_requests += 1
            raise
    
    def _parse_ai_response(
        self, content: str, processes: list[ProcessInfo]
    ) -> list[dict]:
        """Parse AI response JSON and extract assessments."""
        # Try to extract JSON from response
        content = content.strip()
        
        # Handle markdown code blocks
        if content.startswith("```"):
            lines = content.split("\n")
            content = "\n".join(lines[1:-1] if lines[-1] == "```" else lines[1:])
        
        try:
            data = json.loads(content)
            
            if isinstance(data, dict) and "assessments" in data:
                return data["assessments"]
            elif isinstance(data, list):
                return data
            else:
                logger.warning(f"Unexpected AI response structure: {type(data)}")
                return []
                
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse AI response as JSON: {e}")
            logger.debug(f"Response content: {content[:500]}")
            return []
    
    def _process_to_dict(self, process: ProcessInfo) -> dict:
        """Convert ProcessInfo to dict for AI prompt."""
        return {
            "pid": process.pid,
            "process_name": process.process_name,
            "image_path": process.image_path,
            "command_line": process.command_line,
            "parent_pid": process.parent_pid,
            "parent_name": process.parent_name,
            "user": process.user,
            "integrity": process.integrity,
            "event_count": process.event_count,
            "file_operations": process.file_operations,
            "registry_operations": process.registry_operations,
            "network_operations": process.network_operations,
            "accessed_files": process.accessed_files[:5],
            "accessed_registry": process.accessed_registry[:5],
            "matched_rules": process.matched_rules,
        }
    
    def _apply_assessment(self, process: ProcessInfo, assessment: dict) -> None:
        """Apply AI assessment to a ProcessInfo."""
        # Update legitimacy
        legitimacy_str = assessment.get("legitimacy", "").lower()
        if legitimacy_str in ["legitimate", "safe", "benign"]:
            process.legitimacy = LegitimacyStatus.LEGITIMATE
        elif legitimacy_str in ["suspicious", "suspect"]:
            process.legitimacy = LegitimacyStatus.SUSPICIOUS
        elif legitimacy_str in ["malicious", "malware", "threat"]:
            process.legitimacy = LegitimacyStatus.MALICIOUS
        else:
            process.legitimacy = LegitimacyStatus.UNKNOWN
        
        # Update risk score (average with existing if any)
        ai_risk = assessment.get("risk_score")
        if ai_risk is not None and isinstance(ai_risk, (int, float)):
            existing_risk = process.risk_score
            # Weight AI assessment more heavily for flagged processes
            if existing_risk > 0:
                process.risk_score = int((existing_risk + ai_risk * 2) / 3)
            else:
                process.risk_score = int(ai_risk)
        
        # Update reasoning
        if assessment.get("reasoning"):
            process.ai_reasoning = assessment["reasoning"]
        
        # Update behavior tags
        ai_tags = assessment.get("behavior_tags", [])
        if isinstance(ai_tags, list):
            for tag in ai_tags:
                if tag and tag not in process.behavior_tags:
                    process.behavior_tags.append(tag)
        
        # Update MITRE techniques
        mitre = assessment.get("mitre_techniques", [])
        if isinstance(mitre, list):
            for technique in mitre:
                if technique and technique not in process.mitre_techniques:
                    process.mitre_techniques.append(technique)
    
    def get_stats(self) -> dict:
        """Get client usage statistics."""
        return {
            "total_requests": self.total_requests,
            "total_tokens": self.total_tokens,
            "failed_requests": self.failed_requests,
        }
