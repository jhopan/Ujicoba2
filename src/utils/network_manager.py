"""
Network Manager for handling connectivity checks and network-related operations
"""

import asyncio
import logging
from typing import Tuple, Optional, Dict
from datetime import datetime, timedelta

try:
    import aiohttp
    AIOHTTP_AVAILABLE = True
except ImportError:
    AIOHTTP_AVAILABLE = False
    # Fallback untuk basic connectivity check
    import urllib.request
    import urllib.error

logger = logging.getLogger(__name__)

class NetworkManager:
    def __init__(self):
        self.last_check = None
        self.check_interval = 300  # 5 minutes
        self.timeout = 10
        self.test_urls = [
            'https://www.google.com',
            'https://www.googleapis.com',
            'https://api.telegram.org'
        ]
    
    async def check_connectivity(self, force_check: bool = False) -> bool:
        """
        Check internet connectivity
        
        Args:
            force_check: Force a new check regardless of cache
            
        Returns:
            bool: True if connected, False otherwise
        """
        now = datetime.now()
        
        # Use cached result if recent
        if (not force_check and 
            self.last_check and 
            (now - self.last_check).seconds < self.check_interval):
            return True
        
        try:
            if AIOHTTP_AVAILABLE:
                async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout)) as session:
                    for url in self.test_urls:
                        try:
                            async with session.get(url) as response:
                                if response.status == 200:
                                    self.last_check = now
                                    logger.info("Network connectivity confirmed")
                                    return True
                        except Exception as e:
                            logger.debug(f"Failed to reach {url}: {e}")
                            continue
            else:
                # Fallback using urllib
                for url in self.test_urls:
                    try:
                        urllib.request.urlopen(url, timeout=self.timeout)
                        self.last_check = now
                        logger.info("Network connectivity confirmed (fallback)")
                        return True
                    except (urllib.error.URLError, Exception) as e:
                        logger.debug(f"Failed to reach {url}: {e}")
                        continue
                
                logger.warning("No network connectivity detected")
                return False
                
        except Exception as e:
            logger.error(f"Network check failed: {e}")
            return False
    
    async def wait_for_connectivity(self, max_wait_time: int = 300) -> bool:
        """
        Wait for network connectivity to be restored
        
        Args:
            max_wait_time: Maximum time to wait in seconds
            
        Returns:
            bool: True if connectivity restored, False if timeout
        """
        start_time = datetime.now()
        check_interval = 30  # Check every 30 seconds
        
        while (datetime.now() - start_time).seconds < max_wait_time:
            if await self.check_connectivity(force_check=True):
                return True
            
            logger.info(f"Waiting for network connectivity... ({check_interval}s)")
            await asyncio.sleep(check_interval)
        
        logger.error(f"Network connectivity not restored after {max_wait_time} seconds")
        return False
    
    async def test_google_drive_connectivity(self) -> bool:
        """
        Test specific connectivity to Google Drive APIs
        
        Returns:
            bool: True if Google Drive is accessible
        """
        google_urls = [
            'https://www.googleapis.com/drive/v3/about',
            'https://www.googleapis.com/oauth2/v2/tokeninfo'
        ]
        
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout)) as session:
                for url in google_urls:
                    try:
                        async with session.get(url) as response:
                            # We expect 401 for unauthorized, which means the service is up
                            if response.status in [200, 401, 403]:
                                logger.info("Google Drive API connectivity confirmed")
                                return True
                    except Exception as e:
                        logger.debug(f"Failed to reach Google API {url}: {e}")
                        continue
                
                logger.warning("Google Drive API not accessible")
                return False
                
        except Exception as e:
            logger.error(f"Google Drive connectivity check failed: {e}")
            return False
    
    async def test_telegram_connectivity(self) -> bool:
        """
        Test specific connectivity to Telegram APIs
        
        Returns:
            bool: True if Telegram is accessible
        """
        telegram_urls = [
            'https://api.telegram.org',
            'https://core.telegram.org'
        ]
        
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout)) as session:
                for url in telegram_urls:
                    try:
                        async with session.get(url) as response:
                            if response.status in [200, 401, 404]:  # 404 is expected for base API
                                logger.info("Telegram API connectivity confirmed")
                                return True
                    except Exception as e:
                        logger.debug(f"Failed to reach Telegram API {url}: {e}")
                        continue
                
                logger.warning("Telegram API not accessible")
                return False
                
        except Exception as e:
            logger.error(f"Telegram connectivity check failed: {e}")
            return False
    
    async def get_network_info(self) -> Dict[str, any]:
        """
        Get comprehensive network information
        
        Returns:
            dict: Network status information
        """
        info = {
            'timestamp': datetime.now().isoformat(),
            'general_connectivity': await self.check_connectivity(force_check=True),
            'google_drive_connectivity': await self.test_google_drive_connectivity(),
            'telegram_connectivity': await self.test_telegram_connectivity(),
            'last_check': self.last_check.isoformat() if self.last_check else None
        }
        
        return info
    
    def get_retry_delay(self, attempt: int) -> int:
        """
        Calculate exponential backoff delay for retry attempts
        
        Args:
            attempt: Current attempt number (1-based)
            
        Returns:
            int: Delay in seconds
        """
        # Exponential backoff: 2^attempt with maximum of 300 seconds (5 minutes)
        delay = min(2 ** attempt, 300)
        return delay
    
    async def execute_with_retry(self, operation, max_retries: int = 3, 
                                connectivity_check: bool = True) -> Tuple[bool, Optional[any], str]:
        """
        Execute an operation with retry logic and connectivity checks
        
        Args:
            operation: Async function to execute
            max_retries: Maximum number of retry attempts
            connectivity_check: Whether to check connectivity before retrying
            
        Returns:
            tuple: (success, result, error_message)
        """
        last_error = ""
        
        for attempt in range(1, max_retries + 1):
            try:
                # Check connectivity if required
                if connectivity_check and not await self.check_connectivity():
                    if not await self.wait_for_connectivity():
                        return False, None, "Network connectivity lost and not restored"
                
                # Execute the operation
                result = await operation()
                return True, result, ""
                
            except Exception as e:
                last_error = str(e)
                logger.warning(f"Operation failed (attempt {attempt}/{max_retries}): {e}")
                
                # Don't retry on the last attempt
                if attempt < max_retries:
                    delay = self.get_retry_delay(attempt)
                    logger.info(f"Retrying in {delay} seconds...")
                    await asyncio.sleep(delay)
        
        return False, None, f"Operation failed after {max_retries} attempts. Last error: {last_error}"
    
    def check_network(self) -> Dict[str, any]:
        """
        Synchronous network check for compatibility
        
        Returns:
            dict: Network status with 'connected' key
        """
        try:
            if AIOHTTP_AVAILABLE:
                # For async environments, we'll do a simple check
                import socket
                socket.create_connection(("8.8.8.8", 53), timeout=5)
                return {'connected': True}
            else:
                # Use urllib fallback
                try:
                    urllib.request.urlopen('https://www.google.com', timeout=self.timeout)
                    return {'connected': True}
                except:
                    return {'connected': False}
        except Exception as e:
            logger.debug(f"Network check failed: {e}")
            return {'connected': False}
