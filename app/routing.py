def recommend_team(issue_category, product_area):
    """
    Decide which team should receive the ticket.
    """

    if issue_category == "Billing":
        return "Billing Support"

    if issue_category == "Onboarding":
        return "Onboarding Support"

    if issue_category == "Integration":
        return "Integration Support"

    if issue_category == "Data Loss":
        return "Data Recovery Support"

    if issue_category == "Performance":
        return "Technical Support"

    if issue_category == "Bug":
        return "Technical Support"

    if issue_category == "How-To":
        return "Technical Support"

    if issue_category == "Feature Request":
        return "Product Development"

    return "Technical Support"