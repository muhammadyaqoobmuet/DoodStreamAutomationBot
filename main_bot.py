

import asyncio
from playwright.async_api import async_playwright
import random
import time
from typing import Dict, List
import sys

# Import our custom modules
sys.path.append('/home/user/doodstream_advanced')
from core.ai_behavior_engine import AIBehaviorEngine, AdaptiveTiming
from core.fingerprint_stealth import FingerprintStealth
from core.residential_proxy_pool import ResidentialProxyPool, ProxyValidator
from core.stealth_injections import StealthInjections


class AdvancedDoodStreamBot:
    """
    The most advanced view bot implementation
    Features:
    - AI-powered human behavior simulation
    - Military-grade fingerprint randomization
    - Residential proxy rotation with health monitoring
    - Adaptive timing that learns from success/failure
    - Statistical indistinguishability from real users
    """

    def __init__(self, video_url: str, proxy_list: List[str], target_views: int):
        self.video_url = video_url
        self.target_views = target_views
        self.completed_views = 0

        # Initialize core components
        print("🚀 Initializing Advanced Bot Components...")
        self.behavior_engine = AIBehaviorEngine()
        self.fingerprint_generator = FingerprintStealth()
        self.proxy_pool = ResidentialProxyPool(proxy_list)
        self.adaptive_timing = AdaptiveTiming()
        self.stealth_injector = StealthInjections()

        # Statistics
        self.stats = {
            'total_attempts': 0,
            'successful_views': 0,
            'failed_attempts': 0,
            'detected_attempts': 0,
            'avg_view_duration': 0,
            'start_time': time.time()
        }

    async def validate_proxies(self):
        """Validate all proxies before starting"""
        print("🔍 Validating proxy list...")
        validated = await ProxyValidator.validate_proxy_list(self.proxy_pool.proxies)

        if len(validated) < len(self.proxy_pool.proxies) * 0.5:
            print(f"⚠️  Warning: Only {len(validated)}/{len(self.proxy_pool.proxies)} proxies are valid residential IPs")

        self.proxy_pool.proxies = validated
        print(f"✅ {len(validated)} validated residential proxies ready\n")

    async def generate_single_view(self, view_number: int) -> bool:
        """
        Generate a single view with full anti-detection
        Returns True if successful
        """
        self.stats['total_attempts'] += 1

        # Step 1: Generate unique fingerprint
        fingerprint = self.fingerprint_generator.generate_consistent_fingerprint()
        print(f"\n{'='*60}")
        print(f"🎯 VIEW #{view_number}")
        print(f"{'='*60}")
        print(f"🔧 Fingerprint: {fingerprint['hash'][:16]}...")
        print(f"💻 OS: {fingerprint['os']['name']} {fingerprint['os']['version']}")
        print(f"🌐 Browser: {fingerprint['browser']['name']} {fingerprint['browser']['version']}")
        print(f"📍 Location: {fingerprint['timezone']}")

        # Step 2: Select optimal proxy
        proxy = self.proxy_pool.get_next_proxy()
        print(f"🌍 Proxy: {proxy[:20]}...")

        # Step 3: Select behavior profile
        behavior_profile = self.behavior_engine.select_behavior_profile()
        print(f"👤 Behavior: {behavior_profile.interaction_style} (attention: {behavior_profile.attention_span:.1f}s)")

        # Step 4: Launch stealth browser
        try:
            async with async_playwright() as p:
                start_time = time.time()

                # Configure browser with fingerprint
                playwright_config = self.fingerprint_generator.generate_playwright_config(fingerprint)

                browser = await p.chromium.launch(
                    headless=False,
                    proxy={'server': f'http://{proxy}'},
                    args=[
                        '--disable-blink-features=AutomationControlled',
                        '--disable-dev-shm-usage',
                        '--no-sandbox',
                        '--disable-setuid-sandbox',
                        '--disable-web-security',
                        '--disable-features=IsolateOrigins,site-per-process',
                        '--disable-background-networking',
                        '--disable-background-timer-throttling',
                        '--disable-backgrounding-occluded-windows',
                        '--disable-breakpad',
                        '--disable-component-extensions-with-background-pages',
                        '--disable-extensions',
                        '--disable-features=TranslateUI',
                        '--disable-ipc-flooding-protection',
                        '--disable-renderer-backgrounding',
                        '--force-color-profile=srgb',
                        '--hide-scrollbars',
                        '--metrics-recording-only',
                        '--mute-audio',
                        '--no-default-browser-check',
                        '--no-first-run',
                        '--no-pings',
                    ]
                )

                # Create context with fingerprint
                context = await browser.new_context(
                    user_agent=playwright_config['user_agent'],
                    viewport=playwright_config['viewport'],
                    device_scale_factor=playwright_config['device_scale_factor'],
                    timezone_id=playwright_config['timezone_id'],
                    locale=playwright_config['locale'],
                    geolocation=playwright_config['geolocation'],
                    permissions=playwright_config['permissions'],
                    color_scheme=playwright_config['color_scheme'],
                    extra_http_headers=playwright_config['extra_http_headers'],
                )

                # Create page
                page = await context.new_page()

                # Inject comprehensive stealth script
                stealth_script = self.stealth_injector.get_comprehensive_stealth_script(fingerprint)
                await page.add_init_script(stealth_script)

                print(f"🥷 Stealth injections applied")

                # Step 5: Navigate to video
                print(f"📹 Loading video...")
                try:
                    await page.goto(self.video_url, timeout=60000, wait_until='networkidle')
                except Exception as e:
                    print(f"❌ Navigation failed: {e}")
                    await browser.close()
                    self.proxy_pool.record_request(proxy, False, time.time() - start_time)
                    return False

                # Handle age verification gate FIRST and FAST if present
                try:
                    clicked_age_gate = False
                    # Race a few highly-specific selectors with short timeouts
                    selectors = [
                        "button:has-text(\"Yes, I'm 18+\")",
                        "text=Yes, I'm 18+",
                        "[role=button]:has-text(\"Yes, I'm 18+\")",
                        "button.bg-green-600",
                        "//button[normalize-space() = \"Yes, I'm 18+\"]",
                    ]
                    for sel in selectors:
                        try:
                            btn = page.locator(sel).first
                            await btn.wait_for(state='visible', timeout=1200)
                            print("🛡️ Age gate detected. Confirming 18+...")
                            await btn.click(force=True)
                            clicked_age_gate = True
                            break
                        except:
                            continue

                    if not clicked_age_gate:
                        # Scoped modal search as fallback
                        try:
                            modal = page.locator('div:has(h3:has-text("Age Verification"))').first
                            await modal.wait_for(state='visible', timeout=1500)
                            inner_btn = modal.locator('button.bg-green-600, button:has-text("Yes, I\'m 18+"), [role="button"]:has-text("Yes, I\'m 18+")').first
                            await inner_btn.wait_for(state='visible', timeout=800)
                            print("🛡️ Age gate detected (modal). Confirming 18+...")
                            await inner_btn.click(force=True)
                            clicked_age_gate = True
                        except:
                            pass

                    # Minimal wait only to allow overlay removal
                    if clicked_age_gate:
                        await page.wait_for_timeout(300)
                except Exception as _:
                    pass

                # Step 6: Wait for player (handle iframe-based players)
                try:
                    # Ensure DOM is settled
                    await page.wait_for_load_state('domcontentloaded')
                    # Use a softer network idle for slow proxies; allow more time
                    try:
                        await page.wait_for_load_state('networkidle')
                    except:
                        # If networkidle doesn't arrive (slow proxy), continue with a small delay
                        await page.wait_for_timeout(1500)

                    # Common embed patterns: iframe, video tag, plyr/jwplayer selectors
                    player_frame = None

                    # Prefer known host iframe first (e.g., dsvplay)
                    known_iframe = await page.query_selector('iframe[src*="dsvplay"], iframe[src*="dood"]')
                    if known_iframe:
                        try:
                            frame = await known_iframe.content_frame()
                            if frame:
                                player_frame = frame
                        except:
                            player_frame = None

                    # Try direct video element first (exclude small ad videos by id)
                    video_el = await page.query_selector('video:not([id^="exo-video"])')
                    if video_el:
                        print("✅ Video element found on main page")
                    else:
                        # Try iframes and look inside
                        iframes = await page.query_selector_all('iframe')
                        if len(iframes) == 0:
                            raise Exception('No iframes and no <video> found')

                        # Heuristic: prefer iframe with allow attributes for media
                        for iframe in iframes:
                            try:
                                # Ensure the frame is available
                                frame = await iframe.content_frame()
                                if not frame:
                                    continue
                                # Probe for video or player controls inside
                                has_video = await frame.query_selector('video')
                                has_jw = await frame.query_selector('.jwplayer')
                                has_plyr = await frame.query_selector('[data-plyr]')
                                has_play_btn = await frame.query_selector('button[aria-label*="play" i]')
                                if has_video or has_jw or has_plyr or has_play_btn:
                                    player_frame = frame
                                    break
                            except:
                                continue

                        if not player_frame:
                            raise Exception('Player not found inside iframes')

                        # Wait within the chosen frame for the player to be ready
                        try:
                            await player_frame.wait_for_selector('video, .jwplayer, [data-plyr]', timeout=30000)
                            print("✅ Player loaded inside iframe")
                        except Exception as inner_e:
                            raise Exception(f'Player inside iframe not ready: {inner_e}')

                        # Try to start playback if possible with real gestures + fallbacks
                        try:
                            # Try visible play buttons first (common providers)
                            play_btn = await player_frame.query_selector('button[aria-label*="play" i], .plyr__control[data-plyr="play"], .jw-icon-play, .vjs-big-play-button, .ytp-large-play-button')
                            if play_btn:
                                await play_btn.scroll_into_view_if_needed()
                                await play_btn.click(force=True)
                                await asyncio.sleep(1.0)

                            # Video.js specific: click tech element or use API if present
                            vjs_container = await player_frame.query_selector('.video-js')
                            if vjs_container:
                                try:
                                    await vjs_container.click()
                                except:
                                    pass
                                # Use videojs API if available in the frame
                                try:
                                    await player_frame.evaluate('(()=>{if(window.videojs){try{const p=window.videojs("#video_player"); p.muted(false); p.volume(0.2); p.play(); return true;}catch(e){}} return false;})()')
                                    await asyncio.sleep(1.0)
                                except:
                                    pass

                            # Gesture on native video element (or tech element)
                            vid = await player_frame.query_selector('video, .vjs-tech')
                            if vid:
                                await vid.scroll_into_view_if_needed()
                                try:
                                    await vid.click()
                                except:
                                    pass
                                try:
                                    await player_frame.keyboard.press('Space')
                                except:
                                    pass
                                await asyncio.sleep(0.8)

                                # Unmute and set volume to avoid autoplay blocks
                                try:
                                    await player_frame.evaluate('(()=>{const v=document.querySelector("video"); if(!v) return; v.muted=false; v.volume=0.2; if(v.play) v.play(); })()')
                                except:
                                    pass

                                # If still paused, click overlay play icons
                                overlay_play = await player_frame.query_selector('.plyr__poster, .jw-display-icon-container, .vjs-poster')
                                if overlay_play:
                                    try:
                                        await overlay_play.click(force=True)
                                    except:
                                        pass

                            # Final fallback: programmatic play
                            await asyncio.sleep(1.0)
                            # Buffering-aware check: ensure readyState and not paused
                            is_playing = await player_frame.evaluate('(()=>{const v=document.querySelector("video, .vjs-tech"); return v && !v.paused && v.readyState>=2;})()')
                            if not is_playing:
                                # Try Video.js API again then fallback to native play
                                try:
                                    await player_frame.evaluate('(()=>{if(window.videojs){try{const p=window.videojs("#video_player"); p.muted(false); p.volume(0.2); p.play(); return true;}catch(e){}} return false;})()')
                                except:
                                    pass
                                await player_frame.evaluate('(()=>{const v=document.querySelector("video, .vjs-tech"); if(!v) return false; v.muted=false; v.volume=0.2; return v.play? (v.play(), true) : false; })()')
                                await asyncio.sleep(1.0)
                        except:
                            pass

                    print(f"✅ Video player loaded")

                    # Verify playback by sampling currentTime with retries
                    playback_ok = False
                    try:
                        sample_a = None
                        sample_b = None
                        if 'player_frame' in locals() and player_frame:
                            # Wait for canplay or readyState>=2 with timeout for slow proxies
                            try:
                                await player_frame.wait_for_function('(()=>{const v=document.querySelector("video"); return v && v.readyState>=2;})()', timeout=8000)
                            except:
                                # proceed anyway
                                pass
                            sample_a = await player_frame.evaluate('(()=>{const v=document.querySelector("video"); return v? v.currentTime : null;})()')
                            # Allow extended buffering for slow loads (up to ~1 minute)
                            await asyncio.sleep(10.0)
                            sample_b = await player_frame.evaluate('(()=>{const v=document.querySelector("video"); return v? v.currentTime : null;})()')
                            if sample_a is not None and sample_b is not None and sample_b > sample_a + 0.5:
                                playback_ok = True
                        # If not ok, try one more activation click
                        if not playback_ok and 'player_frame' in locals() and player_frame:
                            try:
                                act_btn = await player_frame.query_selector('button[aria-label*="play" i], .plyr__control[data-plyr="play"], .jw-icon-play, .vjs-big-play-button')
                                if act_btn:
                                    await act_btn.click(force=True)
                                    await asyncio.sleep(10.0)
                                    sample_c = await player_frame.evaluate('(()=>{const v=document.querySelector("video"); return v? v.currentTime : null;})()')
                                    if sample_b is not None and sample_c is not None and sample_c > sample_b + 0.5:
                                        playback_ok = True
                            except:
                                pass
                    except:
                        pass

                    # If playback still not OK, mark proxy as slow for future scheduling
                    if not playback_ok:
                        try:
                            self.proxy_pool.mark_slow(proxy)
                        except:
                            pass
                except Exception as e:
                    # Dump minimal DOM for debugging
                    try:
                        html = await page.content()
                        print(f"🔎 DOM snapshot (truncated): {html[:1000]}")
                    except:
                        pass
                    print(f"❌ Player not found: {e}")
                    await browser.close()
                    self.proxy_pool.record_request(proxy, False, time.time() - start_time)
                    return False

                # Attach minimal network logging for player beacons
                def _on_request(req):
                    try:
                        url = req.url
                        if ('dsvplay' in url) or ('dood' in url) or ('stat' in url) or ('log' in url) or ('beacon' in url):
                            print(f"📡 Request: {url}")
                    except:
                        pass
                def _on_response(resp):
                    try:
                        url = resp.url
                        if ('dsvplay' in url) or ('dood' in url) or ('stat' in url) or ('log' in url) or ('beacon' in url):
                            print(f"📩 Response: {url} -> {resp.status}")
                    except:
                        pass
                page.on('request', _on_request)
                page.on('response', _on_response)

                # Step 7: Simulate human viewing behavior
                print(f"👀 Simulating human viewing...")

                # Get video duration (main page or iframe)
                video_duration = None
                try:
                    video_duration = await page.evaluate('(()=>{const v=[...document.querySelectorAll("video:not([id^=exo-video])")][0]; return v? v.duration : undefined;})()')
                except:
                    pass
                if video_duration in (None, 0):
                    # Try inside an iframe if available
                    try:
                        frame_handles = await page.query_selector_all('iframe')
                        for fh in frame_handles:
                            frame = await fh.content_frame()
                            if not frame:
                                continue
                            dur = await frame.evaluate('(()=>{const v=[...document.querySelectorAll("video")][0]; return v? v.duration : undefined;})()')
                            if dur and dur > 0:
                                video_duration = dur
                                break
                    except:
                        pass
                if not video_duration or video_duration == 0:
                    video_duration = 60  # Default to 60 seconds

                # Generate viewing pattern
                viewing_actions = self.behavior_engine.generate_viewing_pattern(min(video_duration, 120))

                # Execute viewing actions
                for action in viewing_actions[:5]:  # Limit to first few actions
                    if action['action'] == 'watch':
                        watch_time = min(action['duration'], 45)  # Cap at 45 seconds for efficiency

                        # Simulate mouse movements during watching
                        for _ in range(random.randint(2, 5)):
                            start_pos = (random.randint(100, 1200), random.randint(100, 800))
                            end_pos = (random.randint(100, 1200), random.randint(100, 800))
                            trajectory = self.behavior_engine.generate_mouse_trajectory(start_pos, end_pos)

                            # Move mouse along trajectory
                            for point in trajectory[::5]:  # Sample every 5th point for speed
                                try:
                                    await page.mouse.move(point[0], point[1])
                                    await asyncio.sleep(0.05)
                                except:
                                    pass

                        # Watch video
                        print(f"   ⏱️  Watching for {watch_time:.1f} seconds...")
                        # Sample currentTime progression inside player iframe if available
                        try:
                            sample1 = None
                            sample2 = None
                            if 'player_frame' in locals() and player_frame:
                                sample1 = await player_frame.evaluate('(()=>{const v=document.querySelector("video"); return v? v.currentTime : null;})()')
                            # Allow more time for buffering on slow proxies (up to ~60s)
                            await asyncio.sleep(max(30.0, watch_time/2))
                            if 'player_frame' in locals() and player_frame:
                                sample2 = await player_frame.evaluate('(()=>{const v=document.querySelector("video"); return v? v.currentTime : null;})()')
                            if sample1 is not None and sample2 is not None:
                                print(f"   ⏱️  currentTime progressed: {sample1:.2f} -> {sample2:.2f}")
                        except:
                            pass
                        # Finish remaining watch time
                        remaining = max(0.0, watch_time - max(2.0, watch_time/2))
                        if remaining > 0:
                            await asyncio.sleep(remaining)

                    elif action['action'] == 'pause':
                        print(f"   ⏸️  Pausing...")
                        try:
                            await page.evaluate('document.querySelector("video").pause()')
                            await asyncio.sleep(action['duration'])
                            await page.evaluate('document.querySelector("video").play()')
                        except:
                            pass

                # Step 8: Calculate engagement score
                engagement = self.behavior_engine.calculate_engagement_score(viewing_actions)
                print(f"📊 Engagement score: {engagement:.1f}/100")

                # Step 9: Check if view registered (heuristic)
                response_time = time.time() - start_time
                success = response_time < 120 and engagement > 30

                if success:
                    print(f"✅ View #{view_number} completed successfully!")
                    self.stats['successful_views'] += 1
                    self.completed_views += 1
                else:
                    print(f"⚠️  View may not have registered (low engagement or timeout)")
                    self.stats['failed_attempts'] += 1

                # Record timing data
                timing_data = {
                    'inter_view_delay': 0,  # Will be set later
                    'response_time': response_time,
                    'engagement': engagement
                }
                self.adaptive_timing.record_attempt(timing_data, success)

                # Record proxy performance
                self.proxy_pool.record_request(proxy, success, response_time)

                # Close browser
                await browser.close()

                return success

        except Exception as e:
            print(f"❌ Critical error: {e}")
            self.stats['failed_attempts'] += 1
            self.proxy_pool.record_request(proxy, False, 0)
            return False

    async def run(self):
        """Main bot execution loop"""
        print(f"\n{'='*60}")
        print(f"🤖 ADVANCED DOODSTREAM BOT")
        print(f"{'='*60}")
        print(f"🎯 Target: {self.target_views} views")
        print(f"📹 Video: {self.video_url}")
        print(f"🌍 Proxies: {len(self.proxy_pool.proxies)}")
        print(f"{'='*60}\n")

        # Validate proxies first
        if len(self.proxy_pool.proxies) > 5:
            await self.validate_proxies()

        # Check if we have enough proxies
        if len(self.proxy_pool.proxies) < 10:
            print(f"⚠️  Warning: Only {len(self.proxy_pool.proxies)} proxies available")
            print(f"   Recommended: at least 50-100 residential proxies for best results")

        # Main loop
        while self.completed_views < self.target_views:
            view_number = self.completed_views + 1

            # Generate view
            success = await self.generate_single_view(view_number)

        # Adaptive delay before next view
        if success:
            optimal_delay = self.adaptive_timing.get_optimal_delay()
        else:
            # Longer delay after failure
            optimal_delay = random.uniform(180, 420)

        # Record delay in timing data
        self.adaptive_timing.successful_timings[-1]['inter_view_delay'] = optimal_delay if success else 0

            # Progress update
        if view_number % 5 == 0 or not success:
                self._print_stats()

            # Wait before next view
        if self.completed_views < self.target_views:
                print(f"\n⏳ Waiting {optimal_delay:.0f}s before next view (adaptive timing)...")
                await asyncio.sleep(optimal_delay)

        # Final statistics
        print(f"\n{'='*60}")
        print(f"✅ BOT COMPLETED!")
        print(f"{'='*60}")
        self._print_stats()

        # Proxy statistics
        proxy_stats = self.proxy_pool.get_stats_summary()
        print(f"\n📊 Proxy Pool Statistics:")
        print(f"   Total proxies: {proxy_stats['total_proxies']}")
        print(f"   Healthy: {proxy_stats['healthy_proxies']}")
        print(f"   Banned: {proxy_stats['banned_proxies']}")
        print(f"   Avg success rate: {proxy_stats['avg_success_rate']*100:.1f}%")

    def _print_stats(self):
        """Print current statistics"""
        runtime = time.time() - self.stats['start_time']
        success_rate = (self.stats['successful_views'] / self.stats['total_attempts'] * 100) if self.stats['total_attempts'] > 0 else 0

        print(f"\n📊 Current Statistics:")
        print(f"   Completed views: {self.completed_views}/{self.target_views}")
        print(f"   Success rate: {success_rate:.1f}%")
        print(f"   Total attempts: {self.stats['total_attempts']}")
        print(f"   Runtime: {runtime/60:.1f} minutes")
        print(f"   Avg time per view: {runtime/self.completed_views:.1f}s" if self.completed_views > 0 else "")


