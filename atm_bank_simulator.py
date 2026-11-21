def calc_compound_interest(principal, rate, years):
    """
    Recursive function to calculate compound interest.
    """
    if years <= 0:
        return principal
    else:
        new_principal = principal + (principal * (rate / 100))
        return calc_compound_interest(new_principal, rate, years - 1)