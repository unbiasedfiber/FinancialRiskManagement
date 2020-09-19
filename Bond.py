
'''
Bond.py

The bond object class models a fixed income security

'''
class Bond(object):
    def __init__(self, face_val, rate, coupon_rate, period, term):

        self.fv = face_val;
        self.y = rate;
        self.cp = coupon_rate;
        self.p = period;
        self.t = term;

        self.payments = [0];
        self.durations = [0];
        self.convexities = [0];

        self.type = "Coupon" if self.cp == 0 else "Zero_Coupon"

        self.calculate_bond()

    # for a change in bond yield, taylor series (first and second derivatives of
    # present value formula) approximates the new present value.
    def price_change_linear(self, y_delta):
        return -self.modified_duration * self.present_value * y_delta

    def price_change_quadratic(self, y_delta):
        return .5 * self.convexity * self.present_value * y_delta**2

    def price_change_calculation(self, y_delta):
        exact_price     = self.fv / ( 1 + ((self.y+y_delta)/self.p) )**(self.t*self.p)
        duration_est    = self.present_value + self.price_change_linear(y_delta)
        dur_convex_est  = duration_est + self.price_change_quadratic(y_delta)
        return '''
        Bond present value {0} with yield {1}
        Bond yield change of {2} to {3}
        ------------------------------------------------------------------------
        Exact Price                     : {4}
        Duration Estimate               : {5}
        Duration and convexity Estimate : {6}
        '''.format(round(self.present_value,4), self.y, y_delta,
                   round(self.y+y_delta,2), exact_price,
                   duration_est, dur_convex_est)

    def calculate_bond(self):
        #cF is coupon payment, fraction of the face value.
        cF = self.cp * self.fv;

        if cF != 0:
        # sum of discounted coupon payments.
            for t in range(1, self.p*self.t+1):
                pV = (cF/self.p) / ( 1 + (self.y/self.p) )**t
                cV = t * pV
                cX = ((t+1)/(1+self.y/self.p)**2)*cV

                self.payments.append( pV )
                self.durations.append( cV )
                self.convexities.append( cX )

            # add face value payment at end of term.
            pV = (self.fv / ( 1 + (self.y/self.p) )**(self.t*self.p))
            cV = self.p * self.t * pV
            cX = ((self.p*self.t + 1) / (1+self.y/self.p)**2)*cV

        else:
            pV = (self.fv / ( 1 + (self.y/self.p) )**(self.t*self.p))
            cV = self.t
            cX =  self.fv * ((self.p*self.t + 1) * self.p*self.t ) / (1+self.y/self.p)**2

        self.payments[-1] += pV
        self.durations[-1] += cV
        self.convexities[-1] += cX

        self.present_value          = sum(self.payments)
        self.convexity              = (sum(self.convexities)**1/2)/self.p;
        self.convexity_per_price    = self.convexity/self.fv
        self.macaulay_duration      = (sum(self.durations)/self.fv)/self.p if cF > 0 else self.t;
        self.modified_duration      = self.macaulay_duration/(1+self.y/self.p)
        self.dollar_duration        = self.modified_duration * self.present_value
        self.dollar_bp              = self.dollar_duration * .0001

    def bond_statistics(self):
        return '''
        [{0}] Bond

        ------------------------------------------------------------------------
        Face Value......................: {1}
        Yield...........................: {2}
        Coupon..........................: {3}
        Period..........................: {4}
        Term............................: {5}

        ------------------------------------------------------------------------
        Present Value...................: {6}
        Macualay Duration...............: {7}
        Modified Duration...............: {8}
        Dollar Duration.................: {9}
        Dollar Duration (DV01)..........: {10}
        Convexity.......................: {11}
        Convesity per Price.............: {12}

        '''.format(self.type, self.fv, self.y, self.cp, self.p, self.t,
                    self.present_value, self.macaulay_duration, self.modified_duration,
                    self.dollar_duration, self.dollar_bp, self.convexity, self.convexity_per_price)
