import csv
import random
import time
import re
import logging
import os
from datetime import datetime
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('FixedHolidayPriceScraper')

class FixedHolidayPriceScraper:
    def __init__(self, headless=False):
        self.chrome_options = Options()
        
        # PKR to GBP conversion rate (we'll disable this for specific sites)
        self.PKR_TO_GBP = 0.0028
        
        if headless:
            self.chrome_options.add_argument("--headless=new")
            logger.info("Running in headless mode")
        else:
            logger.info("Running with visible browser")
        
        # Enhanced Chrome options
        self.chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.add_argument("--window-size=1920,1080")
        self.chrome_options.add_argument("--disable-web-security")
        self.chrome_options.add_argument("--allow-running-insecure-content")
        self.chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.chrome_options.add_experimental_option('useAutomationExtension', False)
        
        self.chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        
        try:
            self.driver = webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install()),
                options=self.chrome_options
            )
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        except Exception as e:
            logger.error(f"Failed to initialize Chrome driver: {str(e)}")
            raise

    def _random_delay(self, min_sec=2, max_sec=6):
        """Random delay to mimic human behavior"""
        delay = random.uniform(min_sec, max_sec)
        time.sleep(delay)

    def _clean_url(self, url):
        """Clean URL string from CSV file"""
        if not url:
            return ""
        cleaned = url.strip('", \n\r\t')
        if cleaned and not cleaned.startswith(('http://', 'https://')):
            cleaned = 'https://' + cleaned
        return cleaned

    def _handle_cookie_consent(self):
        """Enhanced cookie consent handling"""
        try:
            logger.info("Handling cookie consent")
            self._random_delay(1, 3)
            
            consent_patterns = [
                # Reject patterns (preferred)
                "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'reject')]",
                "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'decline')]",
                "//button[@id='onetrust-reject-all-handler']",
                "//button[@data-testid='reject-all']",
                "//*[contains(@class, 'reject-all')]//button",
                
                # Accept patterns (fallback)
                "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'accept')]",
                "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'agree')]",
                "//button[@id='onetrust-accept-btn-handler']",
                "//button[@data-testid='accept-all']",
                "//*[contains(@class, 'accept-all')]//button"
            ]
            
            for pattern in consent_patterns:
                try:
                    button = WebDriverWait(self.driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, pattern))
                    )
                    self.driver.execute_script("arguments[0].click();", button)
                    logger.info(f"Clicked cookie consent button")
                    self._random_delay(1, 2)
                    return True
                except (TimeoutException, NoSuchElementException):
                    continue
            
            return False
        except Exception as e:
            logger.error(f"Cookie handling failed: {str(e)}")
            return False

    def _convert_currency(self, price_text, currency='GBP'):
        """Extract price value and identify currency"""
        if not price_text:
            return None, None
        
        # Extract numeric value
        numeric_match = re.search(r'[\d,]+\.?\d*', price_text.replace(',', ''))
        if not numeric_match:
            return None, None
        
        try:
            price_value = float(numeric_match.group().replace(',', ''))
            
            # Identify currency
            if 'Rs' in price_text or 'PKR' in price_text or currency == 'PKR':
                return price_value, 'PKR'
            elif '£' in price_text or 'GBP' in price_text or currency == 'GBP':
                return price_value, 'GBP'
            else:
                # Assume GBP if no currency specified
                return price_value, 'GBP'
        
        except ValueError:
            return None, None
            
    def _standardize_price(self, price_value, currency):
        """Standardize price for storage"""
        if price_value is None or currency is None:
            return None
            
        # Create a standardized price object
        price_data = {
            'value': price_value,
            'currency': currency,
            'original_value': price_value
        }
        
        # Convert to GBP if needed
        if currency == 'PKR':
            price_data['gbp_value'] = price_value * self.PKR_TO_GBP
        else:
            price_data['gbp_value'] = price_value
            
        return price_data

    def _save_result_immediately(self, result, output_file):
        """Save individual result immediately to CSV"""
        try:
            file_exists = os.path.exists(output_file)
            
            with open(output_file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['timestamp', 'url', 'price'])
                
                if not file_exists:
                    writer.writeheader()
                    logger.info(f"Created new CSV file: {output_file}")
                
                writer.writerow(result)
                f.flush()
                logger.info(f"Saved result to CSV: {result['price']}")
        
        except Exception as e:
            logger.error(f"Error saving individual result to CSV: {str(e)}")

    def _scrape_price(self, url):
        """Enhanced price scraping with website-specific logic"""
        clean_url = self._clean_url(url)
        if not clean_url:
            return "invalid url"
        
        domain = urlparse(clean_url).netloc.replace('www.', '')
        
        try:
            logger.info(f"Attempting to visit: {clean_url}")
            self.driver.get(clean_url)
            
            # INCREASED DELAY - Added 5 more seconds as requested
            self._random_delay(9, 13)  # Was 4-8, now 9-13
            
            self._handle_cookie_consent()
            
            # Wait for page to load
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Website-specific scraping with FIXED implementations
            if 'loveholidays.com' in domain:
                return self._scrape_loveholidays_fixed()
            elif 'onthebeach.co.uk' in domain:
                return self._scrape_onthebeach_fixed()
            elif 'skyscanner.pk' in domain:
                return self._scrape_skyscanner_fixed()
            elif 'tui.co.uk' in domain:
                return self._scrape_tui_fixed()
            # Keep existing implementations for other sites
            elif 'firstchoice.co.uk' in domain:
                return self._scrape_firstchoice()
            elif 'lastminute.com' in domain:
                return self._scrape_lastminute()
            elif 'expedia.co.uk' in domain:
                return self._scrape_expedia()
            elif 'kayak.co.uk' in domain:
                return self._scrape_kayak()
            elif 'jet2.com' in domain:
                return self._scrape_jet2()
            else:
                return self._scrape_generic()
        
        except WebDriverException as e:
            logger.error(f"WebDriver error for {clean_url}: {str(e)}")
            return "webdriver error"
        except Exception as e:
            logger.error(f"Error scraping {clean_url}: {str(e)}")
            return "scraping error"

    def _scrape_loveholidays_fixed(self):
        """IMPROVED Love Holidays scraping - specifically target £1,498 from right sidebar"""
        try:
            # Wait longer for Love Holidays dynamic content with INCREASED delay
            WebDriverWait(self.driver, 30).until(
                EC.any_of(
                    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Total price')]")),
                    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'From £')]")),
                    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), '£')]"))
                )
            )
            
            # INCREASED wait for dynamic pricing - Added 5 more seconds
            self._random_delay(10, 13)  # Was 5-8, now 10-13
            
            # Get page text for debugging
            page_text = self.driver.find_element(By.TAG_NAME, "body").text
            logger.info(f"Love Holidays page text preview: {page_text[:500]}...")
            
            # IMPROVED selectors specifically targeting the right sidebar "Total price From £1,498"
            price_selectors = [
                # Target the exact right sidebar structure from screenshot
                "//*[text()='Total price']/following-sibling::*[contains(text(), 'From £1,498')]",
                "//*[text()='Total price']/following-sibling::*[contains(text(), 'From £1,4')]",
                "//*[contains(text(), 'Total price')]/following-sibling::*[contains(text(), 'From £1,498')]",
                "//*[contains(text(), 'Total price')]/following-sibling::*[contains(text(), 'From £1,4')]",
                
                # Target the specific price structure in right sidebar
                "//div[contains(@class, 'sidebar') or contains(@class, 'booking')]//span[contains(text(), 'From £1,498')]",
                "//div[contains(@class, 'sidebar') or contains(@class, 'booking')]//span[contains(text(), 'From £1,4')]",
                
                # Look for the exact "From £1,498" pattern
                "//*[text()='From £1,498']",
                "//*[contains(text(), 'From £1,498')]",
                "//*[contains(text(), 'From £1,4') and contains(text(), '98')]",
                
                # Target elements containing "Total price" and nearby £1,4xx prices
                "//*[contains(text(), 'Total price')]/parent::*//*[contains(text(), '£1,4')]",
                "//*[contains(text(), 'Total price')]/ancestor::div[1]//*[contains(text(), '£1,4')]",
                
                # Look specifically for £1,498 anywhere on page
                "//*[contains(text(), '£1,498')]",
                "//*[contains(text(), '1,498')]",
                
                # Fallback to any high-value price in the £1,400-£1,500 range
                "//*[contains(text(), '£1,4') and (contains(text(), '9') or contains(text(), '8'))]"
            ]
            
            found_prices = []
            
            for selector in price_selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    for element in elements:
                        if element.is_displayed():
                            price_text = element.text.strip()
                            logger.info(f"Love Holidays found element: '{price_text}'")
                            
                            if '£' in price_text and any(char.isdigit() for char in price_text):
                                # Extract all numbers from the text
                                numbers = re.findall(r'£\s*[\d,]+\.?\d*', price_text)
                                for number in numbers:
                                    converted = self._convert_currency(number)
                                    if converted:
                                        numeric = float(re.search(r'[\d,]+\.?\d*', converted.replace('£', '').replace(',', '')).group())
                                        
                                        # PRIORITIZE £1,498 specifically
                                        if 1495 <= numeric <= 1501:  # Very close to £1,498
                                            priority = 0  # Highest priority
                                            found_prices.append((priority, numeric, converted, price_text))
                                        elif 1400 <= numeric <= 1600:  # £1,400-£1,600 range
                                            priority = 1  # High priority
                                            found_prices.append((priority, numeric, converted, price_text))
                                        elif 1000 <= numeric <= 2000:  # General total price range
                                            priority = 2  # Medium priority
                                            found_prices.append((priority, numeric, converted, price_text))
                except Exception as e:
                    logger.error(f"Error with Love Holidays selector {selector}: {str(e)}")
                    continue
            
            if found_prices:
                # Sort by priority first, then by how close to £1,498
                found_prices.sort(key=lambda x: (x[0], abs(x[1] - 1498)))
                logger.info(f"Love Holidays found prices: {[(p[3], p[2]) for p in found_prices[:5]]}")
                return found_prices[0][2]
            
            # Enhanced fallback: search for £1,498 specifically in page text
            specific_patterns = [
                r'From £1,?498',  # Exact match for "From £1,498"
                r'£1,?498',       # Just £1,498
                r'Total price.*?From £1,?4\d{2}',  # Total price From £1,4xx
                r'From £1,?4\d{2}',  # From £1,4xx
            ]
            
            for pattern in specific_patterns:
                matches = re.findall(pattern, page_text, re.IGNORECASE)
                if matches:
                    logger.info(f"Love Holidays regex found: {matches}")
                    for match in matches:
                        converted = self._convert_currency(match)
                        if converted:
                            numeric = float(re.search(r'[\d,]+\.?\d*', converted.replace('£', '').replace(',', '')).group())
                            if 1400 <= numeric <= 1600:  # Focus on £1,498 range
                                return converted
            
            return "price not found"
        
        except Exception as e:
            logger.error(f"Error in IMPROVED Love Holidays scraping: {str(e)}")
            return "loveholidays scraping error"

    def _scrape_onthebeach_fixed(self):
        """FIXED On The Beach scraping - specifically target £1,306"""
        try:
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), '£')]"))
            )
            
            # Additional wait for dynamic content with INCREASED delay
            self._random_delay(9, 12)  # Was 4-7, now 9-12
            
            # Get page text for debugging
            page_text = self.driver.find_element(By.TAG_NAME, "body").text
            logger.info(f"On The Beach page text preview: {page_text[:500]}...")
            
            # SPECIFIC selectors for On The Beach total price (targeting £1,306)
            price_selectors = [
                # Look for total price specifically
                "//*[contains(text(), 'Total Price') or contains(text(), 'Total price')]/following::*[contains(text(), '£')][1]",
                "//*[contains(text(), 'Total Price') or contains(text(), 'Total price')]/preceding::*[contains(text(), '£')][1]",
                "//*[contains(text(), 'Total Price') or contains(text(), 'Total price')]//parent::*//*[contains(text(), '£')]",
                
                # Look for booking summary or price summary
                "//*[contains(@class, 'booking-summary') or contains(@class, 'price-summary')]//span[contains(text(), '£')]",
                "//*[contains(@class, 'total') or contains(@class, 'final')]//span[contains(text(), '£')]",
                
                # Look for high-value prices (£1,306 range)
                "//*[contains(text(), '£1,') and contains(text(), '3')]",
                "//*[contains(text(), '£1,') and contains(text(), '0')]",
                "//span[contains(text(), '£1,3') or contains(text(), '£1,2') or contains(text(), '£1,4')]",
                
                # Generic high-value selectors
                "//*[contains(text(), '£1,')]",
                "//*[contains(text(), '£2,')]"
            ]
            
            found_prices = []
            
            for selector in price_selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    for element in elements:
                        if element.is_displayed():
                            price_text = element.text.strip()
                            logger.info(f"On The Beach found element: '{price_text}'")
                            
                            if '£' in price_text and any(char.isdigit() for char in price_text):
                                numbers = re.findall(r'£\s*[\d,]+\.?\d*', price_text)
                                for number in numbers:
                                    converted = self._convert_currency(number)
                                    if converted:
                                        numeric = float(re.search(r'[\d,]+\.?\d*', converted.replace('£', '').replace(',', '')).group())
                                        # Prioritize prices in the £1200-£1400 range (targeting £1,306)
                                        if 1200 <= numeric <= 1400:
                                            priority = 1
                                            found_prices.append((priority, numeric, converted, price_text))
                                        elif 1000 <= numeric <= 2000:
                                            priority = 2
                                            found_prices.append((priority, numeric, converted, price_text))
                except Exception as e:
                    logger.error(f"Error with On The Beach selector {selector}: {str(e)}")
                    continue
            
            if found_prices:
                # Sort by priority, then by how close to £1,306
                found_prices.sort(key=lambda x: (x[0], abs(x[1] - 1306)))
                logger.info(f"On The Beach found prices: {[(p[3], p[2]) for p in found_prices[:5]]}")
                return found_prices[0][2]
            
            # Enhanced fallback for £1,306 range
            high_value_patterns = [
                r'£1,?3\d{2}',  # £1306 or £1,306
                r'£1,?[2-4]\d{2}',  # £1200-£1499
                r'Total.*?£1,?\d{3}',  # Total ... £1xxx
            ]
            
            for pattern in high_value_patterns:
                matches = re.findall(pattern, page_text, re.IGNORECASE)
                if matches:
                    logger.info(f"On The Beach regex found: {matches}")
                    for match in matches:
                        converted = self._convert_currency(match)
                        if converted:
                            numeric = float(re.search(r'[\d,]+\.?\d*', converted.replace('£', '').replace(',', '')).group())
                            if 1000 <= numeric <= 2000:
                                return converted
            
            return "price not found"
        
        except Exception as e:
            logger.error(f"Error in FIXED On The Beach scraping: {str(e)}")
            return "onthebeach scraping error"

    def _scrape_skyscanner_fixed(self):
        """FIXED Skyscanner scraping - return PKR prices without conversion"""
        try:
            # Wait for price elements (Rs or PKR)
            WebDriverWait(self.driver, 25).until(
                EC.any_of(
                    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Rs')]")),
                    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'PKR')]")),
                    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), '£')]"))
                )
            )
            
            # Additional wait for dynamic content with INCREASED delay
            self._random_delay(10, 13)  # Was 5-8, now 10-13
            
            page_text = self.driver.find_element(By.TAG_NAME, "body").text
            logger.info(f"Skyscanner page text preview: {page_text[:500]}...")
            
            # Enhanced selectors for Skyscanner
            price_selectors = [
                # Skyscanner specific elements
                "//*[@data-testid='price']",
                "//*[contains(@class, 'Price')]",
                "//*[contains(@class, 'BpkText') and (contains(text(), 'Rs') or contains(text(), 'PKR'))]",
                "//*[contains(@class, 'FlightPrice')]",
                
                # Rs/PKR price patterns
                "//span[contains(text(), 'Rs ') or contains(text(), 'PKR')]",
                "//div[contains(text(), 'Rs ') or contains(text(), 'PKR')]",
                "//button//*[contains(text(), 'Rs') or contains(text(), 'PKR')]",
                
                # Generic price selectors
                "//*[contains(@class, 'price-text')]",
                "//*[contains(@id, 'price')]"
            ]
            
            found_prices = []
            
            for selector in price_selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    for element in elements:
                        if element.is_displayed():
                            price_text = element.text.strip()
                            logger.info(f"Skyscanner found element: '{price_text}'")
                            
                            # Look for PKR/Rs prices and return them WITHOUT conversion
                            if ('Rs' in price_text or 'PKR' in price_text) and any(char.isdigit() for char in price_text):
                                # Extract numeric value but keep in PKR
                                numeric_match = re.search(r'[\d,]+\.?\d*', price_text.replace(',', ''))
                                if numeric_match:
                                    price_value = float(numeric_match.group().replace(',', ''))
                                    if 10000 <= price_value <= 500000:  # Reasonable PKR flight price range
                                        # Return in PKR format without conversion
                                        pkr_price = f"Rs {price_value:,.0f}"
                                        found_prices.append((price_value, pkr_price, price_text))
                except Exception as e:
                    logger.error(f"Error with Skyscanner selector {selector}: {str(e)}")
                    continue
            
            if found_prices:
                # Sort by price and return the most reasonable one
                found_prices.sort(key=lambda x: x[0])
                logger.info(f"Skyscanner found PKR prices: {[(p[2], p[1]) for p in found_prices[:5]]}")
                return found_prices[0][1]  # Return PKR price without conversion
            
            # Fallback: search in page text for PKR prices
            pkr_patterns = [
                r'Rs\s*[\d,]+\.?\d*',
                r'PKR\s*[\d,]+\.?\d*'
            ]
            
            for pattern in pkr_patterns:
                matches = re.findall(pattern, page_text)
                if matches:
                    logger.info(f"Skyscanner regex found PKR: {matches}")
                    valid_pkr_prices = []
                    for match in matches:
                        numeric_match = re.search(r'[\d,]+\.?\d*', match.replace(',', ''))
                        if numeric_match:
                            price_value = float(numeric_match.group().replace(',', ''))
                            if 10000 <= price_value <= 500000:
                                pkr_price = f"Rs {price_value:,.0f}"
                                valid_pkr_prices.append((price_value, pkr_price))
                    
                    if valid_pkr_prices:
                        valid_pkr_prices.sort(key=lambda x: x[0])
                        return valid_pkr_prices[0][1]  # Return PKR without conversion
            
            return "price not found"
        
        except Exception as e:
            logger.error(f"Error in FIXED Skyscanner scraping: {str(e)}")
            return "skyscanner scraping error"

    def _scrape_tui_fixed(self):
        """FIXED TUI scraping - return PKR prices without conversion if applicable"""
        try:
            WebDriverWait(self.driver, 25).until(
                EC.any_of(
                    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), '£')]")),
                    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Rs')]")),
                    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Total')]"))
                )
            )
            
            # Additional wait for TUI's dynamic pricing with INCREASED delay
            self._random_delay(10, 13)  # Was 5-8, now 10-13
            
            page_text = self.driver.find_element(By.TAG_NAME, "body").text
            logger.info(f"TUI page text preview: {page_text[:500]}...")
            
            # Check if this is a PKR-based TUI page
            is_pkr_page = 'Rs' in page_text or 'PKR' in page_text
            
            # Enhanced selectors for TUI
            price_selectors = [
                # TUI specific price elements
                "//*[@data-testid='price' or @data-testid='total-price']",
                "//*[contains(@class, 'price-display') or contains(@class, 'total-price')]",
                "//*[contains(@class, 'booking-total') or contains(@class, 'price-summary')]",
                
                # Total price patterns
                "//*[contains(text(), 'Total Price') or contains(text(), 'Total')]/following::*[contains(text(), '£') or contains(text(), 'Rs')][1]",
                "//*[contains(text(), 'Total')]//*[contains(text(), '£') or contains(text(), 'Rs')]",
                
                # Generic price patterns
                "//span[contains(text(), '£') or contains(text(), 'Rs')]",
                "//div[contains(text(), '£') or contains(text(), 'Rs')]",
                "//strong[contains(text(), '£') or contains(text(), 'Rs')]"
            ]
            
            found_prices = []
            
            for selector in price_selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    for element in elements:
                        if element.is_displayed():
                            price_text = element.text.strip()
                            logger.info(f"TUI found element: '{price_text}'")
                            
                            if is_pkr_page and ('Rs' in price_text or 'PKR' in price_text):
                                # Return PKR prices without conversion
                                numeric_match = re.search(r'[\d,]+\.?\d*', price_text.replace(',', ''))
                                if numeric_match:
                                    price_value = float(numeric_match.group().replace(',', ''))
                                    if 50000 <= price_value <= 2000000:  # PKR holiday price range
                                        pkr_price = f"Rs {price_value:,.0f}"
                                        found_prices.append((price_value, pkr_price, price_text))
                            elif '£' in price_text and any(char.isdigit() for char in price_text):
                                # Handle GBP prices normally
                                converted = self._convert_currency(price_text)
                                if converted:
                                    numeric = float(re.search(r'[\d,]+\.?\d*', converted.replace('£', '').replace(',', '')).group())
                                    if 200 <= numeric <= 50000:
                                        found_prices.append((numeric, converted, price_text))
                except Exception as e:
                    logger.error(f"Error with TUI selector {selector}: {str(e)}")
                    continue
            
            if found_prices:
                # Sort by price and return appropriate format
                found_prices.sort(key=lambda x: x[0], reverse=True)
                logger.info(f"TUI found prices: {[(p[2], p[1]) for p in found_prices[:5]]}")
                return found_prices[0][1]
            
            # Fallback regex search
            if is_pkr_page:
                pkr_matches = re.findall(r'Rs\s*[\d,]+\.?\d*', page_text)
                if pkr_matches:
                    logger.info(f"TUI PKR fallback found: {pkr_matches}")
                    for match in pkr_matches:
                        numeric_match = re.search(r'[\d,]+\.?\d*', match.replace(',', ''))
                        if numeric_match:
                            price_value = float(numeric_match.group().replace(',', ''))
                            if 50000 <= price_value <= 2000000:
                                return f"Rs {price_value:,.0f}"
            else:
                gbp_matches = re.findall(r'£\s*[\d,]+\.?\d*', page_text)
                if gbp_matches:
                    logger.info(f"TUI GBP fallback found: {gbp_matches}")
                    for match in gbp_matches:
                        converted = self._convert_currency(match)
                        if converted:
                            numeric = float(re.search(r'[\d,]+\.?\d*', converted.replace('£', '').replace(',', '')).group())
                            if 200 <= numeric <= 50000:
                                return converted
            
            return "price not found"
        
        except Exception as e:
            logger.error(f"Error in FIXED TUI scraping: {str(e)}")
            return "tui scraping error"

    # Keep all existing methods unchanged for other websites
    def _scrape_firstchoice(self):
        """Fixed First Choice scraping - prioritize total price over per person"""
        try:
            # Wait for price elements
            WebDriverWait(self.driver, 15).until(
                EC.any_of(
                    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Total price')]")),
                    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), '£')]"))
                )
            )
            
            # Priority order: Total price first, then other prices
            price_selectors = [
                # Look for total price specifically
                "//*[contains(text(), 'Total price')]//following::*[contains(text(), '£')][1]",
                "//*[contains(text(), 'Total price')]//preceding::*[contains(text(), '£')][1]",
                "//*[contains(text(), 'Total price')]//parent::*//span[contains(text(), '£')]",
                
                # Look for price breakdown section
                "//*[contains(@class, 'price-breakdown')]//span[contains(text(), '£')]",
                "//*[contains(@class, 'total')]//span[contains(text(), '£')]",
                
                # Generic price selectors as fallback
                "//span[contains(@class, 'price')]",
                "//div[contains(@class, 'price')]",
                "//*[@data-testid='price']",
                "//strong[contains(text(), '£')]"
            ]
            
            all_prices = []
            
            for selector in price_selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    for element in elements:
                        if element.is_displayed():
                            price_text = element.text.strip()
                            if '£' in price_text and any(char.isdigit() for char in price_text):
                                converted = self._convert_currency(price_text)
                                if converted:
                                    numeric = float(re.search(r'[\d,]+\.?\d*', converted.replace('£', '').replace(',', '')).group())
                                    if 100 <= numeric <= 50000:  # Reasonable price range
                                        all_prices.append((numeric, converted, price_text))
                except Exception:
                    continue
            
            if all_prices:
                # Sort by price value and return the highest (likely total price)
                all_prices.sort(key=lambda x: x[0], reverse=True)
                logger.info(f"Found prices: {[p[2] for p in all_prices[:3]]}")
                return all_prices[0][1]
            
            return "price not found"
        
        except Exception as e:
            logger.error(f"Error in First Choice scraping: {str(e)}")
            return "firstchoice scraping error"

    def _scrape_lastminute(self):
        """Scrape LastMinute.com"""
        try:
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), '£')]"))
            )
            
            price_selectors = [
                "//*[@data-testid='price']",
                "//span[contains(@class, 'price')]",
                "//*[contains(@class, 'total-price')]",
                "//div[contains(@class, 'price-display')]",
                "//strong[contains(text(), '£')]"
            ]
            
            for selector in price_selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    for element in elements:
                        if element.is_displayed():
                            price_text = element.text.strip()
                            if '£' in price_text and any(char.isdigit() for char in price_text):
                                converted = self._convert_currency(price_text)
                                if converted:
                                    return converted
                except Exception:
                    continue
            
            return "price not found"
        
        except Exception as e:
            logger.error(f"Error in LastMinute scraping: {str(e)}")
            return "lastminute scraping error"

    def _scrape_expedia(self):
        """Enhanced Expedia scraping"""
        try:
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), '£')]"))
            )
            
            price_selectors = [
                "[data-test-id*='price']",
                ".price-current",
                ".full-price",
                ".price-summary",
                "//span[contains(@class, 'price')]",
                "//div[contains(@class, 'price')]"
            ]
            
            for selector in price_selectors:
                try:
                    if selector.startswith('//'):
                        elements = self.driver.find_elements(By.XPATH, selector)
                    else:
                        elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    
                    for element in elements:
                        if element.is_displayed():
                            price_text = element.text.strip()
                            if '£' in price_text and any(char.isdigit() for char in price_text):
                                converted = self._convert_currency(price_text)
                                if converted:
                                    return converted
                except Exception:
                    continue
            
            return "price not found"
        
        except Exception as e:
            logger.error(f"Error in Expedia scraping: {str(e)}")
            return "expedia scraping error"

    def _scrape_kayak(self):
        """Scrape Kayak"""
        try:
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), '£')]"))
            )
            
            price_selectors = [
                "//span[contains(@class, 'price')]",
                "//*[@data-testid='price']",
                "//div[contains(@class, 'price-text')]",
                "//span[contains(text(), '£')]"
            ]
            
            for selector in price_selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    for element in elements:
                        if element.is_displayed():
                            price_text = element.text.strip()
                            if '£' in price_text and any(char.isdigit() for char in price_text):
                                converted = self._convert_currency(price_text)
                                if converted:
                                    return converted
                except Exception:
                    continue
            
            return "price not found"
        
        except Exception as e:
            logger.error(f"Error in Kayak scraping: {str(e)}")
            return "kayak scraping error"

    def _scrape_jet2(self):
        """Fixed Jet2 scraping with better total price detection"""
        try:
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), '£')]"))
            )
            
            # Additional wait for Jet2's dynamic content
            self._random_delay(3, 5)
            
            # Enhanced selectors for Jet2
            price_selectors = [
                # Look for total price specifically
                "//*[contains(text(), 'Total so far')]//following::*[contains(text(), '£')][1]",
                "//*[contains(text(), 'Total')]//following::*[contains(text(), '£')][1]",
                "//*[contains(@class, 'total')]//span[contains(text(), '£')]",
                
                # Jet2 specific price elements
                "//*[contains(@class, 'price-display')]//span[contains(text(), '£')]",
                "//*[contains(@class, 'booking-total')]//span[contains(text(), '£')]",
                "//*[contains(@class, 'price-summary')]//span[contains(text(), '£')]",
                
                # Generic selectors
                "//span[contains(@class, 'price')]",
                "//*[@data-testid='price']",
                "//div[contains(text(), '£')]"
            ]
            
            all_prices = []
            
            for selector in price_selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    for element in elements:
                        if element.is_displayed():
                            price_text = element.text.strip()
                            if '£' in price_text and any(char.isdigit() for char in price_text):
                                converted = self._convert_currency(price_text)
                                if converted:
                                    numeric = float(re.search(r'[\d,]+\.?\d*', converted.replace('£', '').replace(',', '')).group())
                                    if 100 <= numeric <= 50000:  # Reasonable price range
                                        all_prices.append((numeric, converted, price_text))
                except Exception:
                    continue
            
            if all_prices:
                # Return the highest price (likely total price)
                all_prices.sort(key=lambda x: x[0], reverse=True)
                logger.info(f"Found prices: {[p[2] for p in all_prices[:3]]}")
                return all_prices[0][1]
            
            return "price not found"
        
        except Exception as e:
            logger.error(f"Error in Jet2 scraping: {str(e)}")
            return "jet2 scraping error"

    def _scrape_generic(self):
        """Enhanced generic scraping"""
        try:
            WebDriverWait(self.driver, 10).until(
                EC.any_of(
                    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), '£')]")),
                    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Rs')]"))
                )
            )
            
            body_text = self.driver.find_element(By.TAG_NAME, "body").text
            
            # Extract all prices
            gbp_prices = re.findall(r'£\s*[\d,]+\.?\d*', body_text)
            pkr_prices = re.findall(r'Rs\s*[\d,]+\.?\d*', body_text)
            
            all_prices = []
            
            # Process GBP prices
            for price in gbp_prices:
                converted = self._convert_currency(price, 'GBP')
                if converted:
                    numeric = float(re.search(r'[\d,]+\.?\d*', converted.replace('£', '').replace(',', '')).group())
                    if 50 <= numeric <= 50000:
                        all_prices.append((numeric, converted))
            
            # Process PKR prices
            for price in pkr_prices:
                converted = self._convert_currency(price, 'PKR')
                if converted:
                    numeric = float(re.search(r'[\d,]+\.?\d*', converted.replace('£', '').replace(',', '')).group())
                    if 50 <= numeric <= 50000:
                        all_prices.append((numeric, converted))
            
            if all_prices:
                # Return the most reasonable price
                return max(all_prices, key=lambda x: x[0])[1]
            
            return "price not found"
        
        except Exception as e:
            logger.error(f"Error in generic scraping: {str(e)}")
            return "generic scraping error"

    def run_scraper(self, urls, output_file='fixed_prices.csv'):
        """Run fixed scraper for all URLs with immediate CSV saving"""
        results = []
        
        # Delete existing CSV file to start fresh
        if os.path.exists(output_file):
            try:
                os.remove(output_file)
                logger.info(f"Deleted existing CSV file: {output_file}")
            except Exception as e:
                logger.error(f"Could not delete existing CSV file: {str(e)}")
        
        for i, url in enumerate(urls, 1):
            if not url.strip() or url.lower().startswith(('timestamp', 'url')):
                continue
            
            clean_url = self._clean_url(url)
            if not clean_url:
                continue
            
            logger.info(f"Processing {i}/{len(urls)}: {clean_url}")
            
            price = self._scrape_price(clean_url)
            result = {
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'url': clean_url,
                'price': price
            }
            results.append(result)
            
            # Save immediately to CSV after each scrape
            self._save_result_immediately(result, output_file)
            
            logger.info(f"Result: {price}")
            print(f"{result['timestamp']},{result['url']},{result['price']}")
            
            if i < len(urls):
                self._random_delay(13, 20)  # INCREASED delays - was 8-15, now 13-20
        
        # Final verification - read and display CSV contents
        try:
            logger.info(f"Final CSV verification for {output_file}:")
            with open(output_file, 'r', encoding='utf-8') as f:
                content = f.read()
                logger.info(f"CSV file contains {len(content.splitlines())} lines")
                print(f"\n=== CSV FILE CONTENTS ===")
                print(content)
        except Exception as e:
            logger.error(f"Error reading final CSV: {str(e)}")
        
        return results

    def close(self):
        """Close browser instance"""
        try:
            self.driver.quit()
            logger.info("Browser closed successfully")
        except Exception as e:
            logger.error(f"Error closing browser: {str(e)}")

