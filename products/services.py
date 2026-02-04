"""
Service untuk mengambil data produk dari API eksternal Fast Print.

API URL: https://recruitment.fastprint.co.id/tes/api_tes_programmer
Authentication: Basic Auth
Password format: md5(bisacoding-DD-MM-YY)
"""

import requests
import hashlib
from datetime import datetime
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class FastPrintAPIService:
    """
    Service untuk komunikasi dengan API eksternal Fast Print.
    Handles authentication, request, dan response parsing.
    """
    
    API_URL = "https://recruitment.fastprint.co.id/tes/api_tes_programmer"
    
    @staticmethod
    def generate_password() -> str:
        """
        Generate password MD5 dengan format: bisacoding-DD-MM-YY
        
        Returns:
            str: MD5 hash dari password format
        """
        today = datetime.now()
        password_format = f"bisacoding-{today.strftime('%d-%m-%y')}"
        md5_hash = hashlib.md5(password_format.encode()).hexdigest()
        return md5_hash
    
    @staticmethod
    def generate_username() -> str:
        """
        Generate username dengan format: testprogrammerDDMMYYC##
        Format berubah setiap hari sesuai tanggal server.
        
        CATATAN: Username dapat diambil dari response header X-Credentials-Username
        jika API memberikan hint. Format default: testprogrammerDDMMYYC##
        
        Returns:
            str: Username untuk autentikasi
        """
        today = datetime.now()
        date_str = today.strftime('%d%m%y')
        # Default counter - biasanya berubah setiap hari (cek response header untuk nilai actual)
        # Hari ini (04-02-26) seharusnya C23 atau nomor lain sesuai server
        username = f"tesprogrammer{date_str}C23"
        return username
    
    @staticmethod
    def get_auth_headers(username: str) -> Dict[str, str]:
        """
        Generate Basic Auth header untuk API request.
        
        Args:
            username (str): Username untuk autentikasi
            
        Returns:
            Dict: Authorization header
        """
        import base64
        
        password = FastPrintAPIService.generate_password()
        credentials = f"{username}:{password}"
        encoded = base64.b64encode(credentials.encode()).decode()
        
        return {
            'Authorization': f'Basic {encoded}',
            'User-Agent': 'FastPrint-Django-Client/1.0'
        }
    
    @staticmethod
    def fetch_products(username: str = None) -> Optional[Dict]:
        """
        Fetch data produk dari API eksternal.
        CATATAN: API menggunakan METHOD POST dengan username & password di body
        
        Args:
            username (str): Username untuk autentikasi. Jika None, akan generate otomatis.
            
        Returns:
            Dict: Response dari API atau None jika gagal
        """
        try:
            # Generate username jika tidak disediakan
            if not username:
                username = FastPrintAPIService.generate_username()
            
            password = FastPrintAPIService.generate_password()
            
            # Prepare POST data
            data = {
                'username': username,
                'password': password
            }
            
            # Headers
            headers = {
                'User-Agent': 'FastPrint-Django-Client/1.0'
            }
            
            logger.info(f"Fetching from API with username: {username}")
            
            # NOTE: API memerlukan POST method dengan username & password di body
            response = requests.post(
                FastPrintAPIService.API_URL,
                data=data,
                headers=headers,
                timeout=10,
                verify=True  # Verify SSL certificate
            )
            
            response.raise_for_status()
            
            data = response.json()
            
            logger.info(f"Successfully fetched {len(data.get('data', []))} products from API")
            logger.debug(f"Response headers: {response.headers}")
            logger.debug(f"Response cookies: {response.cookies}")
            
            return data
            
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Connection error: {str(e)}")
            raise Exception("Tidak dapat terhubung ke API. Periksa koneksi internet.")
        
        except requests.exceptions.Timeout:
            logger.error("API request timeout")
            raise Exception("Request timeout. API tidak merespons dalam waktu yang ditentukan.")
        
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error: {e.response.status_code}")
            if e.response.status_code == 401:
                raise Exception("Autentikasi gagal. Username atau password salah.")
            elif e.response.status_code == 403:
                raise Exception("Anda tidak memiliki akses ke resource ini.")
            else:
                raise Exception(f"HTTP Error {e.response.status_code}")
        
        except ValueError as e:
            logger.error(f"JSON decode error: {str(e)}")
            raise Exception("Response dari API bukan format JSON yang valid.")
        
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise Exception(f"Error: {str(e)}")
    
    @staticmethod
    def parse_product_data(api_response: Dict) -> List[Dict]:
        """
        Parse dan transform response API ke format yang sesuai dengan model Product.
        
        Args:
            api_response (Dict): Response dari API
            
        Returns:
            List[Dict]: List of product data
        """
        products = []
        
        try:
            api_data = api_response.get('data', [])
            
            for item in api_data:
                product = {
                    'nama_produk': item.get('nama_produk', ''),
                    'harga': int(item.get('harga', 0)),
                    'kategori': item.get('kategori', ''),
                    'status': item.get('status', ''),
                }
                
                if product['nama_produk'] and product['harga'] > 0:
                    products.append(product)
            
            logger.info(f"Parsed {len(products)} valid products from API response")
            
        except Exception as e:
            logger.error(f"Error parsing product data: {str(e)}")
            raise Exception(f"Error parsing data: {str(e)}")
        
        return products
