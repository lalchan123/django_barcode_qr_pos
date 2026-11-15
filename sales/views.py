import json
from decimal import Decimal, InvalidOperation
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.db import transaction
from django.contrib import messages
from products.models import Product
from .models import Sale, SaleItem

def pos(request):
    return render(request, "sales/pos.html")

@require_POST
def scan_product(request):
    try:
        data = json.loads(request.body or "{}")
        code = str(data.get("barcode", "")).strip()
        product = Product.objects.get(barcode=code)
        return JsonResponse({
            "ok": True, "id": product.id, "name": product.name, "barcode": product.barcode,
            "price": str(product.price), "stock": product.stock
        })
    except Product.DoesNotExist:
        return JsonResponse({"ok": False, "message": "Product not found. Add it first."}, status=404)
    except Exception:
        return JsonResponse({"ok": False, "message": "Invalid scan request."}, status=400)

@require_POST
@transaction.atomic
def checkout(request):
    try:
        payload = json.loads(request.POST.get("cart", "[]"))
        discount = Decimal(request.POST.get("discount", "0"))
        if not payload:
            raise ValueError("Cart is empty.")
        invoice = "INV" + __import__("datetime").datetime.now().strftime("%Y%m%d%H%M%S%f")
        sale = Sale.objects.create(invoice_no=invoice, customer_name=request.POST.get("customer", ""),
                                   discount=discount)
        subtotal = Decimal("0.00")
        for row in payload:
            product = Product.objects.select_for_update().get(pk=int(row["id"]))
            qty = int(row["qty"])
            if qty < 1 or product.stock < qty:
                raise ValueError(f"Insufficient stock for {product.name}. Available: {product.stock}")
            line = product.price * qty
            SaleItem.objects.create(sale=sale, product=product, quantity=qty,
                                    unit_price=product.price, line_total=line)
            product.stock -= qty
            product.save(update_fields=["stock"])
            subtotal += line
        if discount < 0 or discount > subtotal:
            raise ValueError("Invalid discount amount.")
        sale.subtotal = subtotal
        sale.total = subtotal - discount
        sale.save(update_fields=["subtotal", "total"])
        return redirect("sales:receipt", pk=sale.pk)
    except Exception as exc:
        messages.error(request, str(exc))
        return redirect("sales:pos")

def receipt(request, pk):
    sale = get_object_or_404(Sale.objects.prefetch_related("items__product"), pk=pk)
    return render(request, "sales/receipt.html", {"sale": sale})
