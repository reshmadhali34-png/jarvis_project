from openai import OpenAI

print("Starting program...")

client = OpenAI(timeout=10)  # ⬅️ added timeout

try:
    print("Sending request to AI...")

    response = client.responses.create(
        model="gpt-4.1-mini",
        input="Hello"
    )

    print("Response received!")
    print(response.output[0].content[0].text)

except Exception as e:
    print("ERROR:", e)

print("Program ended")