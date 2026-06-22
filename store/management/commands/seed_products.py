from django.core.management.base import BaseCommand

from store.models import Category, Product


class Command(BaseCommand):
    help = 'Seed the database with sample products (Indian market prices in INR)'

    def handle(self, *args, **options):
        categories_data = [
            {'name': 'Electronics', 'slug': 'electronics'},
            {'name': 'Fashion', 'slug': 'fashion'},
            {'name': 'Home & Living', 'slug': 'home-living'},
            {'name': 'Sports & Fitness', 'slug': 'sports'},
        ]

        for cat_data in categories_data:
            Category.objects.update_or_create(slug=cat_data['slug'], defaults=cat_data)

        products_data = [
            {
                'name': 'boAt Rockerz 450 Wireless Headphones',
                'slug': 'wireless-bluetooth-headphones',
                'category': 'electronics',
                'description': 'India\'s favourite wireless headphones with 15-hour playback, dual connectivity, and signature boAt sound. Lightweight design perfect for daily commute and WFH.',
                'price': 1499,
                'stock': 25,
                'image_url': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400',
            },
            {
                'name': 'Noise ColorFit Pro 4 Smart Watch',
                'slug': 'smart-watch-pro',
                'category': 'electronics',
                'description': 'Made-in-India smartwatch with AMOLED display, Bluetooth calling, SpO2 monitor, and 7-day battery. Water resistant with 100+ watch faces.',
                'price': 3999,
                'stock': 15,
                'image_url': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400',
            },
            {
                'name': 'Portronics My Buddy K9 Laptop Stand',
                'slug': 'laptop-stand-aluminum',
                'category': 'electronics',
                'description': 'Adjustable aluminium laptop stand with 7 height levels. Improves posture, keeps laptop cool, and fits all devices from 11" to 17".',
                'price': 899,
                'stock': 40,
                'image_url': 'https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=400',
            },
            {
                'name': 'Roadster Men\'s Denim Jacket',
                'slug': 'classic-denim-jacket',
                'category': 'fashion',
                'description': 'Classic blue denim jacket from Roadster. Premium cotton fabric, regular fit, button closure with chest pockets. Perfect for casual outings.',
                'price': 2199,
                'stock': 30,
                'image_url': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400',
            },
            {
                'name': 'Puma Softride Running Shoes',
                'slug': 'running-sneakers',
                'category': 'fashion',
                'description': 'Lightweight Puma running shoes with soft foam cushioning and breathable mesh upper. Ideal for morning jogs, gym sessions, and everyday wear.',
                'price': 3499,
                'stock': 20,
                'image_url': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400',
            },
            {
                'name': 'Clay Craft Ceramic Kulhad Set (Set of 4)',
                'slug': 'ceramic-coffee-mug-set',
                'category': 'home-living',
                'description': 'Handcrafted traditional kulhad cups — perfect for chai lovers. Microwave safe, eco-friendly, and adds authentic Indian charm to your kitchen.',
                'price': 599,
                'stock': 50,
                'image_url': 'https://images.unsplash.com/photo-1514228742587-6b1558fcca73?w=400',
            },
            {
                'name': 'Bella Vita Organic Scented Candle Set',
                'slug': 'scented-candle-collection',
                'category': 'home-living',
                'description': 'Set of 3 soy wax candles — Lavender, Sandalwood & Jasmine. Hand-poured in India, burns up to 40 hours each. Perfect for festivals and gifting.',
                'price': 749,
                'stock': 35,
                'image_url': 'https://images.unsplash.com/photo-1602607890114-2a0b4e5a5a5a?w=400',
            },
            {
                'name': 'Strauss Yoga Mat 6mm Anti-Slip',
                'slug': 'yoga-mat-premium',
                'category': 'sports',
                'description': 'Extra thick 6mm yoga mat with anti-slip texture and carry strap. TPE material, eco-friendly. Perfect for yoga, surya namaskar, and home workouts.',
                'price': 799,
                'stock': 45,
                'image_url': 'https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=400',
            },
            {
                'name': 'Boldfit Resistance Band Set (5 Bands)',
                'slug': 'resistance-band-set',
                'category': 'sports',
                'description': 'Complete home gym kit with 5 resistance bands, door anchor, handles & ankle straps. Great for strength training without expensive equipment.',
                'price': 499,
                'stock': 60,
                'image_url': 'https://images.unsplash.com/photo-1598289431512-b97b0917affc?w=400',
            },
            {
                'name': 'boAt Stone 350 Bluetooth Speaker',
                'slug': 'portable-bluetooth-speaker',
                'category': 'electronics',
                'description': 'IPX7 waterproof portable speaker with 360° sound, 12-hour playtime, and built-in mic. Perfect for house parties, picnics, and travel across India.',
                'price': 1999,
                'stock': 28,
                'image_url': 'https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=400',
            },
        ]

        updated_count = 0
        for prod_data in products_data:
            category = Category.objects.get(slug=prod_data.pop('category'))
            _, created = Product.objects.update_or_create(
                slug=prod_data['slug'],
                defaults={**prod_data, 'category': category},
            )
            updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(f'Updated {updated_count} products with INR pricing ({Product.objects.count()} total).')
        )
