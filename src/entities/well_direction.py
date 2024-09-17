class WellDirection:
    def __init__(self, incl, azm, measured_depth):
        self.incl = incl
        self.azm = azm
        self.measured_depth = measured_depth
        self.tvd = 0.0
        self.ns = 0.0
        self.ew = 0.0
        self.closure = 0.0
        self.closure_direction = 0.0
        self.vs = 0.0
        self.dls = 0.0
        self.bur_deg_100ft = 0.0

    def update_values(self, tvd, ns, ew, closure, closure_direction, vs, dls, bur_deg_100ft):
        self.tvd = tvd
        self.ns = ns
        self.ew = ew
        self.closure = closure
        self.closure_direction = closure_direction
        self.vs = vs
        self.dls = dls
        self.bur_deg_100ft = bur_deg_100ft