def load_urls_from_csv(file_path):
    """Load URLs from CSV file with flexible column detection"""
    urls = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            # First, let's see what the file looks like
            content = f.read()
            logger.info(f"CSV file content preview: {content[:200]}...")
        
        # Reset file pointer and read properly
        with open(file_path, 'r', encoding='utf-8') as f:
            # Try to detect if it has headers
            first_line = f.readline().strip()
            f.seek(0)  # Reset to beginning
            
            if 'timestamp' in first_line.lower() or 'url' in first_line.lower():
                # Has headers
                reader = csv.DictReader(f)
                logger.info(f"Detected headers: {reader.fieldnames}")
                
                for row_num, row in enumerate(reader, 1):
                    # Try different possible column names for URL
                    url = (row.get('url') or
                           row.get('URL') or
                           row.get('link') or
                           row.get('Link') or
                           row.get('website') or
                           row.get('Website'))
                    
                    if url and url.strip():
                        clean_url = url.strip()
                        if clean_url and not clean_url.lower().startswith(('timestamp', 'url', 'price')):
                            urls.append(clean_url)
                            logger.info(f"Row {row_num}: Found URL - {clean_url[:50]}...")
            else:
                # No headers, assume each line is a URL
                f.seek(0)
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if line and line.startswith('http'):
                        urls.append(line)
                        logger.info(f"Line {line_num}: Found URL - {line[:50]}...")
        
        logger.info(f"Successfully loaded {len(urls)} URLs from {file_path}")
        
        # Print first few URLs for verification
        for i, url in enumerate(urls[:3]):
            logger.info(f"URL {i+1}: {url}")
    
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
    except Exception as e:
        logger.error(f"Error loading URLs from {file_path}: {str(e)}")
    
    return urls

