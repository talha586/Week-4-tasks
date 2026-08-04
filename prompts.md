# Prompt Log — AI Agent Architecture Learning Session

This log documents the sequence of prompts used to learn AI agent architecture concepts, from foundational theory through to implementation details. Organized by topic to show the learning progression.

---

## 1. Agent Architecture Fundamentals

1. "What is an agent architecture. Explain me completely each and every thing regarding this."
2. "Make a graph/workflow of it which helps me in understanding much better."
3. "Is this called agent loop?"

## 2. Planner–Executor–Memory Pattern

4. "planner → executor → memory loop — explain this topic."
5. "In this case we have three LLMs? One plans, second executes, and the third holds memory?"
6. "Explain me it using the workflow/graph."
7. "So the above architecture and the recent one are different?"

## 3. Agent Architecture Taxonomy

8. "So planner→executor→memory loop is one type of AI architecture — are there any others, and where is this one used?"
9. "Give me the diagram/workflow of the last three architectures too." *(Supervisor-worker, graph-based, event-driven)*

## 4. Tools / Function Calling — Concept

10. "Explain me tools/function calling in the same way. It should cover each and everything."

## 5. Skills

11. "How to make a skill — its syntax and how to write it."

## 6. Function Calling — From Scratch (Implementation)

12. "How to make function calling."
13. "I want to learn from the scratch how to make function calling, their syntax and how to use them, what does each line refer to. I want to know from the scratch so help me in guiding this topic in that way."
14. "How to do the setup of it — also explain the steps."
15. "Give me the syntax of how to write the tools, as I have understood its purpose. Explain me its syntax by showing me multiple examples."

## 7. Function Calling — Cross-Provider Comparison

16. "Function calling with Claude API and OpenAI-compatible APIs — explain me this topic completely, just like the way you did above."
17. "Now give me an example."
18. *(Pasted own code snippet)* "What is happening here — explain me and why are we doing each step here and what it does."
19. "What does response.content contain, and what does `block` refer to?"

## 8. Hooks

20. "Hooks: pre/post-action interceptors in agent pipelines — give me complete understanding and each and every detail related to this topic, and also share some articles so I can learn this topic much better."

## 9. Agent Memory Systems

21. "Memory types: in-context, vector (ChromaDB), key-value stores — give me complete understanding and each and every detail, share articles, give an example, and draw a workflow/graph if required."

## 10. Extending Agents — Search, Code Execution, File I/O

22. "Extending agents with search, code execution, file I/O — explain these topics and suggest some articles and videos for complete understanding."

## 11. Plugins

23. "What are Plugin[s]?"

## 12. Multi-Step Reasoning

24. "What is Multi-step reasoning?"

---

### Topics covered, end to end
Agent loops (ReAct) → Planner-executor-memory → Architecture taxonomy (supervisor-worker, graph-based, event-driven) → Tool/function calling (concept, syntax, setup, Claude API + OpenAI-compatible APIs) → Skills → Hooks (pre/post-action interceptors) → Memory systems (in-context, vector/ChromaDB, key-value) → Extending agents (search, code execution, file I/O) → Plugins → Multi-step reasoning.
