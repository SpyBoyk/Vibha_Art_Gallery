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
    help = "Loads Vibha Art Galleries master catalog 2026 data"

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
            User.objects.create_superuser("admin", "admin@vibha.com", "adminpass")
            self.stdout.write("Created superuser: admin / adminpass")

        # 2. Create Categories (Sections A to F) & copy images
        cats_mapping = [
            ("section-a-premium-metal-stand-busts", "Section A: Premium Metal Stand Busts", "Premium metal stand busts featuring adjustable heights and luxury suede finishes.", "images.jfif"),
            ("section-b-multi-size-bust-collection", "Section B: Multi-Size Bust Collection", "Red, blue, and white suede bust collections in small, medium, and big sizes.", "images (1).jfif"),
            ("section-c-metal-pu-display-stands", "Section C: Metal & PU Display Stands", "Metal & PU display stands for earrings, bangles, rings, and bracelets.", "images (2).jfif"),
            ("section-d-premium-suede-display-trays", "Section D: Premium Suede Display Trays", "Premium suede display trays for earrings, rings, chains, and necklaces.", "images (3).jfif"),
            ("section-e-premium-combo-sets", "Section E: Premium Combo Sets", "Ready-for-showroom display solutions, multi-ring props, and complete sets.", "images (4).jfif"),
            ("section-f-luxury-combo-collection", "Section F: Luxury Combo Collection", "Premium Turkish designs and full display combo sets on wooden bases.", "images.jfif"),
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
            title="Premium Jewellery Display Solutions",
            subtitle="Master Catalog 2026 - Bulk Orders & Custom Logo Available.",
            link="/products/shop/?category=section-a-premium-metal-stand-busts",
            order=1
        )
        Banner.objects.create(
            title="Luxury Suede Display Trays",
            subtitle="Anti-Tarnish, Anti-Scratch Premium Showroom Counter Accessories.",
            link="/products/shop/?category=section-d-premium-suede-display-trays",
            order=2
        )

        # 4. Create Products
        products_data = [
            # Section A: Premium Metal Stand Busts
            {
                "category": cats["section-a-premium-metal-stand-busts"],
                "name": "Adjustable Red Bust with Metal Stand - 15\"",
                "sku": "VAG-A-03",
                "description": "Premium red suede bust with gold metal base. Features: Height Adjustable | Gold Metal Stand | Flat Base. Color: Classic Red Suede. Best For: Shop Counter + Exhibition Stall. MOQ: 10 Pcs.",
                "price": 2200.00,
                "stock": 50,
                "is_featured": True,
                "is_trending": True,
                "images_list": [("images (5).jfif", "red-bust-1.jfif"), ("images (6).jfif", "red-bust-2.jfif")]
            },
            {
                "category": cats["section-a-premium-metal-stand-busts"],
                "name": "Luxury White Bust 20\" with Metal Stand",
                "sku": "VAG-A-04",
                "description": "Luxury white suede bust with heavy gold metal stand. Features: 20\" High Adjustable | Premium Finish | Stable Base. Color: Pure White Suede. Best For: High-End Showroom + Bridal Collection. MOQ: 10 Pcs.",
                "price": 2200.00,
                "stock": 35,
                "is_featured": True,
                "is_best_seller": True,
                "images_list": [("images (6).jfif", "white-bust-1.jfif"), ("images (5).jfif", "white-bust-2.jfif")]
            },
            {
                "category": cats["section-a-premium-metal-stand-busts"],
                "name": "Dual Tone Bust Set 20\" Adjustable",
                "sku": "VAG-A-05",
                "description": "Dual tone bust combo set of 3. Black & white suede with gold metal stands. Features: 2 Color Options | 20\" Adjustable | Heavy Base. Color: Black Suede, White Suede. Best For: Modern Designs + Instagram Photoshoot. MOQ: 10 Pcs/Set.",
                "price": 6500.00,
                "stock": 15,
                "is_featured": True,
                "images_list": [("images (5).jfif", "dualtone-bust-1.jfif")]
            },
            {
                "category": cats["section-a-premium-metal-stand-busts"],
                "name": "Mini Pink Bust with Stand 20\"",
                "sku": "VAG-A-07",
                "description": "Soft pink suede mini bust set of 4 with metal stands. Features: Compact Size | 20\" Height | Set of 4 Pcs. Color: Soft Pink Suede. Best For: Boutique + Trendy Collection. MOQ: 10 Sets.",
                "price": 1980.00,
                "stock": 20,
                "is_featured": False,
                "is_trending": True,
                "images_list": [("images (6).jfif", "pink-bust-1.jfif")]
            },

            # Section B: Multi-Size Bust Collection
            {
                "category": cats["section-b-multi-size-bust-collection"],
                "name": "Red Bust Set - Small, Medium, Big (Trio Set)",
                "sku": "VAG-B-06",
                "description": "Premium red suede bust trio set (10\" + 14\" + 17\"). Features: 3 Sizes in 1 Set | Same Color Match | Space Saving. Color: Rich Red Suede. Best For: Complete Display Solution. MOQ: 10 Sets.",
                "price": 1100.00,
                "stock": 40,
                "is_featured": True,
                "images_list": [("images (1).jfif", "red-trio-1.jfif")]
            },
            {
                "category": cats["section-b-multi-size-bust-collection"],
                "name": "Blue Round Bust 12\"",
                "sku": "VAG-B-32",
                "description": "Unique round base design blue suede bust. Features: Round Base Design | 12\" Height | Compact. Color: Royal Blue Suede. Best For: Unique Display | Gift Purpose. MOQ: 10 Pcs.",
                "price": 1320.00,
                "stock": 25,
                "is_featured": False,
                "is_best_seller": True,
                "images_list": [("images (1).jfif", "blue-round-1.jfif")]
            },
            {
                "category": cats["section-b-multi-size-bust-collection"],
                "name": "Big Bust - Royal Blue & White",
                "sku": "VAG-B-34",
                "description": "Big royal bust 18\"+ in blue & white suede. Features: Big Size | Full Neck Coverage | Premium Look. Color: Royal Blue, White. Best For: Bridal Shop + Wedding Exhibition. MOQ: 10 Pcs.",
                "price": 3800.00,
                "stock": 10,
                "is_featured": False,
                "images_list": [("images (1).jfif", "big-bust-1.jfif")]
            },
            {
                "category": cats["section-b-multi-size-bust-collection"],
                "name": "Medium Blue Bust Pair",
                "sku": "VAG-B-35",
                "description": "Medium blue suede bust pair. Features: 2 Pcs Set | Matching Color | Standard Size. Color: Royal Blue Suede. Best For: Retail Shop Counter. MOQ: 10 Pairs.",
                "price": 2200.00,
                "stock": 12,
                "is_featured": False,
                "images_list": [("images (1).jfif", "blue-pair-1.jfif")]
            },

            # Section C: Metal & PU Display Stands
            {
                "category": cats["section-c-metal-pu-display-stands"],
                "name": "Gold Metal Earring Stand Set of 3",
                "sku": "VAG-C-02",
                "description": "Premium gold metal earring stand set of 3. 100% metal with gold polish finish. Features: 3 Design | Anti-Tarnish | Heavy Base | No Wobble | Multi Height Design. Best For: Shop Counter | Photoshoot Prop. MOQ: 10 Sets.",
                "price": 1540.00,
                "stock": 30,
                "is_featured": True,
                "is_trending": True,
                "images_list": [("images (2).jfif", "earring-stand-1.jfif")]
            },
            {
                "category": cats["section-c-metal-pu-display-stands"],
                "name": "Prop Stand with Metal Rod",
                "sku": "VAG-C-10",
                "description": "Multi-prop display stand with metal rod. White Suede Top + Gold Metal Base & Rod. Features: 6+ Props | Top + Hanging Rod | Adjustable. Best For: Exhibition Stall | Complete Collection Display. MOQ: 5 Sets.",
                "price": 1800.00,
                "stock": 15,
                "is_featured": False,
                "images_list": [("images (2).jfif", "prop-stand-1.jfif")]
            },
            {
                "category": cats["section-c-metal-pu-display-stands"],
                "name": "PU Bracelet Stand",
                "sku": "VAG-C-11",
                "description": "Luxury grey PU leather bracelet stand with metal frame. Features: 8\" Length | 2\" Width | Velvet Soft Touch. Best For: Modern Jewellery | Minimalist Display. MOQ: 10 Pcs.",
                "price": 880.00,
                "stock": 50,
                "is_featured": False,
                "is_best_seller": True,
                "images_list": [("images (7).jfif", "pu-bracelet-1.jfif")]
            },
            {
                "category": cats["section-c-metal-pu-display-stands"],
                "name": "Gold T-Stand Earring Display",
                "sku": "VAG-C-12",
                "description": "Metal T-stand earring display with gold finish. Features: T-Shape | 4\" Height | Stable Square Base. Best For: Bulk Earring Display | Tray Setup. MOQ: 20 Pcs.",
                "price": 880.00,
                "stock": 60,
                "is_featured": False,
                "images_list": [("images (8).jfif", "tstand-earring-1.jfif")]
            },
            {
                "category": cats["section-c-metal-pu-display-stands"],
                "name": "Multi-Color PU Pillow Stand",
                "sku": "VAG-C-14",
                "description": "Premium PU pillow stand - multi color. PU Leather + Metal Base. Features: Soft Pillow Top | Metal Stand | 5 Color Options. Color: Grey, Peach, Orange, Brown, Black. Best For: Ring Counter | Mix & Match Display. MOQ: 10 Pcs/Set.",
                "price": 880.00,
                "stock": 40,
                "is_featured": False,
                "images_list": [("images (2).jfif", "pillow-stand-1.jfif")]
            },
            {
                "category": cats["section-c-metal-pu-display-stands"],
                "name": "Blue Suede Round Ring Stand",
                "sku": "VAG-C-18",
                "description": "Royal blue suede round ring stand. Blue Suede + Gold Metal Base. Features: Round Top | Velvet Finish | Compact Size. Best For: Bridal Jewellery | Color Contrast. MOQ: 10 Pcs.",
                "price": 1320.00,
                "stock": 35,
                "is_featured": False,
                "images_list": [("images (2).jfif", "blue-ring-1.jfif")]
            },
            {
                "category": cats["section-c-metal-pu-display-stands"],
                "name": "Blue Suede Pillow Stand with Metal Base",
                "sku": "VAG-C-19",
                "description": "Premium blue suede pillow stand. Blue Suede + Gold Metal Stand. Features: Pillow Shape | Metal Height | Premium Look. Best For: High-End Showroom Display. MOQ: 10 Pcs.",
                "price": 21320.00,
                "stock": 5,
                "is_featured": True,
                "images_list": [("images (2).jfif", "blue-pillow-1.jfif")]
            },
            {
                "category": cats["section-c-metal-pu-display-stands"],
                "name": "Orange Suede Round Ring Stand",
                "sku": "VAG-C-20",
                "description": "Trendy orange suede ring stand. Orange Suede + Gold Metal Base. Features: Round Top | Bright Color | Eye Catching. Best For: Young Customer | Trendy Collection. MOQ: 10 Pcs.",
                "price": 880.00,
                "stock": 30,
                "is_featured": False,
                "images_list": [("images (2).jfif", "orange-ring-1.jfif")]
            },
            {
                "category": cats["section-c-metal-pu-display-stands"],
                "name": "Navy Blue Bangle Stand with Metal",
                "sku": "VAG-C-30",
                "description": "Navy blue suede bangle stand with metal frame. Features: Roller Design | Metal Base | Smooth Surface. Best For: Bangle Shop | Bridal Kada Display. MOQ: 10 Pcs.",
                "price": 1100.00,
                "stock": 25,
                "is_featured": False,
                "images_list": [("images (2).jfif", "blue-bangle-1.jfif")]
            },
            {
                "category": cats["section-c-metal-pu-display-stands"],
                "name": "Orange Suede Pillow Stand",
                "sku": "VAG-C-33",
                "description": "Bright orange suede pillow stand with metal base. Features: Double Pillow | Metal Stand | Compact. Best For: Valentine Collection | Gift Display. MOQ: 10 Pairs.",
                "price": 1320.00,
                "stock": 20,
                "is_featured": False,
                "images_list": [("images (2).jfif", "orange-pillow-1.jfif")]
            },

            # Section D: Premium Suede Display Trays
            {
                "category": cats["section-d-premium-suede-display-trays"],
                "name": "Premium Earring Tray (10\"x15\")",
                "sku": "VAG-D-22",
                "description": "6-slot black suede earring tray. Premium Black Suede | High Density Foam Base. Features: 6 Separate Slots | Scratch Proof | Stackable Design. Best For: Counter Display | Storage Box Setup. MOQ: 10 Pcs.",
                "price": 880.00,
                "stock": 45,
                "is_featured": True,
                "images_list": [("images (3).jfif", "earring-tray-1.jfif")]
            },
            {
                "category": cats["section-d-premium-suede-display-trays"],
                "name": "Bracelet Tray (10\"x15\")",
                "sku": "VAG-D-23",
                "description": "6-pillow black suede bracelet tray. Black Suede + Soft Pillow Insert. Features: 6 Soft Pillows | Kada Secure Fit | Velvet Touch. Best For: Bridal Kada | Daily Wear Kada. MOQ: 10 Pcs.",
                "price": 1320.00,
                "stock": 30,
                "is_featured": True,
                "is_best_seller": True,
                "images_list": [("images (3).jfif", "bracelet-tray-1.jfif")]
            },
            {
                "category": cats["section-d-premium-suede-display-trays"],
                "name": "Small Chain Tray 3 Channel (9\"x10\")",
                "sku": "VAG-D-24",
                "description": "3-channel small chain tray in premium black suede. Features: 3 Deep Channels | Anti-Tangle | Compact Size. Best For: Small Chain Collection | Cash Counter. MOQ: 10 Pcs.",
                "price": 2750.00,
                "stock": 35,
                "is_featured": False,
                "images_list": [("images (4).jfif", "chain-tray-1.jfif")]
            },
            {
                "category": cats["section-d-premium-suede-display-trays"],
                "name": "Necklace Tray - Single Neck",
                "sku": "VAG-D-25",
                "description": "Single neck display tray 8\"x10\" in black suede. Features: Slanted Neck | Pendant Slot | Space Saving. Best For: Single Piece Display | Gift Purpose. MOQ: 10 Pcs.",
                "price": 2715.00,
                "stock": 30,
                "is_featured": False,
                "images_list": [("images (3).jfif", "single-neck-1.jfif")]
            },
            {
                "category": cats["section-d-premium-suede-display-trays"],
                "name": "Ring Tray - 5 Slot (10\"x15\")",
                "sku": "VAG-D-26",
                "description": "5-slot black suede ring tray. Premium Black Suede. Features: 5 Separate Ring Slots | Finger Fit Design. Best For: Ring Counter | Complete Set Display. MOQ: 10 Pcs.",
                "price": 960.00,
                "stock": 40,
                "is_featured": False,
                "images_list": [("images (3).jfif", "ring-tray-1.jfif")]
            },
            {
                "category": cats["section-d-premium-suede-display-trays"],
                "name": "Combo Ring Stand Tray",
                "sku": "VAG-D-28",
                "description": "Combo ring stand tray 6\"x9\" in black suede. Features: Ring Slots + Small Compartment | 2-in-1 Design. Best For: Small Counter | Mix Item Display. MOQ: 10 Pcs.",
                "price": 2660.00,
                "stock": 25,
                "is_featured": False,
                "images_list": [("images (3).jfif", "combo-ring-1.jfif")]
            },
            {
                "category": cats["section-d-premium-suede-display-trays"],
                "name": "Bracelet Stand Tray - 6 Pillow",
                "sku": "VAG-D-29",
                "description": "6-pillow bracelet stand tray 10\"x15\" in premium black suede. Features: 6 High Pillows | Extra Soft | Secure Grip. Best For: Heavy Kada | Rajwadi Bracelet. MOQ: 10 Pcs.",
                "price": 1200.00,
                "stock": 18,
                "is_featured": False,
                "images_list": [("images (3).jfif", "pillow-bracelet-1.jfif")]
            },

            # Section E: Premium Combo Sets
            {
                "category": cats["section-e-premium-combo-sets"],
                "name": "Bust + Earring Stand Combo Set",
                "sku": "VAG-E-01",
                "description": "Maroon bust + gold earring stand combo set. Maroon Suede/Microfiber Bust + Gold Metal Stand. Includes: 2 Bust 15\" High + 2 Gold Earring Stands. Features: Complete Neck + Earring Display | Color Match. MOQ: 5 Sets.",
                "price": 2500.00,
                "stock": 10,
                "is_featured": True,
                "is_trending": True,
                "images_list": [("images (4).jfif", "maroon-combo-1.jfif")]
            },
            {
                "category": cats["section-e-premium-combo-sets"],
                "name": "Grey Suede Earring Stand Set",
                "sku": "VAG-E-13",
                "description": "Premium grey suede earring stand set with T-stand. Includes: 5 Suede Trays + 1 Gold T-Stand. Features: Multi-Level Display | Modern Look | Space Saving. MOQ: 5 Sets.",
                "price": 2200.00,
                "stock": 12,
                "is_featured": False,
                "images_list": [("images (4).jfif", "grey-combo-1.jfif")]
            },
            {
                "category": cats["section-e-premium-combo-sets"],
                "name": "Bust with Props Combo - Metal Neck",
                "sku": "VAG-E-15",
                "description": "Metal neck bust combo set 10\" - 3 color. Suede Bust + Metal Neck + Metal Props. Includes: 3 Bust Peach/Grey + 1 Small Prop + 1 Pillow Prop. Features: Heavy Duty | 3 Color Options | Props Included. MOQ: 5 Sets.",
                "price": 3200.00,
                "stock": 14,
                "is_featured": False,
                "images_list": [("images (4).jfif", "peach-combo-1.jfif")]
            },
            {
                "category": cats["section-e-premium-combo-sets"],
                "name": "Blue Suede Pillow + Bangle Stand Set",
                "sku": "VAG-E-17",
                "description": "Royal blue complete display set. Blue Suede + Gold Metal Base. Includes: Multiple Pillow Stands + Bangle Stands + Props. Features: Complete Counter Setup | Matching Color. MOQ: 3 Sets.",
                "price": 3500.00,
                "stock": 8,
                "is_featured": False,
                "images_list": [("images (4).jfif", "blue-pillow-combo-1.jfif")]
            },
            {
                "category": cats["section-e-premium-combo-sets"],
                "name": "Combo Ring Props - Black Suede",
                "sku": "VAG-E-31",
                "description": "Combo ring props display set - black suede. Includes: Multi-Ring Props on Round Base. Features: Compact Round Design | Multi Slot | Velvet Finish. MOQ: 10 Sets.",
                "price": 1400.00,
                "stock": 15,
                "is_featured": False,
                "images_list": [("images (4).jfif", "ring-props-1.jfif")]
            },
            {
                "category": cats["section-e-premium-combo-sets"],
                "name": "Premium Bust Trio Combo",
                "sku": "VAG-E-36",
                "description": "Blue suede bust trio combo on single base. Includes: 3 Blue Busts on Matching Base | Height Variation. Features: 3 Sizes in 1 Base | Uniform Look | Space Saving. MOQ: 5 Sets.",
                "price": 3800.00,
                "stock": 7,
                "is_featured": False,
                "images_list": [("images (4).jfif", "bust-trio-1.jfif")]
            },
            {
                "category": cats["section-e-premium-combo-sets"],
                "name": "Blue Suede Complete Display Set",
                "sku": "VAG-E-37",
                "description": "Blue suede master display set 12\" - full combo. Includes: 2 NeckBust 12\" + Ring Props + Pillow Props + T-Earring Props. Features: 7+ Pieces in 1 Set | Complete Showroom Setup. MOQ: 3 Sets.",
                "price": 4500.00,
                "stock": 8,
                "is_featured": True,
                "images_list": [("IMG-20220806-WA0000.jpg", "bluesuede-set-1.jpg")]
            },
            {
                "category": cats["section-e-premium-combo-sets"],
                "name": "Blue Suede NeckBust Set Compact",
                "sku": "VAG-E-38",
                "description": "Blue suede neckbust compact set 12\". Includes: 1 NeckBust 12\" + Ring Props + Pillow Props + T-Earring Props. Features: 5 Pieces in 1 Set | Compact Size | Premium Look. MOQ: 5 Sets.",
                "price": 3200.00,
                "stock": 11,
                "is_featured": False,
                "images_list": [("IMG-20220806-WA0000.jpg", "bluesuede-compact-1.jpg")]
            },

            # Section F: Luxury Combo Collection
            {
                "category": cats["section-f-luxury-combo-collection"],
                "name": "Turkish Bust Luxury Combo with Props",
                "sku": "VAG-F-09",
                "description": "Turkish luxury bust combo - white suede + metal. White Suede Bust + Gold Metal Props + Metal Base. Includes: 1 Turkish Bust + Multiple Round Props + T-Stands. Features: Turkish Design | Heavy Metal Base | Premium White Finish. MOQ: 2 Sets.",
                "price": 4800.00,
                "stock": 6,
                "is_featured": True,
                "images_list": [("images.jfif", "turkish-combo-1.jfif")]
            },
            {
                "category": cats["section-f-luxury-combo-collection"],
                "name": "Bust with Props Combo",
                "sku": "VAG-F-16",
                "description": "Royal blue bust combo set with gold props. Blue Suede + Gold Metal Props. Includes: 1 Big Bust + T-Stand + Round Props + Pillow Props. Features: Color Match Props | Gold Base | Premium Finish. MOQ: 3 Sets.",
                "price": 3600.00,
                "stock": 5,
                "is_featured": False,
                "images_list": [("images.jfif", "blue-gold-combo-1.jfif")]
            },
            {
                "category": cats["section-f-luxury-combo-collection"],
                "name": "Complete Neck + Bracelet Combo Set",
                "sku": "VAG-F-39",
                "description": "Brown suede complete jewellery combo set. Brown Suede + Wooden Base. Includes: Small Neck Bust + Big Neck Bust + Chain Stand + Ring Props + Bracelet Props. Features: 6+ Items in 1 Set | Wood + Suede Combo | Premium Look. MOQ: 2 Sets.",
                "price": 2800.00,
                "stock": 8,
                "is_featured": False,
                "images_list": [("images.jfif", "brown-wood-combo-1.jfif")]
            },
            {
                "category": cats["section-f-luxury-combo-collection"],
                "name": "Full Display Combo Set - Wood Base",
                "sku": "VAG-F-40",
                "description": "Master display combo set - grey suede + wood. Grey Suede + Wooden Base + Metal Props. Includes: Earring Props + Bangle Props + Chain Stand + Earring Tray + Multiple Busts. Features: 15+ Items in 1 Set | Complete Counter Setup | Premium Wood Base. MOQ: 1 Set.",
                "price": 9500.00,
                "stock": 3,
                "is_featured": True,
                "images_list": [("images.jfif", "grey-wood-combo-1.jfif")]
            }
        ]

        for p_info in products_data:
            images_list = p_info.pop("images_list")
            product = Product.objects.create(**p_info)
            for src, dest in images_list:
                copied_path = copy_img(src, "products", dest)
                if copied_path:
                    ProductImage.objects.create(product=product, image=copied_path)
                
        self.stdout.write("Created catalog products with image galleries.")

        # 5. Create Coupons
        Coupon.objects.create(
            code="WELCOME10",
            discount=10,
            active=True,
            valid_from=timezone.now() - datetime.timedelta(days=1),
            valid_to=timezone.now() + timezone.timedelta(days=60),
        )

        # 6. Create Blogs
        BlogPost.objects.create(
            title="Choosing the Right Display Materials for Gold & Diamond Jewelry",
            content="A premium jewelry showroom requires display stands that highlight the brilliance of the ornaments. In this guide, we review how velvet, suede, and gold metal stand busts contrast with kundan, diamond, and temple jewelry to elevate customer presentation.",
        )

        self.stdout.write("Vibha Art Galleries Catalog successfully loaded!")
