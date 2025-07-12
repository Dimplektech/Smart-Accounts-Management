"""
Views for the scanner app - integrated with Smart Account Management
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from accounts.models import Transaction, Category
from .models import Receipt, ReceiptItem 
from accounts.models import Transaction, Category


@login_required
def scanner_home(request):
    """Scanner home page - shows recent receipts and quick actions"""
    recent_receipts = Receipt.objects.filter(user=request.user)[:5]
    context = {
        'recent_receipts': recent_receipts,
        'total_receipts': Receipt.objects.filter(user=request.user).count(),
        'completed_receipts': Receipt.objects.filter(user=request.user, status='completed').count(),
    }
    return render(request, 'scanner/scanner_home.html', context)

@login_required
def upload_receipt(request):
    """Upload and process receipt with OCR"""
    if request.method == 'POST':
        if 'receipt_image' in request.FILES:
            image_file = request.FILES['receipt_image']
            
            try:
                # Create receipt instance
                receipt = Receipt.objects.create(
                    user=request.user,
                    image=image_file,
                    original_filename=image_file.name,
                    status='processing'
                )
                
                try:
                    # Try OCR processing
                    from .ocr_service import ReceiptOCRService
                    ocr_service = ReceiptOCRService()
                    result = ocr_service.process_receipt(receipt.image.path)
                    
                    if result:
                        # Convert date object to string for JSON storage
                        if result.get('date') and hasattr(result['date'], 'strftime'):
                            result['date'] = result['date'].strftime('%Y-%m-%d')
                        
                        # Update receipt with OCR results
                        receipt.raw_text = result.get('raw_text', '')
                        receipt.parsed_data = result  # Now safe for JSON
                        receipt.merchant_name = result.get('merchant_name')
                        receipt.total_amount = result.get('total_amount')
                        
                        # Handle date field separately
                        if result.get('date'):
                            from datetime import datetime
                            try:
                                if isinstance(result['date'], str):
                                    receipt.date = datetime.strptime(result['date'], '%Y-%m-%d').date()
                                else:
                                    receipt.date = result['date']
                            except:
                                receipt.date = None
                        
                        receipt.tax_amount = result.get('tax_amount')
                        receipt.status = 'completed'
                        receipt.save()
                        
                        # Create receipt items
                        items = result.get('items', [])
                        for item_data in items:
                            ReceiptItem.objects.create(
                                receipt=receipt,
                                name=item_data.get('name', ''),
                                quantity=item_data.get('quantity', 1),
                                price=item_data.get('price', 0),
                                total=item_data.get('total', 0),
                            )
                        
                        messages.success(request, f'Receipt processed with OCR! Found: {receipt.merchant_name or "Unknown merchant"}')
                    else:
                        receipt.status = 'failed'
                        receipt.save()
                        messages.warning(request, 'OCR processing failed, but receipt saved.')
                        
                except Exception as ocr_error:
                    receipt.status = 'failed'
                    receipt.save()
                    messages.warning(request, f'OCR error: {str(ocr_error)}. Receipt saved without processing.')
                
                return redirect('scanner:receipt_detail', receipt_id=receipt.id)
                    
            except Exception as e:
                messages.error(request, f'Error uploading receipt: {str(e)}')
                return redirect('scanner:upload_receipt')
        else:
            messages.error(request, 'Please select a receipt image to upload.')
    
    return render(request, 'scanner/upload_receipt.html')


@login_required
def receipt_history(request):
    """Receipt history view - shows all user's receipts"""
    receipts = Receipt.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'receipts': receipts,
    }
    return render(request, 'scanner/receipt_history.html', context)


@login_required
def receipt_detail(request, receipt_id):
    """View individual receipt details"""
    receipt = get_object_or_404(Receipt, id=receipt_id, user=request.user)
    context = {
        'receipt': receipt,
        'items': receipt.items.all(),
    }
    return render(request, 'scanner/receipt_detail.html', context)


@login_required
def create_transaction_from_receipt(request, receipt_id):
    """Convert a receipt to a transaction (future functionality)"""
    receipt = get_object_or_404(Receipt, id=receipt_id, user=request.user)
    
    if receipt.status != 'completed' or not receipt.total_amount:
        messages.info(request, "OCR processing coming soon! For now, please add transactions manually.")
        return redirect('accounts:add_transaction')
    
    # Future OCR integration code will go here
    messages.info(request, "Transaction creation from receipts coming soon!")
    return redirect('scanner:receipt_detail', receipt_id=receipt_id)


@login_required
def scanner_status(request):
    """API endpoint to check scanner status"""
    return JsonResponse({
        'scanner_available': False,  # Set to False until OCR is working
        'message': 'Scanner functionality coming soon!'
    })