import datetime
import os
import shutil
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import get_user_model
from products.models import Category, Product, ProductImage, Banner
from core.models import BlogPost
from orders.models import Coupon

User = get_user_model()

class Command(BaseCommand):
    help = "Loads sample data and copies images into media directory"

    def handle(self, *args, **options):
        self.stdout.write("Clearing existing database records for clean load...")
        ProductImage.objects.all().delete()
        Product.objects.all().delete()
        Category.objects.all().delete()
        Banner.objects.all().delete()
        BlogPost.objects.all().delete()
        Coupon.objects.all().delete()

        # Define paths
        media_src = os.path.join(settings.MEDIA_ROOT, 'images')
        categories_dest = os.path.join(settings.MEDIA_ROOT, 'categories')
        products_dest = os.path.join(settings.MEDIA_ROOT, 'products')
        
        os.makedirs(categories_dest, exist_ok=True)
        os.makedirs(products_dest, exist_ok=True)

        def copy_img(src_filename, dest_subdir, new_name):
            src_path = os.path.join(media_src, src_filename)
            if os.path.exists(src_path):
                dest_path = os.path.join(settings.MEDIA_ROOT, dest_subdir, new_name)
                shutil.copy(src_path, dest_path)
                return f"{dest_subdir}/{new_name}"
            return None

        # 1. Create Superuser if not exists
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@kalamandir.com", "adminpass")
            self.stdout.write("Created superuser: admin / adminpass")

        # 2. Create Categories & copy images
        cats_mapping = [
            ("ganpati-idols", "Ganpati Idols", "Beautiful traditional Ganpati idols handcrafted by rural artisans.", "images.jfif"),
            ("eco-friendly-ganpati", "Eco-Friendly Ganpati", "Ganpati idols made from 100% biodegradable Shadu clay.", "images (1).jfif"),
            ("pooja-accessories", "Pooja Accessories", "Authentic pooja thalis, brass lamps, and traditional festival items.", "images (2).jfif"),
            ("handmade-jewellery", "Handmade Jewellery", "Ethnic necklaces, earrings, and bangles designed for festivals.", "images (3).jfif"),
            ("customized-gifts", "Customized Gifts", "Handcrafted customized gift baskets and luxury boxes.", "images (4).jfif"),
        ]

        cats = {}
        for slug, name, desc, img_file in cats_mapping:
            new_img_name = f"{slug}.jfif"
            copied_path = copy_img(img_file, "categories", new_img_name)
            cat = Category.objects.create(
                name=name,
                slug=slug,
                description=desc,
                image=copied_path
            )
            cats[slug] = cat
        self.stdout.write("Created categories with images.")

        # 3. Create Banners
        Banner.objects.create(
            title="Ganesh Festival Special",
            subtitle="Bring home the blessings of Eco-Friendly Clay Bappa.",
            link="/products/shop/?category=eco-friendly-ganpati",
            order=1
        )
        Banner.objects.create(
            title="Handcrafted Festive Jewellery",
            subtitle="Discover pure silver and semi-precious custom designs.",
            link="/products/shop/?category=handmade-jewellery",
            order=2
        )

        # 4. Create Products
        products_data = [
            {
                "category": cats["eco-friendly-ganpati"],
                "name": "Eco-Friendly Shadu Clay Ganpati Idol (12 Inches)",
                "sku": "GAN-SHADU-12",
                "description": "Handcrafted by award-winning artisans. Made of pure eco-friendly Shadu clay and painted with organic water-soluble colors.",
                "price": 1899.00,
                "discount_price": 1599.00,
                "stock": 25,
                "is_featured": True,
                "is_trending": True,
                "images_list": [("images (5).jfif", "gan-shadu-12-1.jfif"), ("images (6).jfif", "gan-shadu-12-2.jfif"), ("images.jfif", "gan-shadu-12-3.jfif")]
            },
            {
                "category": cats["ganpati-idols"],
                "name": "Ornate Dagadusheth Clay Ganpati Idol",
                "sku": "GAN-DAGADU-15",
                "description": "A magnificent clay replication of the historical Pune Dagadusheth Halwai Ganpati idol, adorned with golden clay ornaments.",
                "price": 2499.00,
                "stock": 10,
                "is_featured": True,
                "is_best_seller": True,
                "images_list": [("images (6).jfif", "gan-dagadu-15-1.jfif"), ("images (5).jfif", "gan-dagadu-15-2.jfif"), ("images (1).jfif", "gan-dagadu-15-3.jfif")]
            },
            {
                "category": cats["handmade-jewellery"],
                "name": "Guttapusalu Traditional Pearl Necklace",
                "sku": "JWE-GUTTA-01",
                "description": "Premium handcrafted ethnic Guttapusalu necklace with high-quality pearls, ruby stones, and gold plating.",
                "price": 3200.00,
                "discount_price": 2800.00,
                "stock": 15,
                "is_featured": True,
                "is_trending": True,
                "images_list": [("images (7).jfif", "jwe-gutta-01-1.jfif"), ("images (8).jfif", "jwe-gutta-01-2.jfif")]
            },
            {
                "category": cats["handmade-jewellery"],
                "name": "Temple Work Jhumka Earrings",
                "sku": "JWE-JHUM-05",
                "description": "Traditional gold-plated temple design jhumkas featuring delicate floral carvings and hanging seed pearls.",
                "price": 850.00,
                "stock": 30,
                "is_featured": False,
                "is_best_seller": True,
                "images_list": [("images (8).jfif", "jwe-jhum-05-1.jfif"), ("images (7).jfif", "jwe-jhum-05-2.jfif")]
            },
            {
                "category": cats["pooja-accessories"],
                "name": "Premium Brass Pooja Thali Set (8 Items)",
                "sku": "POO-THALI-08",
                "description": "An elegant pure brass thali set including diya, incense holder, roli-chawal containers, bell, and panchamrit spoon.",
                "price": 1250.00,
                "discount_price": 1099.00,
                "stock": 20,
                "is_featured": True,
                "is_best_seller": True,
                "images_list": [("IMG-20220806-WA0000.jpg", "poo-thali-08-1.jpg"), ("images (2).jfif", "poo-thali-08-2.jfif")]
            },
            {
                "category": cats["customized-gifts"],
                "name": "Luxury Deepavali Handcrafted Gift Hamper",
                "sku": "GIF-DEEPA-01",
                "description": "Customizable luxury wooden box containing handmade clay diyas, premium dry fruits, and an organic incense set.",
                "price": 1500.00,
                "stock": 8,
                "is_featured": False,
                "is_trending": True,
                "images_list": [("images.jfif", "gif-deepa-01-1.jfif"), ("images (4).jfif", "gif-deepa-01-2.jfif")]
            }
        ]

        for p_info in products_data:
            images_list = p_info.pop("images_list")
            product = Product.objects.create(**p_info)
            for src, dest in images_list:
                copied_path = copy_img(src, "products", dest)
                if copied_path:
                    ProductImage.objects.create(product=product, image=copied_path)
                
        self.stdout.write("Created products with associated image galleries.")

        # 5. Create Coupons
        Coupon.objects.create(
            code="WELCOME10",
            discount=10,
            active=True,
            valid_from=timezone.now() - datetime.timedelta(days=1),
            valid_to=timezone.now() + datetime.timedelta(days=60),
        )

        # 6. Create Blogs
        BlogPost.objects.create(
            title="The Sacred Significance of Shadu Clay Ganpati Idols",
            content="Celebrating Ganesh Chaturthi with Clay Idols (Shadu Mati) is a practice deeply rooted in tradition. Shadu clay is natural silt sourced from riverbanks, signifying returning to nature. This article details why you should celebrate with clay Bappa.",
        )

        self.stdout.write("Sample data and image galleries loaded successfully!")
