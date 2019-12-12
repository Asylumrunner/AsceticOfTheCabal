class Item:
    def __init__(self, use_function=None, uses=-99, **kwargs):
        self.use_function = use_function
        self.uses = uses
        self.function_kwargs = kwargs
    
    def use(self, *args):
        for function in self.use_function:
            function(*args, **self.function_kwargs)
        
        if self.uses != -99:
            self.uses -= 1
            if self.uses <= 0:
                return True
        
        return False

    