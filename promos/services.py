from .models import Promo

class DeductPromoAmount:
    def __init__(self, promo_obj, amt_to_deduct):
        self.promo_obj = promo_obj
        self.amt_to_deduct = amt_to_deduct

    def is_correct_input(self):
        """
        Prevent amount to be an empty value, a non-int value
        or a value that is less than or equal to zero.
        """
        return self.amt_to_deduct and type(self.amt_to_deduct) == int and self.amt_to_deduct > 0


    def is_deductable(self):
        """
        Prevent deducting if the amount sent is greater
        than the available amount.
        """
        return self.amt_to_deduct <= self.promo_obj.promo_amount


    def is_successful_deduction(self):
        """
        Return True in case of no problems with the amount sent in the request.
        """
        return self.is_correct_input() and self.is_deductable()


    def get_failure_message(self):
        """
        Gets called only if is_successful_deduction returns False.
        """
        if not self.is_correct_input():
            return 'Please enter a valid positive integer number to be deducted.'

        if not self.is_deductable():
            return 'The deducted amount cannot be greater than the available amount.'

        return None

    def deduct_promo_amt(self):
        """
        Deduct a specific amount from a specific promo.
        Return: The new amount after deduction.
        """
        self.promo_obj.promo_amount -= self.amt_to_deduct
        self.promo_obj.save()
        return self.promo_obj