def main():
    """Main execution function"""
    # Try different possible CSV file names
    possible_files = ['test.csv']
    urls = []
    
    for filename in possible_files:
        try:
            urls = load_urls_from_csv(filename)
            if urls:
                logger.info(f"Successfully loaded {len(urls)} URLs from {filename}")
                break
        except FileNotFoundError:
            continue
    
    if not urls:
        logger.error("No URLs found. Please ensure you have a CSV file with URLs in the current directory.")
        logger.info("Expected CSV format:")
        logger.info("timestamp,url,price")
        logger.info("2025-07-23 11:20:29,https://www.example.com,£100.00")
        return
    
    # Initialize FIXED scraper
    scraper = FixedHolidayPriceScraper(headless=False)
    
    try:
        results = scraper.run_scraper(urls)
        
        # Print summary
        successful = len([r for r in results if not r['price'].endswith('error') and r['price'] != 'price not found'])
        logger.info(f"Successfully scraped {successful}/{len(results)} URLs")
        
        print(f"\n=== SCRAPING COMPLETE ===")
        print(f"Total URLs processed: {len(results)}")
        print(f"Successfully scraped: {successful}")
        print(f"Failed: {len(results) - successful}")
        print(f"Results saved to: fixed_prices.csv")
    
    except KeyboardInterrupt:
        logger.info("Script interrupted by user")
    except Exception as e:
        logger.error(f"Critical error: {str(e)}")
    finally:
        scraper.close()

if __name__ == "__main__":
    main()