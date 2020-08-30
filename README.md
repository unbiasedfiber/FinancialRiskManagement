# FinancialRiskManagement

Study material for the FRM exam
(So far I've included Bond.py, next I'll develop a portfolio class to organize securities.)


- create a coupon bond object. Face value of 100, yield rate 6%, coupon rate 6% (par bond)
- period is payments per year, so period = 2 is semiannual payments. Term is time to maturity
- in years.

from Bond import Bond

B = Bond(face_val=100, rate=.06, coupon_rate=.06, period=2, term=10)

B.bond_statistics()
