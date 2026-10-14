from assistant.knowledge import KnowledgeService


knowledge = KnowledgeService()

questions = [
    "Python programming language",
    "Albert Einstein",
    "Solar System"
]

for question in questions:
    print(f"\nQuestion: {question}")

    answer = knowledge.ask(question)

    print(f"Answer: {answer}")