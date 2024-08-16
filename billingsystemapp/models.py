from django.db import models,IntegrityError
import uuid
from datetime import date,timedelta
from decimal import Decimal


class Category(models.Model):
    name = models.CharField(max_length=100)
    starting_discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)  # Add this line

    def __str__(self):
        return self.name


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=200)
    brand = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount=models.DecimalField(max_digits=10, decimal_places=2,default=0.00)
    quantity = models.IntegerField()
    manufacturingdate = models.DateField(null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    def __str__(self):
        return self.product_name
    from datetime import date

    def update_discount(self):
        if self.manufacturingdate:
            months_old = (date.today().year - self.manufacturingdate.year) * 12 + date.today().month - self.manufacturingdate.month

            if months_old < 6:
                self.discount = Decimal('0.00')
            else:
                six_month_periods = (months_old - 6) // 6

                # Get the starting discount from the category
                starting_discount = Decimal(self.category.starting_discount)  # Ensure it's a Decimal

                # Define the increment per six-month period
                increment = Decimal('5.00')

                # Calculate the total discount
                total_discount = starting_discount + (six_month_periods * increment)
            
                # Ensure the total discount does not exceed 90%
                if total_discount > Decimal('90.00'):
                    total_discount = Decimal('90.00')

                self.discount = total_discount
        
            self.save()


class Sales(models.Model):
    sales_id = models.AutoField(primary_key=True)
    product_name = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()

    def __str__(self):
        return str(self.sales_id)
    
class Billing(models.Model):
    id = models.AutoField(primary_key=True)
    sale_number = models.UUIDField(default=uuid.uuid4, editable=False)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    purchasetime = models.DateTimeField(null=True)
    customer_name = models.CharField(max_length=200,null=True)
    customer_address = models.CharField(max_length=200,null=True)
    customer_phone = models.PositiveIntegerField(null=True)
    payment_method =models.CharField(max_length=200,null=True)

    class Meta:
        unique_together = ('sale_number', 'product_id')
    def __str__(self):
        return str(self.sale_number)

class stock(models.Model): 
    stock_id = models.AutoField(primary_key=True)
    product_name = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    stock =models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10,decimal_places=2)
    
    def __str__(self):
        return str(self.stock_id)

