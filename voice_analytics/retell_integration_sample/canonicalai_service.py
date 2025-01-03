#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 12:15:48 2024

@author: tom
"""

import httpx
import os
from dotenv import load_dotenv

class CanonicalAIService:
    """Simple service to forward call_analyzed events to Canonical AI"""
    
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('CANONICALAI_API_KEY')
        if not self.api_key:
            raise ValueError("CANONICALAI_API_KEY not found in environment variables")
            
    async def forward_call_analyzed(self, event_data: dict) -> dict:
        """
        Forward a call_analyzed event to Canonical AI
        
        Args:
            event_data (dict): The complete Retell webhook event data
            
        Returns:
            dict: Response from Canonical AI
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                'https://voiceapp.canonical.chat/api/v1/webhooks/retell',
                json=event_data,
                headers={
                    'Content-Type': 'application/json',
                    'X-Canonical-Api-Key': self.api_key
                }
            )
            return response.json()