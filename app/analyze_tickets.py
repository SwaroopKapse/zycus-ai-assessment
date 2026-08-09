from data_loader import load_tickets

tickets = load_tickets()

categories = set()
products = set()
urgencies = set()
product_areas = set()

for ticket in tickets:
    categories.add(ticket["category"])
    products.add(ticket["product"])
    urgencies.add(ticket["urgency"])
    product_areas.add(ticket["product_area"])

print("\nCATEGORIES")
for item in sorted(categories):
    print("-", item)

print("\nPRODUCTS")
for item in sorted(products):
    print("-", item)

print("\nURGENCY LEVELS")
for item in sorted(urgencies):
    print("-", item)

print("\nPRODUCT AREAS")
for item in sorted(product_areas):
    print("-", item)