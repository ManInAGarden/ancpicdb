import sqlitepersist as sqp

class FilterData:

    """base class for filterting data"""
    def __init__(self, fact : sqp.SQFactory):
        self._fact = fact

    def is_defined(self, arg):
        return arg is not None and len(arg) > 0
    
    def is_strict(self, arg):
        return arg is not None and len(arg) > 0 and not '*' in arg
    
    def add2exp(self, exp, exppart):
        if exp is None: 
            return exppart
        else:
            return (exp) & (exppart)

    def add2exps(self, exps : str, adds : str) -> str:
        if exps is None:
            return adds
        else:
            return exps + " und " + adds
        
    def _get_monthcode(self, ms : int) -> str:
        if ms is None:
            return "NOMONTH"
        
        if ms > 0 and ms < 12:
            return "MONTH{:02d}".format(ms)
        
    def get_info(self) -> str:
        raise Exception("override me!")
        
    def get_query(self) -> sqp.SQQuery:
        """create and return the query for the current filter"""
        raise Exception("Override me!")    
    
    def get_query_info(self) -> str:
        raise Exception("Override me!")