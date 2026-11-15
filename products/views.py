from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Product
import barcode as barcode_lib
from barcode.writer import ImageWriter
import qrcode
from pathlib import Path
from django.conf import settings

def product_list(request):
    return render(request, "products/list.html", {"products": Product.objects.all().order_by("-id")})

def product_add(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        sku = request.POST.get("sku", "").strip()
        code = request.POST.get("barcode", "").strip()
        price = request.POST.get("price") or "0"
        stock = request.POST.get("stock") or "0"
        kind = request.POST.get("barcode_type", "code128")
        if not name or not sku or not code:
            messages.error(request, "Name, SKU and barcode are required.")
        else:
            try:
                product = Product.objects.create(name=name, sku=sku, barcode=code,
                    price=price, stock=stock, barcode_type=kind)
                _make_labels(product)
                messages.success(request, "Product saved and labels generated.")
                return redirect("products:list")
            except Exception as exc:
                messages.error(request, f"Could not save product: {exc}")
    return render(request, "products/add.html")

def _make_labels(product):
    folder = Path(settings.MEDIA_ROOT) / "barcodes"
    folder.mkdir(parents=True, exist_ok=True)
    if product.barcode_type == "ean13" and len(product.barcode) == 13 and product.barcode.isdigit():
        cls = barcode_lib.get_barcode_class("ean13")
        image = cls(product.barcode, writer=ImageWriter()).render()
        image.save(str(folder / f"{product.pk}_barcode.png"), format="PNG")
    else:
        cls = barcode_lib.get_barcode_class("code128")
        image = cls(product.barcode, writer=ImageWriter()).render()
        image.save(str(folder / f"{product.pk}_barcode.png"), format="PNG")
    qr = qrcode.make(product.barcode)
    qr.save(folder / f"{product.pk}_qr.png")

def product_label(request, pk):
    product = get_object_or_404(Product, pk=pk)
    folder = Path(settings.MEDIA_ROOT) / "barcodes"
    return render(request, "products/label.html", {
        "product": product,
        "barcode_url": f"{settings.MEDIA_URL}barcodes/{pk}_barcode.png",
        "qr_url": f"{settings.MEDIA_URL}barcodes/{pk}_qr.png",
    })
