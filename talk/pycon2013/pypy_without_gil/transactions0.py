import transaction



def compute():
    for k in range(10**7):
        pass


for i in range(10):
    transaction.add(compute)

transaction.run()
