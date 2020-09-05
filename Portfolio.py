





class Portfolio(object):
    def __init__(self):

        self.positions = {}
        self.portfolio_value = 0

    def add_security(self, security_name, security, quantity, long):
        long_short = 1 if long is True else -1
        self.positions[security_name] = {"security":security, "quantity":quantity, "long": long_short}
        self.portfolio_value += security.present_value * quantity * long_short

        self.update_portfolio()

    def update_portfolio(self):

        self.portfolio_dollar_dur = 0
        self.portfolio_convexity = 0

        for key in self.positions.keys():

            q = self.positions[key]["quantity"]
            l = self.positions[key]["long"]
            pV = self.positions[key]["security"].present_value
            dD = self.positions[key]["security"].dollar_duration
            cV = self.positions[key]["security"].convexity_per_price

            self.portfolio_dollar_dur += dD * q * l
            self.portfolio_convexity += pV * cV * q * l

    def portfolio_details(self):
        portfolio      = '''
                Portfolio Value                 {}
                Portfolio Dollar Duration       {}
                Portfolio Convexity             {}

'''.format(round(self.portfolio_value,2), round(self.portfolio_dollar_dur,2), round(self.portfolio_convexity,2))

        for sec_name in self.positions.keys():
            sec = self.positions[sec_name]['security']
            q = self.positions[sec_name]['quantity']
            pos = 'long' if self.positions[sec_name]['long'] > 0 else 'short'
            p_details  = '''    {0} {1}'''.format(q, pos)+sec.bond_statistics()
            portfolio += p_details+'\n'

        return portfolio
