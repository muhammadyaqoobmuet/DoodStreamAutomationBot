"""
Enterprise-Grade Residential Proxy Management
With health checking, rotation strategy, and geo-distribution
"""

import asyncio
import aiohttp
import time
from typing import List, Dict, Optional
from dataclasses import dataclass
from collections import defaultdict
import random

@dataclass
class ProxyStats:
    """Statistics for each proxy"""
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    last_used: float = 0
    avg_response_time: float = 0
    consecutive_failures: int = 0
    banned: bool = False

    @property
    def success_rate(self) -> float:
        if self.total_requests == 0:
            return 1.0
        return self.successful_requests / self.total_requests

    @property
    def is_healthy(self) -> bool:
        """Determine if proxy is healthy"""
        if self.banned or self.consecutive_failures >= 3:
            return False
        if self.total_requests > 10 and self.success_rate < 0.5:
            return False
        return True

class ResidentialProxyPool:
    """
    Intelligent proxy pool with health monitoring and rotation
    """

    def __init__(self, proxy_list: List[str], health_check_interval: int = 300):
        self.proxies = proxy_list
        self.proxy_stats = {proxy: ProxyStats() for proxy in proxy_list}
        self.health_check_interval = health_check_interval
        self.geo_groups = self._group_by_geo()
        self.current_proxy = None
        self.rotation_strategy = 'intelligent'  # or 'round_robin', 'random', 'least_used'

    def _group_by_geo(self) -> Dict[str, List[str]]:
        """Group proxies by geographic region (would need geo-ip lookup in production)"""
        # Placeholder - in production, use MaxMind GeoIP or similar
        groups = defaultdict(list)
        for proxy in self.proxies:
            # Simulate geo grouping
            region = random.choice(['US', 'EU', 'ASIA', 'OTHER'])
            groups[region].append(proxy)
        return groups

    async def health_check(self, proxy: str) -> bool:
        """Check if proxy is working"""
        test_urls = [
            'http://httpbin.org/ip',
            'https://api.ipify.org?format=json',
        ]

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    random.choice(test_urls),
                    proxy=f'http://{proxy}',
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    return response.status == 200
        except Exception as e:
            print(f"Health check failed for {proxy}: {e}")
            return False

    async def health_check_all(self):
        """Perform health check on all proxies"""
        tasks = [self.health_check(proxy) for proxy in self.proxies]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        for proxy, is_healthy in zip(self.proxies, results):
            if isinstance(is_healthy, Exception) or not is_healthy:
                self.proxy_stats[proxy].consecutive_failures += 1
                if self.proxy_stats[proxy].consecutive_failures >= 5:
                    self.proxy_stats[proxy].banned = True
                    print(f"🚫 Proxy {proxy} marked as banned")
            else:
                self.proxy_stats[proxy].consecutive_failures = 0

    def get_next_proxy(self, geo_preference: Optional[str] = None) -> str:
        """
        Get next proxy based on rotation strategy
        """
        if self.rotation_strategy == 'intelligent':
            return self._get_intelligent_proxy(geo_preference)
        elif self.rotation_strategy == 'least_used':
            return self._get_least_used_proxy()
        elif self.rotation_strategy == 'random':
            return self._get_random_healthy_proxy()
        else:
            return self._get_round_robin_proxy()

    def _get_intelligent_proxy(self, geo_preference: Optional[str] = None) -> str:
        """
        Select proxy using intelligent algorithm:
        - Prioritize healthy proxies
        - Balance usage across proxies
        - Respect geo preferences
        - Avoid recently failed proxies
        """
        candidates = [p for p in self.proxies if self.proxy_stats[p].is_healthy]

        if not candidates:
            # All proxies unhealthy, reset and try again
            self._reset_proxy_health()
            candidates = self.proxies

        # Filter by geo preference if specified
        if geo_preference and geo_preference in self.geo_groups:
            geo_candidates = [p for p in candidates if p in self.geo_groups[geo_preference]]
            if geo_candidates:
                candidates = geo_candidates

        # Score each proxy
        scores = []
        current_time = time.time()

        for proxy in candidates:
            stats = self.proxy_stats[proxy]

            # Factors for scoring
            success_factor = stats.success_rate * 100
            usage_factor = 100 / (stats.total_requests + 1)  # Prefer less used
            recency_factor = min(100, (current_time - stats.last_used) / 60)  # Prefer not recently used

            # Weighted score
            score = (success_factor * 0.5) + (usage_factor * 0.3) + (recency_factor * 0.2)
            scores.append((proxy, score))

        # Select proxy with highest score
        scores.sort(key=lambda x: x[1], reverse=True)

        # Add randomness to top 5 to avoid patterns
        top_candidates = scores[:min(5, len(scores))]
        selected = random.choice(top_candidates)[0]

        self.current_proxy = selected
        self.proxy_stats[selected].last_used = current_time

        return selected

    def _get_least_used_proxy(self) -> str:
        """Get proxy with least usage"""
        healthy_proxies = [p for p in self.proxies if self.proxy_stats[p].is_healthy]
        if not healthy_proxies:
            healthy_proxies = self.proxies

        return min(healthy_proxies, key=lambda p: self.proxy_stats[p].total_requests)

    def _get_random_healthy_proxy(self) -> str:
        """Get random healthy proxy"""
        healthy_proxies = [p for p in self.proxies if self.proxy_stats[p].is_healthy]
        if not healthy_proxies:
            healthy_proxies = self.proxies

        return random.choice(healthy_proxies)

    def _get_round_robin_proxy(self) -> str:
        """Simple round robin selection"""
        if self.current_proxy is None:
            self.current_proxy = self.proxies[0]
            return self.current_proxy

        current_index = self.proxies.index(self.current_proxy)
        next_index = (current_index + 1) % len(self.proxies)

        # Skip unhealthy proxies
        attempts = 0
        while not self.proxy_stats[self.proxies[next_index]].is_healthy and attempts < len(self.proxies):
            next_index = (next_index + 1) % len(self.proxies)
            attempts += 1

        self.current_proxy = self.proxies[next_index]
        return self.current_proxy

    def record_request(self, proxy: str, success: bool, response_time: float):
        """Record request statistics"""
        stats = self.proxy_stats[proxy]
        stats.total_requests += 1

        if success:
            stats.successful_requests += 1
            stats.consecutive_failures = 0
            # Update rolling average response time
            if stats.avg_response_time == 0:
                stats.avg_response_time = response_time
            else:
                stats.avg_response_time = (stats.avg_response_time * 0.8) + (response_time * 0.2)
        else:
            stats.failed_requests += 1
            stats.consecutive_failures += 1

            # Ban after too many consecutive failures
            if stats.consecutive_failures >= 5:
                stats.banned = True
                print(f"🚫 Proxy {proxy} auto-banned after 5 consecutive failures")

    def _reset_proxy_health(self):
        """Reset health status for all proxies"""
        for stats in self.proxy_stats.values():
            if stats.consecutive_failures < 10:  # Don't reset truly bad proxies
                stats.consecutive_failures = 0
                stats.banned = False

    def get_stats_summary(self) -> Dict:
        """Get summary statistics for all proxies"""
        total_requests = sum(s.total_requests for s in self.proxy_stats.values())
        healthy_count = sum(1 for s in self.proxy_stats.values() if s.is_healthy)
        banned_count = sum(1 for s in self.proxy_stats.values() if s.banned)

        return {
            'total_proxies': len(self.proxies),
            'healthy_proxies': healthy_count,
            'banned_proxies': banned_count,
            'total_requests': total_requests,
            'avg_success_rate': sum(s.success_rate for s in self.proxy_stats.values()) / len(self.proxies)
        }

    def get_proxy_performance(self, proxy: str) -> Dict:
        """Get detailed performance metrics for a proxy"""
        stats = self.proxy_stats[proxy]
        return {
            'proxy': proxy,
            'total_requests': stats.total_requests,
            'success_rate': f"{stats.success_rate * 100:.2f}%",
            'avg_response_time': f"{stats.avg_response_time:.2f}s",
            'is_healthy': stats.is_healthy,
            'banned': stats.banned,
            'consecutive_failures': stats.consecutive_failures,
        }


