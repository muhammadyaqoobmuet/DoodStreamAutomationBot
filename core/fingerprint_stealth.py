import random
import hashlib
import json
from typing import Dict, List
import base64

class FingerprintStealth:
    """
    Advanced fingerprint generation that's statistically identical to real users
    Based on actual browser telemetry data
    """

    # Real-world statistics from StatCounter 2024
    BROWSER_MARKET_SHARE = {
        'chrome': 0.65,
        'safari': 0.19,
        'edge': 0.05,
        'firefox': 0.03,
        'opera': 0.02,
        'other': 0.06
    }

    OS_MARKET_SHARE = {
        'windows': 0.72,
        'macos': 0.15,
        'linux': 0.04,
        'android': 0.05,
        'ios': 0.04
    }

    SCREEN_RESOLUTIONS = {
        (1920, 1080): 0.22,
        (1366, 768): 0.18,
        (1440, 900): 0.10,
        (1536, 864): 0.08,
        (2560, 1440): 0.07,
        (1920, 1200): 0.05,
        (1600, 900): 0.05,
        (1280, 720): 0.04,
        (3840, 2160): 0.03,
        (2560, 1080): 0.02,
    }

    TIMEZONE_DISTRIBUTIONS = {
        'America/New_York': 0.15,
        'America/Chicago': 0.12,
        'America/Los_Angeles': 0.13,
        'Europe/London': 0.10,
        'Europe/Paris': 0.08,
        'Asia/Tokyo': 0.07,
        'Asia/Shanghai': 0.09,
        'Asia/Kolkata': 0.08,
        'Australia/Sydney': 0.03,
        'America/Sao_Paulo': 0.05,
        'America/Mexico_City': 0.04,
        'Europe/Berlin': 0.03,
        'Africa/Cairo': 0.02,
        'Asia/Dubai': 0.01,
    }

    def __init__(self):
        self.used_fingerprints = set()

    def weighted_choice(self, choices: Dict) -> any:
        """Select item based on probability distribution"""
        items = list(choices.keys())
        weights = list(choices.values())
        return random.choices(items, weights=weights)[0]

    def generate_consistent_fingerprint(self, seed: str = None) -> Dict:
        """
        Generate fingerprint that's internally consistent
        E.g., Safari only on macOS/iOS, Chrome versions match OS, etc.
        """
        if seed:
            random.seed(seed)

        # Select OS first (determines available browsers)
        os_type = self.weighted_choice(self.OS_MARKET_SHARE)

        # Select browser compatible with OS
        browser = self._get_compatible_browser(os_type)

        # Select screen resolution common for that OS
        screen_res = self._get_common_resolution(os_type)

        # Select timezone based on global distribution
        timezone = self.weighted_choice(self.TIMEZONE_DISTRIBUTIONS)

        # Generate detailed fingerprint
        fingerprint = {
            'os': self._generate_os_details(os_type),
            'browser': self._generate_browser_details(browser, os_type),
            'screen': self._generate_screen_details(screen_res),
            'hardware': self._generate_hardware_details(os_type),
            'timezone': timezone,
            'locale': self._get_locale_for_timezone(timezone),
            'fonts': self._generate_font_list(os_type),
            'plugins': self._generate_plugin_list(browser),
            'canvas': self._generate_canvas_fingerprint(),
            'webgl': self._generate_webgl_fingerprint(),
            'audio': self._generate_audio_fingerprint(),
            'media_devices': self._generate_media_devices(),
            'battery': self._generate_battery_status(),
            'connection': self._generate_connection_info(),
        }

        # Generate unique hash
        fingerprint_hash = self._hash_fingerprint(fingerprint)

        # Ensure uniqueness (regenerate if collision)
        if fingerprint_hash in self.used_fingerprints:
            return self.generate_consistent_fingerprint()

        self.used_fingerprints.add(fingerprint_hash)
        fingerprint['hash'] = fingerprint_hash

        return fingerprint

    def _get_compatible_browser(self, os_type: str) -> str:
        """Get browser compatible with OS"""
        if os_type == 'ios':
            return 'safari'
        elif os_type == 'macos':
            return random.choices(['chrome', 'safari', 'firefox'], weights=[0.5, 0.4, 0.1])[0]
        elif os_type == 'windows':
            return random.choices(['chrome', 'edge', 'firefox', 'opera'], weights=[0.7, 0.15, 0.1, 0.05])[0]
        elif os_type == 'linux':
            return random.choices(['chrome', 'firefox'], weights=[0.6, 0.4])[0]
        else:
            return 'chrome'

    def _get_common_resolution(self, os_type: str) -> tuple:
        """Get screen resolution common for OS"""
        if os_type == 'macos':
            resolutions = [(2560, 1440), (1920, 1080), (1440, 900)]
        elif os_type == 'windows':
            resolutions = [(1920, 1080), (1366, 768), (1536, 864), (1440, 900)]
        elif os_type == 'linux':
            resolutions = [(1920, 1080), (1366, 768), (1600, 900)]
        else:
            resolutions = list(self.SCREEN_RESOLUTIONS.keys())

        return random.choice(resolutions)

    def _generate_os_details(self, os_type: str) -> Dict:
        """Generate realistic OS version and details with a consistent user_agent_string"""
        if os_type == 'windows':
            versions = ['10.0', '11.0']
            version = random.choice(versions)
            return {
                'name': 'Windows',
                'version': version,
                'platform': 'Win32',
                'user_agent_string': f'Windows NT {version}; Win64; x64'
            }
        elif os_type == 'macos':
            versions = ['10_15_7', '11_6', '12_5', '13_0', '14_0']
            version = random.choice(versions)
            return {
                'name': 'macOS',
                'version': version.replace('_', '.'),
                'platform': 'MacIntel',
                'user_agent_string': f'Macintosh; Intel Mac OS X {version}'
            }
        elif os_type == 'linux':
            return {
                'name': 'Linux',
                'version': 'x86_64',
                'platform': 'Linux x86_64',
                'user_agent_string': 'X11; Linux x86_64'
            }
        elif os_type == 'android':
            version = random.choice(['11', '12', '13'])
            return {
                'name': 'Android',
                'version': version,
                'platform': 'Linux armv8l',
                'user_agent_string': f'Linux; Android {version}; Pixel 6'
            }
        elif os_type == 'ios':
            version = random.choice(['15_7', '16_4', '17_0'])
            return {
                'name': 'iOS',
                'version': version.replace('_', '.'),
                'platform': 'iPhone',
                'user_agent_string': f'iPhone; CPU iPhone OS {version} like Mac OS X'
            }
        else:
            # Fallback ensures required keys exist
            return {
                'name': os_type,
                'version': 'unknown',
                'platform': 'unknown',
                'user_agent_string': os_type
            }

    def _generate_browser_details(self, browser: str, os_type: str) -> Dict:
        """Generate realistic browser version"""
        if browser == 'chrome':
            version = f'{random.randint(115, 120)}.0.{random.randint(5000, 6000)}.{random.randint(100, 200)}'
            return {
                'name': 'Chrome',
                'version': version,
                'user_agent': f'Mozilla/5.0 ({self._generate_os_details(os_type)["user_agent_string"]}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version} Safari/537.36'
            }
        elif browser == 'firefox':
            version = f'{random.randint(115, 120)}.0'
            return {
                'name': 'Firefox',
                'version': version,
                'user_agent': f'Mozilla/5.0 ({self._generate_os_details(os_type)["user_agent_string"]}; rv:{version}) Gecko/20100101 Firefox/{version}'
            }
        elif browser == 'safari':
            version = f'{random.randint(15, 17)}.{random.randint(0, 5)}'
            return {
                'name': 'Safari',
                'version': version,
                'user_agent': f'Mozilla/5.0 ({self._generate_os_details(os_type)["user_agent_string"]}) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/{version} Safari/605.1.15'
            }
        else:
            return {'name': browser, 'version': '1.0', 'user_agent': 'Mozilla/5.0'}

    def _generate_screen_details(self, resolution: tuple) -> Dict:
        """Generate screen details"""
        width, height = resolution
        return {
            'width': width,
            'height': height,
            'availWidth': width,
            'availHeight': height - random.choice([0, 40, 48]),  # Account for taskbar
            'colorDepth': 24,
            'pixelDepth': 24,
            'devicePixelRatio': random.choice([1, 1.25, 1.5, 2]),
        }

    def _generate_hardware_details(self, os_type: str) -> Dict:
        """Generate hardware concurrency (CPU cores)"""
        if os_type in ['windows', 'macos']:
            cores = random.choices([4, 6, 8, 12, 16], weights=[0.3, 0.25, 0.25, 0.15, 0.05])[0]
        else:
            cores = random.choices([2, 4, 8], weights=[0.4, 0.4, 0.2])[0]

        return {
            'hardwareConcurrency': cores,
            'deviceMemory': random.choice([4, 8, 16, 32]),
            'maxTouchPoints': 0 if os_type in ['windows', 'macos', 'linux'] else random.randint(5, 10)
        }

    def _get_locale_for_timezone(self, timezone: str) -> str:
        """Get appropriate locale for timezone"""
        locale_map = {
            'America/New_York': 'en-US',
            'America/Chicago': 'en-US',
            'America/Los_Angeles': 'en-US',
            'Europe/London': 'en-GB',
            'Europe/Paris': 'fr-FR',
            'Asia/Tokyo': 'ja-JP',
            'Asia/Shanghai': 'zh-CN',
            'Asia/Kolkata': 'en-IN',
            'Australia/Sydney': 'en-AU',
            'America/Sao_Paulo': 'pt-BR',
            'America/Mexico_City': 'es-MX',
            'Europe/Berlin': 'de-DE',
            'Africa/Cairo': 'ar-EG',
            'Asia/Dubai': 'ar-AE',
        }
        return locale_map.get(timezone, 'en-US')

    def _generate_font_list(self, os_type: str) -> List[str]:
        """Generate realistic font list for OS"""
        common_fonts = ['Arial', 'Helvetica', 'Times New Roman', 'Courier New', 'Verdana', 'Georgia']

        if os_type == 'windows':
            windows_fonts = ['Calibri', 'Cambria', 'Consolas', 'Segoe UI', 'Tahoma']
            return common_fonts + windows_fonts + random.sample(['Impact', 'Comic Sans MS', 'Trebuchet MS'], 2)
        elif os_type == 'macos':
            mac_fonts = ['Helvetica Neue', 'Menlo', 'Monaco', 'San Francisco', 'Lucida Grande']
            return common_fonts + mac_fonts + random.sample(['Baskerville', 'Optima', 'Palatino'], 2)
        elif os_type == 'linux':
            linux_fonts = ['DejaVu Sans', 'Liberation Sans', 'Ubuntu', 'Noto Sans']
            return common_fonts + linux_fonts
        else:
            return common_fonts

    def _generate_plugin_list(self, browser: str) -> List[Dict]:
        """Generate realistic plugin list (mostly deprecated but still fingerprinted)"""
        if browser == 'chrome':
            return [
                {'name': 'Chrome PDF Plugin', 'filename': 'internal-pdf-viewer'},
                {'name': 'Chrome PDF Viewer', 'filename': 'mhjfbmdgcfjbbpaeojofohoefgiehjai'},
                {'name': 'Native Client', 'filename': 'internal-nacl-plugin'},
            ]
        else:
            return []

    def _generate_canvas_fingerprint(self) -> str:
        """Generate unique canvas fingerprint"""
        # Simulate canvas rendering variation
        data = str(random.random() * 1000000)
        return hashlib.sha256(data.encode()).hexdigest()[:16]

    def _generate_webgl_fingerprint(self) -> Dict:
        """Generate WebGL fingerprint"""
        vendors = ['Intel Inc.', 'NVIDIA Corporation', 'AMD', 'Apple Inc.']
        renderers = [
            'Intel Iris OpenGL Engine',
            'NVIDIA GeForce GTX 1060',
            'AMD Radeon RX 580',
            'Apple M1',
            'Intel UHD Graphics 630',
        ]

        return {
            'vendor': random.choice(vendors),
            'renderer': random.choice(renderers),
            'version': f'OpenGL ES {random.choice(["2.0", "3.0"])}',
            'shadingLanguageVersion': f'WebGL GLSL ES {random.choice(["1.0", "3.0"])}',
        }

    def _generate_audio_fingerprint(self) -> str:
        """Generate audio context fingerprint"""
        data = str(random.random() * 10000)
        return hashlib.sha256(data.encode()).hexdigest()[:12]

    def _generate_media_devices(self) -> Dict:
        """Generate media devices info"""
        return {
            'audioInput': random.randint(0, 2),
            'audioOutput': random.randint(1, 3),
            'videoInput': random.randint(0, 2),
        }

    def _generate_battery_status(self) -> Dict:
        """Generate battery status (if applicable)"""
        if random.random() < 0.7:  # 70% on AC power
            return {'charging': True, 'level': random.uniform(0.5, 1.0)}
        else:
            return {'charging': False, 'level': random.uniform(0.2, 0.9)}

    def _generate_connection_info(self) -> Dict:
        """Generate network connection info"""
        connection_types = ['4g', 'wifi', 'ethernet']
        effective_types = ['4g', '3g', '2g']

        return {
            'effectiveType': random.choice(effective_types),
            'type': random.choice(connection_types),
            'downlink': round(random.uniform(1.5, 10.0), 2),
            'rtt': random.randint(50, 300),
        }

    def _hash_fingerprint(self, fingerprint: Dict) -> str:
        """Generate hash of fingerprint for uniqueness check"""
        fp_string = json.dumps(fingerprint, sort_keys=True)
        return hashlib.sha256(fp_string.encode()).hexdigest()

    def generate_playwright_config(self, fingerprint: Dict) -> Dict:
        """Convert fingerprint to Playwright configuration"""
        return {
            'user_agent': fingerprint['browser']['user_agent'],
            'viewport': {
                'width': fingerprint['screen']['width'],
                'height': fingerprint['screen']['height']
            },
            'device_scale_factor': fingerprint['screen']['devicePixelRatio'],
            'timezone_id': fingerprint['timezone'],
            'locale': fingerprint['locale'],
            'geolocation': self._get_geolocation_for_timezone(fingerprint['timezone']),
            'permissions': ['geolocation'],
            'color_scheme': random.choice(['light', 'dark', 'no-preference']),
            'extra_http_headers': {
                'Accept-Language': f"{fingerprint['locale']},en;q=0.9",
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'DNT': str(random.choice([1, 0])),
                'Upgrade-Insecure-Requests': '1',
            }
        }

    def _get_geolocation_for_timezone(self, timezone: str) -> Dict:
        """Get approximate geolocation for timezone"""
        geo_map = {
            'America/New_York': {'latitude': 40.7128, 'longitude': -74.0060, 'accuracy': 100},
            'America/Los_Angeles': {'latitude': 34.0522, 'longitude': -118.2437, 'accuracy': 100},
            'Europe/London': {'latitude': 51.5074, 'longitude': -0.1278, 'accuracy': 100},
            'Asia/Tokyo': {'latitude': 35.6762, 'longitude': 139.6503, 'accuracy': 100},
            'Asia/Shanghai': {'latitude': 31.2304, 'longitude': 121.4737, 'accuracy': 100},
        }

        default_geo = {'latitude': 37.7749, 'longitude': -122.4194, 'accuracy': 100}
        geo = geo_map.get(timezone, default_geo)

        # Add random offset for uniqueness
        geo['latitude'] += random.uniform(-0.1, 0.1)
        geo['longitude'] += random.uniform(-0.1, 0.1)

        return geo

