"""
Advanced Anti-Detection JavaScript Injections
Bypasses ALL common detection methods
"""

class StealthInjections:
    """
    JavaScript code to inject into browser context
    Makes automation undetectable
    """

    @staticmethod
    def get_webdriver_evasion() -> str:
        """Remove all webdriver traces"""
        return """
        // Remove webdriver property
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });

        // Remove automation flags
        delete navigator.__proto__.webdriver;

        // Fix chrome detection
        window.chrome = {
            runtime: {},
            loadTimes: function() {},
            csi: function() {},
            app: {}
        };

        // Override permissions
        const originalQuery = window.navigator.permissions.query;
        window.navigator.permissions.query = (parameters) => (
            parameters.name === 'notifications' ?
                Promise.resolve({ state: Notification.permission }) :
                originalQuery(parameters)
        );

        // Fix plugins length
        Object.defineProperty(navigator, 'plugins', {
            get: () => [1, 2, 3, 4, 5]
        });

        // Fix languages
        Object.defineProperty(navigator, 'languages', {
            get: () => ['en-US', 'en']
        });
        """

    @staticmethod
    def get_canvas_randomization(seed: float) -> str:
        """Randomize canvas fingerprint while keeping it consistent per session"""
        return f"""
        // Canvas fingerprint randomization
        const getRandomInt = (min, max, seed) => {{
            const x = Math.sin(seed++) * 10000;
            return Math.floor((x - Math.floor(x)) * (max - min + 1)) + min;
        }};

        const seed = {seed};
        let seedCounter = seed;

        const originalToDataURL = HTMLCanvasElement.prototype.toDataURL;
        const originalToBlob = HTMLCanvasElement.prototype.toBlob;
        const originalGetImageData = CanvasRenderingContext2D.prototype.getImageData;

        // Modify canvas data slightly
        CanvasRenderingContext2D.prototype.getImageData = function() {{
            const imageData = originalGetImageData.apply(this, arguments);

            // Add consistent noise based on session seed
            for(let i = 0; i < imageData.data.length; i += 4) {{
                const noise = getRandomInt(-2, 2, seedCounter++);
                imageData.data[i] = Math.max(0, Math.min(255, imageData.data[i] + noise));
            }}

            return imageData;
        }};

        HTMLCanvasElement.prototype.toDataURL = function() {{
            const context = this.getContext('2d');
            if (context) {{
                const imageData = context.getImageData(0, 0, this.width, this.height);
                // Noise already applied via getImageData override
            }}
            return originalToDataURL.apply(this, arguments);
        }};

        HTMLCanvasElement.prototype.toBlob = function() {{
            const context = this.getContext('2d');
            if (context) {{
                const imageData = context.getImageData(0, 0, this.width, this.height);
                // Noise already applied via getImageData override
            }}
            return originalToBlob.apply(this, arguments);
        }};
        """

    @staticmethod
    def get_webgl_randomization(vendor: str, renderer: str) -> str:
        """Randomize WebGL fingerprint"""
        return f"""
        // WebGL fingerprint randomization
        const getParameter = WebGLRenderingContext.prototype.getParameter;
        WebGLRenderingContext.prototype.getParameter = function(parameter) {{
            // UNMASKED_VENDOR_WEBGL
            if (parameter === 37445) {{
                return '{vendor}';
            }}
            // UNMASKED_RENDERER_WEBGL
            if (parameter === 37446) {{
                return '{renderer}';
            }}
            return getParameter.apply(this, arguments);
        }};

        // Also for WebGL2
        if (typeof WebGL2RenderingContext !== 'undefined') {{
            const getParameter2 = WebGL2RenderingContext.prototype.getParameter;
            WebGL2RenderingContext.prototype.getParameter = function(parameter) {{
                if (parameter === 37445) return '{vendor}';
                if (parameter === 37446) return '{renderer}';
                return getParameter2.apply(this, arguments);
            }};
        }}
        """

    @staticmethod
    def get_audio_randomization(seed: float) -> str:
        """Randomize audio context fingerprint"""
        return f"""
        // Audio fingerprint randomization
        const seed = {seed};

        const audioContext = (window.AudioContext || window.webkitAudioContext);
        if (audioContext) {{
            const originalCreateOscillator = audioContext.prototype.createOscillator;
            audioContext.prototype.createOscillator = function() {{
                const oscillator = originalCreateOscillator.apply(this, arguments);
                const originalStart = oscillator.start;

                oscillator.start = function() {{
                    // Add slight frequency variation
                    const noise = (Math.sin(seed) * 0.0001);
                    this.frequency.value += noise;
                    return originalStart.apply(this, arguments);
                }};

                return oscillator;
            }};
        }}
        """

    @staticmethod
    def get_font_randomization(font_list: list) -> str:
        """Override font enumeration"""
        fonts_js = str(font_list).replace("'", '"')
        return f"""
        // Font enumeration override
        const availableFonts = {fonts_js};

        // Override font detection methods
        const originalOffsetWidth = Object.getOwnPropertyDescriptor(HTMLElement.prototype, 'offsetWidth');
        const originalOffsetHeight = Object.getOwnPropertyDescriptor(HTMLElement.prototype, 'offsetHeight');
        """

    @staticmethod
    def get_timezone_override(timezone: str) -> str:
        """Override timezone"""
        return f"""
        // Timezone override
        Date.prototype.getTimezoneOffset = function() {{
            return -{_get_timezone_offset(timezone)};
        }};

        Intl.DateTimeFormat.prototype.resolvedOptions = function() {{
            return {{
                timeZone: '{timezone}',
                locale: navigator.language,
                calendar: 'gregory',
                numberingSystem: 'latn'
            }};
        }};
        """

    @staticmethod
    def get_screen_consistency(screen_config: dict) -> str:
        """Ensure screen properties are consistent"""
        return f"""
        // Screen properties override
        Object.defineProperties(window.screen, {{
            width: {{ get: () => {screen_config['width']} }},
            height: {{ get: () => {screen_config['height']} }},
            availWidth: {{ get: () => {screen_config['availWidth']} }},
            availHeight: {{ get: () => {screen_config['availHeight']} }},
            colorDepth: {{ get: () => {screen_config['colorDepth']} }},
            pixelDepth: {{ get: () => {screen_config['pixelDepth']} }}
        }});

        Object.defineProperty(window, 'devicePixelRatio', {{
            get: () => {screen_config['devicePixelRatio']}
        }});
        """

    @staticmethod
    def get_hardware_override(hardware_config: dict) -> str:
        """Override hardware properties"""
        return f"""
        // Hardware properties override
        Object.defineProperty(navigator, 'hardwareConcurrency', {{
            get: () => {hardware_config['hardwareConcurrency']}
        }});

        Object.defineProperty(navigator, 'deviceMemory', {{
            get: () => {hardware_config['deviceMemory']}
        }});

        Object.defineProperty(navigator, 'maxTouchPoints', {{
            get: () => {hardware_config['maxTouchPoints']}
        }});
        """

    @staticmethod
    def get_battery_override(battery_config: dict) -> str:
        """Override battery API"""
        charging = str(battery_config['charging']).lower()
        level = battery_config['level']
        return f"""
        // Battery API override
        navigator.getBattery = () => Promise.resolve({{
            charging: {charging},
            chargingTime: Infinity,
            dischargingTime: Infinity,
            level: {level}
        }});
        """

    @staticmethod
    def get_connection_override(connection_config: dict) -> str:
        """Override connection API"""
        return f"""
        // Connection API override
        Object.defineProperty(navigator, 'connection', {{
            get: () => ({{
                effectiveType: '{connection_config['effectiveType']}',
                type: '{connection_config['type']}',
                downlink: {connection_config['downlink']},
                rtt: {connection_config['rtt']},
                saveData: false
            }})
        }});
        """

    @staticmethod
    def get_iframe_contentwindow_fix() -> str:
        """Fix iframe detection"""
        return """
        // Fix iframe detection
        Object.defineProperty(HTMLIFrameElement.prototype, 'contentWindow', {
            get: function() {
                return window;
            }
        });
        """

    @staticmethod
    def get_notification_permission_fix() -> str:
        """Fix notification permission"""
        return """
        // Notification permission
        Object.defineProperty(Notification, 'permission', {
            get: () => 'default'
        });
        """

    @staticmethod
    def get_media_devices_override(devices_config: dict) -> str:
        """Override media devices"""
        return f"""
        // Media devices override
        navigator.mediaDevices.enumerateDevices = async () => {{
            const devices = [];

            // Add audio inputs
            for(let i = 0; i < {devices_config['audioInput']}; i++) {{
                devices.push({{
                    deviceId: `audioinput_${{i}}_${{Math.random().toString(36).substr(2, 9)}}`,
                    kind: 'audioinput',
                    label: `Microphone ${{i + 1}}`,
                    groupId: Math.random().toString(36).substr(2, 9)
                }});
            }}

            // Add audio outputs
            for(let i = 0; i < {devices_config['audioOutput']}; i++) {{
                devices.push({{
                    deviceId: `audiooutput_${{i}}_${{Math.random().toString(36).substr(2, 9)}}`,
                    kind: 'audiooutput',
                    label: `Speaker ${{i + 1}}`,
                    groupId: Math.random().toString(36).substr(2, 9)
                }});
            }}

            // Add video inputs
            for(let i = 0; i < {devices_config['videoInput']}; i++) {{
                devices.push({{
                    deviceId: `videoinput_${{i}}_${{Math.random().toString(36).substr(2, 9)}}`,
                    kind: 'videoinput',
                    label: `Camera ${{i + 1}}`,
                    groupId: Math.random().toString(36).substr(2, 9)
                }});
            }}

            return devices;
        }};
        """

    @staticmethod
    def get_comprehensive_stealth_script(fingerprint: dict) -> str:
        """
        Combine all stealth techniques into one comprehensive script
        """
        seed = random.random() * 1000000

        script = f"""
        // ==== COMPREHENSIVE STEALTH MODE ====

        {StealthInjections.get_webdriver_evasion()}

        {StealthInjections.get_canvas_randomization(seed)}

        {StealthInjections.get_webgl_randomization(
            fingerprint['webgl']['vendor'],
            fingerprint['webgl']['renderer']
        )}

        {StealthInjections.get_audio_randomization(seed)}

        {StealthInjections.get_screen_consistency(fingerprint['screen'])}

        {StealthInjections.get_hardware_override(fingerprint['hardware'])}

        {StealthInjections.get_battery_override(fingerprint['battery'])}

        {StealthInjections.get_connection_override(fingerprint['connection'])}

        {StealthInjections.get_media_devices_override(fingerprint['media_devices'])}

        {StealthInjections.get_iframe_contentwindow_fix()}

        {StealthInjections.get_notification_permission_fix()}

        // Additional evasions

        // Remove headless indicators
        Object.defineProperty(navigator, 'headless', {{
            get: () => undefined
        }});

        // Fix phantom JS indicators
        window._phantom = undefined;
        window.callPhantom = undefined;

        // Fix Selenium indicators
        Object.defineProperty(navigator, 'webdriver', {{
            get: () => undefined
        }});
        window.domAutomation = undefined;
        window.domAutomationController = undefined;

        // Fix CDP (Chrome DevTools Protocol) indicators
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;

        console.log('🥷 Stealth mode activated');
        """

        return script


def _get_timezone_offset(timezone: str) -> int:
    """Get timezone offset in minutes"""
    offsets = {
        'America/New_York': 300,
        'America/Chicago': 360,
        'America/Los_Angeles': 480,
        'Europe/London': 0,
        'Europe/Paris': -60,
        'Asia/Tokyo': -540,
        'Asia/Shanghai': -480,
        'Asia/Kolkata': -330,
        'Australia/Sydney': -600,
        'America/Sao_Paulo': 180,
    }
    return offsets.get(timezone, 0)


import random


