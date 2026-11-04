import sys
sys.path.insert(0, "src")

from contextual_os import ContextualOS

system = ContextualOS()

try:
    # Simulate current weather context
    system.set_context(
        city="Pune",
        temperature=39,
        humidity=65,
        prediction="HEAT ALERT",
        role="Farmer"
    )

    print("\n========== CONTEXTUAL OS ==========")

    print("\nSTORED CONTEXT:")
    print(system.context_manager.get_context())

    question = "What precautions should farmers take today?"

    print("\nUSER QUESTION:")
    print(question)

    result = system.ask(question)

    print("\nDETECTED INTENT:")
    print(result["intent"])

    print("\nCONTEXTUAL SLM RESPONSE:")
    print(result["answer"])

    print("\n===================================")

finally:
    system.close()