class ProxyValidator:
    """
    Validates proxies before adding to pool
    Tests for:
    - Actual residential IP (not datacenter)
    - Geo-location accuracy
    - Speed and reliability
    """

    @staticmethod
    async def validate_proxy(proxy: str) -> Dict:
        """Comprehensive proxy validation"""
        results = {
            'valid': False,
            'is_residential': False,
            'country': None,
            'city': None,
            'isp': None,
            'response_time': None,
            'errors': []
        }

        try:
            start_time = time.time()

            async with aiohttp.ClientSession() as session:
                # Check IP info
                async with session.get(
                    'https://ipapi.co/json/',
                    proxy=f'http://{proxy}',
                    timeout=aiohttp.ClientTimeout(total=15)
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        results['country'] = data.get('country_name')
                        results['city'] = data.get('city')
                        results['isp'] = data.get('org')
                        results['response_time'] = time.time() - start_time

                        # Check if residential (heuristic - not perfect)
                        isp_lower = str(data.get('org', '')).lower()
                        datacenter_keywords = ['amazon', 'google', 'microsoft', 'digitalocean', 
                                            'ovh', 'hetzner', 'linode', 'vultr']
                        results['is_residential'] = not any(kw in isp_lower for kw in datacenter_keywords)

                        results['valid'] = True
                    else:
                        results['errors'].append(f"HTTP {response.status}")

        except asyncio.TimeoutError:
            results['errors'].append("Timeout")
        except Exception as e:
            results['errors'].append(str(e))

        return results

    @staticmethod
    async def validate_proxy_list(proxy_list: List[str]) -> List[str]:
        """Validate entire proxy list and return only residential IPs"""
        tasks = [ProxyValidator.validate_proxy(proxy) for proxy in proxy_list]
        results = await asyncio.gather(*tasks)

        validated_proxies = []
        for proxy, result in zip(proxy_list, results):
            if result['valid'] and result['is_residential']:
                print(f"✅ {proxy} - {result['country']}, {result['city']} ({result['isp']})")
                validated_proxies.append(proxy)
            else:
                errors = ', '.join(result['errors']) if result['errors'] else 'Not residential'
                print(f"❌ {proxy} - {errors}")

        return validated_proxies