# ==== EXAMPLE USAGE (DO NOT RUN FOR ACTUAL FRAUD) ====

async def main():
    """
    Example configuration - FOR EDUCATIONAL PURPOSES ONLY
    """

    # Configuration
    VIDEO_URL = "https://www.desimaterial24.tech/video/cmiur5qqy0007106zsn0b6g5e"
    TARGET_VIEWS = 1000

    PROXY_LIST = [
    "216.26.235.151:3129",
    "104.207.55.5:3129",
    "209.50.161.101:3129",
    "104.207.41.88:3129",
    "209.50.172.226:3129",
    "104.207.62.139:3129",
    "45.3.39.216:3129",
    "209.50.171.159:3129",
    "209.50.169.233:3129",
    "209.50.173.10:3129",
    "209.50.189.98:3129",
    "45.3.35.221:3129",
    "216.26.250.224:3129",
    "209.50.166.49:3129",
    "209.50.172.61:3129",
    "45.3.35.41:3129",
    "104.167.25.95:3129",
    "216.26.254.158:3129",
    "45.3.39.168:3129",
    "65.111.3.172:3129",
    "65.111.25.111:3129",
    "209.50.174.77:3129",
    "104.207.61.13:3129",
    "193.56.28.172:3129",
    "104.207.51.181:3129",
    "104.207.38.130:3129",
    "65.111.4.229:3129",
    "104.207.33.171:3129",
    "65.111.23.143:3129",
    "216.26.228.34:3129",
    "104.207.56.19:3129",
    "209.50.161.118:3129",
    "216.26.242.7:3129",
    "209.50.164.178:3129",
    "209.50.175.153:3129",
    "104.207.62.164:3129",
    "104.167.19.115:3129",
    "104.167.19.22:3129",
    "209.50.185.203:3129",
    "209.50.171.50:3129",
    "216.26.248.97:3129",
    "104.207.59.39:3129",
    "104.207.60.166:3129",
    "45.3.38.69:3129",
    "209.50.177.69:3129",
    "216.26.243.149:3129",
    "193.56.28.136:3129",
    "65.111.8.248:3129",
    "45.3.62.45:3129",
    "209.50.162.123:3129",
    "209.50.166.126:3129",
    "104.207.60.227:3129",
    "216.26.239.74:3129",
    "216.26.250.162:3129",
    "45.3.45.140:3129",
    "216.26.240.204:3129",
    "216.26.239.207:3129",
    "209.50.185.73:3129",
    "45.3.41.77:3129",
    "154.213.160.92:3129",
    "104.207.46.150:3129",
    "45.3.51.231:3129",
    "209.50.189.91:3129",
    "45.3.49.170:3129",
    "216.26.228.207:3129",
    "216.26.252.253:3129",
    "45.3.36.92:3129",
    "65.111.6.158:3129",
    "65.111.21.87:3129",
    "65.111.3.47:3129",
    "104.207.52.65:3129",
    "65.111.2.217:3129",
    "216.26.246.45:3129",
    "45.3.42.173:3129",
    "45.3.49.197:3129",
    "45.3.43.86:3129",
    "216.26.236.100:3129",
    "209.50.163.36:3129",
    "216.26.226.235:3129",
    "45.3.43.1:3129",
    "209.50.174.162:3129",
    "154.213.165.127:3129",
    "154.213.160.6:3129",
    "104.207.62.233:3129",
    "209.50.184.58:3129",
    "65.111.25.125:3129",
    "45.3.35.110:3129",
    "209.50.182.220:3129",
    "45.3.53.200:3129",
    "45.3.41.154:3129",
    "104.207.37.253:3129",
    "209.50.184.65:3129",
    "209.50.177.87:3129",
    "104.207.59.66:3129",
    "45.3.52.48:3129",
    "104.207.61.5:3129",
    "45.3.33.36:3129",
    "65.111.22.160:3129",
    "104.207.60.228:3129",
    "104.207.42.152:3129"
]

    if len(PROXY_LIST) < 10:
        print("❌ ERROR: You need at least 10 residential proxies")
        print("   This bot requires high-quality residential proxy service")
        print("   Examples: Bright Data, Oxylabs, SmartProxy, etc.")
        print("   Cost: $50-500/month for sufficient proxy pool")
        return

    # Initialize bot
    bot = AdvancedDoodStreamBot(
        video_url=VIDEO_URL,
        proxy_list=PROXY_LIST,
        target_views=TARGET_VIEWS
    )

    await bot.run()


asyncio.run(main())

 

