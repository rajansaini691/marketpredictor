"""
Calculate the customer survey score
"""
"""
Notes: 
 - age and mtbf scores stay the same throughout the simulation.
   price is predictable long-term, and ideal_position is from
   perceptual map
 - do importances change?
"""

# Importances
age_importance = 
price = 
ideal_position = 
mtbf = 

# Scores
age_mean = 
age_stdev = 
ideal_price =       # If reported as a range [low,high], this should be the average
ideal_position_range = []
mtbf_range = []

# Product params
product_age = 

# Calculate Age:
# Age is a gaussian
# TODO Convert to function and implement
age_score = gaussian(age_mean, age_stdev, product_age) * age_importance

# Price goes down 50 cents every year (we can do long-term predictions here)
def price_score(product_price, price_range):
    """
    Returns a value in [0,1]. The closer the product_price
    and ideal_price are, the higher the returned value.
    """
    low, high = price_range

    # Rough cut
    if product_price < low - 5 or high > ideal_price + 5:
        return 0

    # Normal demand curve
    if low < product_price < high:

    # Fine cut. Derivation done on paper.
    return (80/100)**abs(product_price - ideal_price)

def mtbf_score(product_mtbf, desired_mtbf):
    """
    Returns a value in [0,1]. Towards top of range implies
    higher score.

    desired_mtbf is the uppermost mtbf desired by customers.
    Going higher has no effect; going >5000 below fails this task.
    """
    # Rough cut
    if product_mtbf - 5000 < desired_mtbf:
        return 0
    
    return (80/100)**(abs(product_mtbf - desired_mtbf)/1000)

def positioning_score(centroid, offset_vector, product_position):
    """
    Calculates the positioning score under section 3.1.1.
    Returns a value in [0,1]. Closer to ideal implies higher score.

    Parameters:
        centroid            Center coord (x_c, y_c) of the market segment circle
        offset_vector       Ideal spot offset (dx, dy)
        product_position    Current placement of the product, (x, y)
    """
    assert(centroid[0] > 0 and centroid[1] > 0 and product_position[0] > 0 and product_position[1] > 0)

    x_c, y_c = centroid
    dx, dy = offset_vector
    x, y = product_position

    dist_from_centroid = (x - x_c)**2 + (y - y_c)**2
    # Outside of rough cut circle
    if dist_from_centroid > 4**2:
        return 0

    # Positioning Rough Cut (Between 2.5 and 4 units from center)
    if dist_from_centroid > 2.5**2:

    
    


