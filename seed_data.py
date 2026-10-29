"""
Seed script for AlphaShop E-Commerce Store.
Populates realistic sample products and creates a default superuser if none exists.

Usage:
    python seed_data.py
"""

import os
import django

# Configure Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_site.settings')
django.setup()

from django.contrib.auth.models import User
from store.models import Product

SAMPLE_PRODUCTS = [
    {
        "name": "Apex Pro ANC Wireless Headphones",
        "category": "Audio",
        "price": 199.99,
        "stock": 25,
        "rating": 4.9,
        "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&auto=format&fit=crop&q=80",
        "description": "High-fidelity studio audio with hybrid active noise cancellation, 40-hour battery life, plush memory foam ear cushions, and transparency mode."
    },
    {
        "name": "PulseFit Ultra Smartwatch 2",
        "category": "Wearables",
        "price": 149.50,
        "stock": 18,
        "rating": 4.7,
        "image_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800&auto=format&fit=crop&q=80",
        "description": "Advanced health tracking with AMOLED always-on display, heart rate monitor, SpO2 sensor, sleep staging, GPS navigation, and 7-day battery life."
    },
    {
        "name": "Vortex RGB Mechanical Keyboard",
        "category": "Electronics",
        "price": 129.00,
        "stock": 30,
        "rating": 4.8,
        "image_url": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=800&auto=format&fit=crop&q=80",
        "description": "Hot-swappable linear switches, per-key RGB backlighting, aircraft-grade aluminum top plate, and sound-dampening acoustic silicone padding."
    },
    {
        "name": "ErgoGlide Precision Wireless Mouse",
        "category": "Accessories",
        "price": 59.99,
        "stock": 42,
        "rating": 4.6,
        "image_url": "https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?w=800&auto=format&fit=crop&q=80",
        "description": "Ergonomic 57-degree vertical grip designed to eliminate wrist strain, 4000 DPI sensor, silent click switches, and dual Bluetooth/2.4GHz connectivity."
    },
    {
        "name": "ViewMaster 27-inch 4K UHD Monitor",
        "category": "Electronics",
        "price": 349.99,
        "stock": 12,
        "rating": 4.9,
        "image_url": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=800&auto=format&fit=crop&q=80",
        "description": "Frameless IPS display with 99% sRGB color gamut, HDR400 certification, USB-C 65W power delivery, and an ergonomic height-adjustable pivot stand."
    },
    {
        "name": "Luxe Leather 15\" Laptop Sleeve",
        "category": "Accessories",
        "price": 45.00,
        "stock": 35,
        "rating": 4.7,
        "image_url": "https://images.unsplash.com/photo-1607604276583-eef5d076aa5f?w=800&auto=format&fit=crop&q=80",
        "description": "Handcrafted water-resistant vegan leather sleeve with magnetic clasp, scratch-proof microfiber interior lining, and rear accessory stash pocket."
    },
    {
        "name": "AuraDesk Smart Lamp with Qi Charger",
        "category": "Home & Office",
        "price": 69.95,
        "stock": 20,
        "rating": 4.8,
        "image_url": "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=800&auto=format&fit=crop&q=80",
        "description": "Minimalist architectural LED desk lamp with 5 color temperatures, touch slider dimmer, and 15W Qi fast wireless phone charging integrated base."
    },
    {
        "name": "EchoBeat Hi-Fi Bluetooth Speaker",
        "category": "Audio",
        "price": 89.00,
        "stock": 22,
        "rating": 4.7,
        "image_url": "https://images.unsplash.com/photo-1545454675-3531b543be5d?w=800&auto=format&fit=crop&q=80",
        "description": "360-degree immersive acoustic sound, dual passive bass radiators, IPX7 waterproof rating, and up to 24 hours of continuous playtime."
    },
    {
        "name": "NovaPods Pro True Wireless Earbuds",
        "category": "Audio",
        "price": 79.99,
        "stock": 28,
        "rating": 4.5,
        "image_url": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=800&auto=format&fit=crop&q=80",
        "description": "Compact featherweight wireless earbuds with dynamic graphene drivers, environmental noise cancellation for calls, and quick wireless charging case."
    },
    {
        "name": "FlexiStand Aluminum Monitor Riser",
        "category": "Home & Office",
        "price": 54.50,
        "stock": 15,
        "rating": 4.6,
        "image_url": "https://images.unsplash.com/photo-1586717791821-3f44a563fa4c?w=800&auto=format&fit=crop&q=80",
        "description": "Solid unibody aluminum desk riser supporting up to 50 lbs, keyboard stowage clearance underneath, and integrated cable routing channel."
    },
    {
        "name": "MagLock Fast Magnetic Power Bank",
        "category": "Accessories",
        "price": 39.99,
        "stock": 40,
        "rating": 4.8,
        "image_url": "https://images.unsplash.com/photo-1609592426868-b80c39fba667?w=800&auto=format&fit=crop&q=80",
        "description": "10,000mAh magnetic portable power bank with strong snap-on alignment, 20W PD USB-C bidirectional fast charging, and LED battery percentage readout."
    },
    {
        "name": "ZenDesk Dual-Sided Eco Desk Mat",
        "category": "Home & Office",
        "price": 28.00,
        "stock": 50,
        "rating": 4.9,
        "image_url": "https://images.unsplash.com/photo-1593642632823-8f785ba67e45?w=800&auto=format&fit=crop&q=80",
        "description": "Extra large 36\" x 17\" reversible desk pad made of organic cork and premium PU leather. Waterproof, oil-proof, and easy to clean with a damp cloth."
    }
]


def seed_database():
    print("-> Starting database seeding for AlphaShop E-Commerce Store...")

    # Create Superuser if needed
    if not User.objects.filter(username='admin').exists():
        admin_user = User.objects.create_superuser('admin', 'admin@alphashop.com', 'admin123')
        admin_user.first_name = "AlphaShop"
        admin_user.last_name = "Admin"
        admin_user.save()
        print("  [+] Superuser created: username='admin' | password='admin123'")
    else:
        print("  [i] Superuser 'admin' already exists.")

    # Create Sample Customer
    if not User.objects.filter(username='demo_user').exists():
        customer = User.objects.create_user('demo_user', 'demo@alphashop.com', 'password123')
        customer.first_name = "Alex"
        customer.last_name = "Morgan"
        customer.save()
        print("  [+] Demo Customer created: username='demo_user' | password='password123'")

    # Seed Products
    created_count = 0
    updated_count = 0
    for prod_data in SAMPLE_PRODUCTS:
        product, created = Product.objects.update_or_create(
            name=prod_data["name"],
            defaults={
                "category": prod_data["category"],
                "price": prod_data["price"],
                "stock": prod_data["stock"],
                "rating": prod_data["rating"],
                "image_url": prod_data["image_url"],
                "description": prod_data["description"],
            }
        )
        if created:
            created_count += 1
        else:
            updated_count += 1

    print(f"  [+] Seeding complete! {created_count} products created, {updated_count} updated.")
    print("\n✓ Your Django database is now loaded with realistic products!")
    print("Run `python manage.py runserver` to launch the store at http://127.0.0.1:8000/\n")


if __name__ == '__main__':
    seed_database()
