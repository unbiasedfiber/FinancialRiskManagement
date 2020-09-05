from Bond import Bond
from Portfolio import Portfolio


b1 = Bond(face_val=100, rate=.06, coupon_rate=.06, period=2, term=10)
b2 = Bond(face_val=100, rate=.06, coupon_rate=0, period=2, term=1)
b3 = Bond(face_val=100, rate=.06, coupon_rate=0, period=2, term=30)

p = Portfolio()
p.add_security(security_name='Bond 1', security=b1, quantity=10000, long=True)
p.add_security(security_name='Bond 2', security=b2, quantity=5000, long=True)
p.add_security(security_name='Bond 3', security=b3, quantity=10000, long=False)

print(p.portfolio_details())
