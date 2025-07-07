# accounts/forms.py
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, HTML, Div, Field
from crispy_forms.bootstrap import FormActions
from .models import Account, Transaction, Category, Budget, AccountType, Category_type

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['transaction_type', 'account', 'category', 'amount', 'description', 'date', 'payment_method']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
    
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filter accounts and categories by user
        self.fields['account'].queryset = Account.objects.filter(user=user, is_active=True)
        self.fields['category'].queryset = Category.objects.filter(user=user)
        
        # Crispy Forms Helper
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        
        self.helper.layout = Layout(
            HTML('<div class="card">'),
            HTML('<div class="card-header bg-primary text-white">'),
            HTML('<h4 class="mb-0"><i class="fas fa-plus me-2"></i>Add New Transaction</h4>'),
            HTML('</div>'),
            HTML('<div class="card-body">'),
            
            Row(
                Column('transaction_type', css_class='form-group col-md-6'),
                Column('account', css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            
            Row(
                Column('category', css_class='form-group col-md-6'),
                Column(
                    Field('amount', template='crispy_forms/bootstrap5/field_with_prepend.html', prepend='$'),
                    css_class='form-group col-md-6'
                ),
                css_class='form-row'
            ),
            
            'description',
            
            Row(
                Column('date', css_class='form-group col-md-6'),
                Column('payment_method', css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            
            HTML('</div>'),
            HTML('<div class="card-footer">'),
            FormActions(
                HTML('<a href="{% url "accounts:dashboard" %}" class="btn btn-secondary me-2">'
                     '<i class="fas fa-arrow-left me-1"></i>Cancel</a>'),
                Submit('submit', 'Save Transaction', css_class='btn btn-primary',
                       css_id='submit-transaction'),
            ),
            HTML('</div>'),
            HTML('</div>'),
        )

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'account_type', 'account_number', 'initial_balance', 'description']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        
        self.helper.layout = Layout(
            HTML('<div class="card">'),
            HTML('<div class="card-header bg-success text-white">'),
            HTML('<h4 class="mb-0"><i class="fas fa-university me-2"></i>Account Information</h4>'),
            HTML('</div>'),
            HTML('<div class="card-body">'),
            
            Row(
                Column('name', css_class='form-group col-md-8'),
                Column('account_type', css_class='form-group col-md-4'),
                css_class='form-row'
            ),
            
            Row(
                Column('account_number', css_class='form-group col-md-6'),
                Column(
                    Field('initial_balance', template='crispy_forms/bootstrap5/field_with_prepend.html', prepend='$'),
                    css_class='form-group col-md-6'
                ),
                css_class='form-row'
            ),
            
            'description',
            
            HTML('</div>'),
            HTML('<div class="card-footer">'),
            FormActions(
                HTML('<a href="{% url "accounts:account_list" %}" class="btn btn-secondary me-2">'
                     '<i class="fas fa-arrow-left me-1"></i>Cancel</a>'),
                Submit('submit', 'Save Account', css_class='btn btn-success'),
            ),
            HTML('</div>'),
            HTML('</div>'),
        )

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'category_type', 'color', 'icon', 'description']
        widgets = {
            'color': forms.TextInput(attrs={'type': 'color'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        
        self.helper.layout = Layout(
            HTML('<div class="card">'),
            HTML('<div class="card-header bg-info text-white">'),
            HTML('<h4 class="mb-0"><i class="fas fa-tags me-2"></i>Category Information</h4>'),
            HTML('</div>'),
            HTML('<div class="card-body">'),
            
            Row(
                Column('name', css_class='form-group col-md-6'),
                Column('category_type', css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            
            Row(
                Column('color', css_class='form-group col-md-6'),
                Column('icon', css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            
            'description',
            
            HTML('</div>'),
            HTML('<div class="card-footer">'),
            FormActions(
                HTML('<a href="{% url "accounts:dashboard" %}" class="btn btn-secondary me-2">'
                     '<i class="fas fa-arrow-left me-1"></i>Cancel</a>'),
                Submit('submit', 'Save Category', css_class='btn btn-info'),
            ),
            HTML('</div>'),
            HTML('</div>'),
        )

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['name', 'category', 'amount', 'start_date', 'end_date', 'description']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filter categories by user
        self.fields['category'].queryset = Category.objects.filter(
            user=user, 
            category_type__name='expense'
        )
        
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        
        self.helper.layout = Layout(
            HTML('<div class="card">'),
            HTML('<div class="card-header bg-warning text-dark">'),
            HTML('<h4 class="mb-0"><i class="fas fa-target me-2"></i>Budget Information</h4>'),
            HTML('</div>'),
            HTML('<div class="card-body">'),
            
            Row(
                Column('name', css_class='form-group col-md-8'),
                Column(
                    Field('amount', template='crispy_forms/bootstrap5/field_with_prepend.html', prepend='$'),
                    css_class='form-group col-md-4'
                ),
                css_class='form-row'
            ),
            
            Row(
                Column('category', css_class='form-group col-md-4'),
                Column('start_date', css_class='form-group col-md-4'),
                Column('end_date', css_class='form-group col-md-4'),
                css_class='form-row'
            ),
            
            'description',
            
            HTML('</div>'),
            HTML('<div class="card-footer">'),
            FormActions(
                HTML('<a href="{% url "accounts:dashboard" %}" class="btn btn-secondary me-2">'
                     '<i class="fas fa-arrow-left me-1"></i>Cancel</a>'),
                Submit('submit', 'Save Budget', css_class='btn btn-warning'),
            ),
            HTML('</div>'),
            HTML('</div>'),
        )