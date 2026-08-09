from task2.account_health import generate_account_brief


account_id = "ACC-3336"

result = generate_account_brief(account_id)

print("\n" + "=" * 70)
print("ACCOUNT HEALTH BRIEF")
print("=" * 70)

print(result)

print("\n" + "=" * 70)
print("END OF BRIEF")
print("=" * 70)