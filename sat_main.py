from sat_ollama import generate_response

print("Refrigerator Service Chatbot")

serial_number = input("Enter refrigerator serial number: ").strip()
issue = input(" Describe the issue: ").strip()

answer = generate_response(serial_number, issue)

print("\n Suggested Resolution:\n")
print(answer)
