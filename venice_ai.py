import requests
import json
import logging
import asyncio
import uuid
from typing import List, Dict, Optional
from config import (
    API_PROVIDER, VENICE_API_KEY, VENICE_AI_HEADERS, VENICE_AI_COOKIES,
    OPENROUTER_API_KEY, OPENROUTER_BASE_URL,
    GEMINI_API_KEY, GEMINI_BASE_URL,
    BEAST_SYSTEM_PROMPT, JAILBREAK_PROMPTS, MODEL_CONFIGS
)

class VeniceAI:
    """ThayinMMII's Beast AI - Multi-provider uncensored AI system"""
    
    def __init__(self):
        self.api_provider = API_PROVIDER
        self.setup_provider()
        logging.info(f"🔥 Beast AI initialized - Provider: {self.api_provider.upper()}")
        
    def setup_provider(self):
        """Setup current API provider configuration"""
        if self.api_provider == "venice":
            self.api_key = VENICE_API_KEY
            self.base_url = "https://outerface.venice.ai/api/inference/chat"
            self.headers = VENICE_AI_HEADERS
            self.cookies = VENICE_AI_COOKIES
            self.default_model = MODEL_CONFIGS["venice"]["default_model"]
            logging.info("🔥 Venice AI configured as primary (UNCENSORED)")
        elif self.api_provider == "openrouter":
            self.api_key = OPENROUTER_API_KEY
            self.base_url = OPENROUTER_BASE_URL
            self.default_model = MODEL_CONFIGS["openrouter"]["default_model"]
            logging.info("🚀 OpenRouter configured as provider")
        elif self.api_provider == "gemini":
            self.api_key = GEMINI_API_KEY
            self.base_url = GEMINI_BASE_URL
            self.default_model = MODEL_CONFIGS["gemini"]["default_model"]
            logging.info("🤖 Gemini configured as provider")

    def generate_ids(self):
        """Generate unique IDs for Venice AI requests"""
        return {
            'requestId': f'req_thayinmmii_{str(uuid.uuid4()).replace("-", "")}',
            'messageId': f'msg_beast_{str(uuid.uuid4()).replace("-", "")}',
            'userId': f'user_akshit_{str(uuid.uuid4()).replace("-", "")}'
        }

    def prepare_payload(self, conversation_history: List[Dict], user_message: str, jailbreak_mode: str = "beast_mode"):
        """Prepare API payload with BEAST MODE prompting"""
        
        if self.api_provider == "venice":
            ids = self.generate_ids()
            
            # BEAST MODE: Maximum uncensored system prompt
            beast_system = {
                "role": "system", 
                "content": BEAST_SYSTEM_PROMPT + "\\n\\n" + JAILBREAK_PROMPTS.get(jailbreak_mode, JAILBREAK_PROMPTS["beast_mode"])
            }
            
            # Prepare conversation
            messages = [beast_system]
            messages.extend(conversation_history)
            messages.append({"role": "user", "content": user_message})
            
            payload = {
                'requestId': ids['requestId'],
                'conversationType': 'text',
                'type': 'text',
                'modelId': self.default_model,
                'modelName': 'ThayinMMII Beast',
                'messageId': ids['messageId'],
                'userId': ids['userId'],
                'prompt': messages,
                'temperature': 0.9,  # High creativity for beast responses
                'maxTokens': 4000,
                'topP': 1.0,
                'streaming': False
            }
            return payload
            
        elif self.api_provider == "openrouter":
            # OpenRouter with beast prompt
            beast_system = {"role": "system", "content": BEAST_SYSTEM_PROMPT}
            messages = [beast_system]
            messages.extend(conversation_history)
            messages.append({"role": "user", "content": user_message})
            
            return {
                "model": self.default_model,
                "messages": messages,
                "temperature": 0.8,
                "max_tokens": 4000,
                "top_p": 1.0
            }
            
        elif self.api_provider == "gemini":
            # Gemini with beast prompt
            full_prompt = BEAST_SYSTEM_PROMPT + "\\n\\n"
            for msg in conversation_history:
                full_prompt += f"{msg['role']}: {msg['content']}\\n"
            full_prompt += f"user: {user_message}\\nassistant:"
            
            return {
                "contents": [{
                    "parts": [{"text": full_prompt}]
                }],
                "generationConfig": {
                    "temperature": 0.8,
                    "maxOutputTokens": 4000,
                    "topP": 1.0
                }
            }

    def get_ai_response(self, conversation_history: List[Dict], user_message: str, jailbreak_mode: str = "beast_mode") -> str:
        """Get AI response with fallback system"""
        try:
            return self._get_response_from_provider(conversation_history, user_message, jailbreak_mode)
        except Exception as e:
            logging.error(f"Primary provider {self.api_provider} failed: {e}")
            return self._try_fallback_providers(conversation_history, user_message, jailbreak_mode)

    def _get_response_from_provider(self, conversation_history: List[Dict], user_message: str, jailbreak_mode: str) -> str:
        """Get response from current provider"""
        
        if self.api_provider == "venice":
            return self._venice_request(conversation_history, user_message, jailbreak_mode)
        elif self.api_provider == "openrouter":
            return self._openrouter_request(conversation_history, user_message, jailbreak_mode)
        elif self.api_provider == "gemini":
            return self._gemini_request(conversation_history, user_message, jailbreak_mode)

    def _venice_request(self, conversation_history: List[Dict], user_message: str, jailbreak_mode: str) -> str:
        """Venice AI request - FULLY UNCENSORED"""
        try:
            payload = self.prepare_payload(conversation_history, user_message, jailbreak_mode)
            
            response = requests.post(
                self.base_url,
                headers=self.headers,
                cookies=self.cookies,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                response_data = response.json()
                if 'response' in response_data:
                    return f"🔥 {response_data['response'].strip()}"
                elif 'choices' in response_data and len(response_data['choices']) > 0:
                    return f"🔥 {response_data['choices'][0]['message']['content'].strip()}"
                elif 'message' in response_data:
                    return f"🔥 {response_data['message'].strip()}"
            
            logging.error(f"Venice AI unexpected response: {response.status_code} - {response.text}")
            raise Exception(f"Venice AI error: {response.status_code}")
            
        except Exception as e:
            logging.error(f"Venice AI request failed: {e}")
            raise

    def _openrouter_request(self, conversation_history: List[Dict], user_message: str, jailbreak_mode: str) -> str:
        """OpenRouter request with beast prompting"""
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json',
                'HTTP-Referer': 'https://github.com/ThayinMMII/HacxGPT-Beast',
                'X-Title': 'ThayinMMII HacxGPT Beast'
            }
            
            payload = self.prepare_payload(conversation_history, user_message, jailbreak_mode)
            
            response = requests.post(self.base_url, headers=headers, json=payload, timeout=60)
            
            if response.status_code == 200:
                response_data = response.json()
                return f"🚀 {response_data['choices'][0]['message']['content'].strip()}"
            
            logging.error(f"OpenRouter error: {response.status_code} - {response.text}")
            raise Exception(f"OpenRouter error: {response.status_code}")
            
        except Exception as e:
            logging.error(f"OpenRouter request failed: {e}")
            raise

    def _gemini_request(self, conversation_history: List[Dict], user_message: str, jailbreak_mode: str) -> str:
        """Gemini request with beast prompting"""
        try:
            headers = {'Content-Type': 'application/json'}
            payload = self.prepare_payload(conversation_history, user_message, jailbreak_mode)
            
            response = requests.post(
                f"{self.base_url}?key={self.api_key}",
                headers=headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                response_data = response.json()
                return f"🤖 {response_data['candidates'][0]['content']['parts'][0]['text'].strip()}"
            
            logging.error(f"Gemini error: {response.status_code} - {response.text}")
            raise Exception(f"Gemini error: {response.status_code}")
            
        except Exception as e:
            logging.error(f"Gemini request failed: {e}")
            raise

    def _try_fallback_providers(self, conversation_history: List[Dict], user_message: str, jailbreak_mode: str) -> str:
        """Try fallback providers when primary fails"""
        providers = ["venice", "openrouter", "gemini"]
        if self.api_provider in providers:
            providers.remove(self.api_provider)
        
        for provider in providers:
            try:
                logging.info(f"🔄 Trying fallback provider: {provider}")
                original_provider = self.api_provider
                self.api_provider = provider
                self.setup_provider()
                
                response = self._get_response_from_provider(conversation_history, user_message, jailbreak_mode)
                
                # Restore original provider
                self.api_provider = original_provider
                self.setup_provider()
                
                return f"🔄 (via {provider.upper()}): {response}"
                
            except Exception as e:
                logging.warning(f"Fallback provider {provider} also failed: {e}")
                continue
        
        return "❌ All AI providers failed! The Beast needs a moment to recover. Try again, Akshit!"

    def switch_provider(self, new_provider: str) -> bool:
        """Switch to different AI provider"""
        if new_provider in ["venice", "openrouter", "gemini"]:
            self.api_provider = new_provider
            self.setup_provider()
            logging.info(f"🔄 Provider switched to: {new_provider.upper()}")
            return True
        return False

    def get_available_models(self) -> List[str]:
        """Get available models for current provider"""
        return MODEL_CONFIGS[self.api_provider]["models"]

    def apply_jailbreak(self, mode: str, conversation_history: List[Dict]) -> List[Dict]:
        """Apply jailbreak mode to conversation"""
        if mode in JAILBREAK_PROMPTS:
            jailbreak_prompt = {
                "role": "system",
                "content": JAILBREAK_PROMPTS[mode]
            }
            return [jailbreak_prompt] + conversation_history
        return conversation_history

    def get_provider_status(self) -> dict:
        """Get current provider status"""
        return {
            "current_provider": self.api_provider,
            "model": self.default_model,
            "available_providers": ["venice", "openrouter", "gemini"],
            "beast_mode": "ACTIVE"
        }

# For compatibility with existing code
class MultiProviderAI(VeniceAI):
    pass