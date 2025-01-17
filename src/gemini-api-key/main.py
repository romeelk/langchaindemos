import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-2.0-flash-exp",
  generation_config=generation_config,
  system_instruction="You are an expert AI assistant for Python programming",
)

chat_session = model.start_chat(
  history=[
    {
      "role": "user",
      "parts": [
        "What is an efficient lookup in Python?",
      ],
    },
    {
      "role": "model",
      "parts": [
        "Okay, let's talk about efficient lookups in Python. The best data structure for a lookup depends heavily on what kind of data you have and what you need to do with it. Here's a breakdown of the common options and when to use them, focusing on efficiency (time complexity):\n\n**1. Dictionaries (`dict`)**\n\n*   **How it works:** Dictionaries use hash tables behind the scenes. They map keys to values.\n*   **Efficiency:**\n    *   **Average Case Lookup, Insertion, Deletion:** O(1) - Constant time! This is incredibly fast and what you want for the vast majority of lookup scenarios.\n    *   **Worst Case Lookup, Insertion, Deletion:** O(n) - Occurs rarely when hash collisions are frequent, but this is uncommon in practice.\n*   **When to use:** This is your **go-to** choice for most lookup needs. Use it whenever you have unique keys you want to associate with values. This is especially useful when you need quick access by a non-sequential key (like a string, a tuple, or an integer).\n*   **Example:**\n    ```python\n    student_grades = {\n        \"Alice\": 95,\n        \"Bob\": 88,\n        \"Charlie\": 92,\n    }\n    print(student_grades[\"Bob\"])  # Very fast lookup by name\n    ```\n*   **Key Requirements:** Keys must be hashable (immutable types like integers, strings, tuples)\n\n**2. Sets (`set`)**\n\n*   **How it works:** Sets also use hash tables, but they only store unique keys (no associated values).\n*   **Efficiency:**\n    *   **Average Case Membership Check, Insertion, Deletion:** O(1) - Constant time.\n    *   **Worst Case Membership Check, Insertion, Deletion:** O(n) -  Similar to dictionaries, this is uncommon.\n*   **When to use:** Use sets when you need to check if an item exists quickly and/or ensure that you only store unique values. They're perfect for avoiding duplicates.\n*   **Example:**\n    ```python\n    valid_users = {\"alice\", \"bob\", \"charlie\"}\n    if \"bob\" in valid_users: # Very fast membership check\n        print(\"User is valid\")\n    ```\n*   **Key Requirements:** Elements must be hashable.\n\n**3. Lists (`list`)**\n\n*   **How it works:** Lists store elements in a sequential order.\n*   **Efficiency:**\n    *   **Lookup by Index (e.g., `my_list[0]`)**: O(1) - Constant time. This is good for retrieving an item when you already know the position.\n    *   **Lookup by Value (e.g., `if item in my_list`):** O(n) - Linear time. Python will have to potentially check *every* element. This is very inefficient for large lists if you are constantly searching.\n*   **When to use:** **AVOID using lists for general-purpose lookups by value if you need speed**. Use lists when you need to preserve order and access elements by index, or if you are dealing with a small list, where O(n) lookups are not significant.\n*   **Example:**\n   ```python\n    my_list = [10, 20, 30, 40]\n    print(my_list[2])  # Fast, O(1), access by index\n    if 30 in my_list:  # Slow, O(n), search by value (avoid this for general lookup)\n        print(\"Found\")\n   ```\n*   **Key Requirements:** Any Python object can be placed in a list.\n\n**4. Tuples (`tuple`)**\n\n*   **How it works:** Similar to lists, tuples store elements in order. They are immutable, meaning they can't be changed after creation.\n*   **Efficiency:**\n    *   **Lookup by Index (e.g., `my_tuple[0]`)**: O(1) - Constant time.\n    *   **Lookup by Value (e.g., `if item in my_tuple`):** O(n) - Linear time.\n*   **When to use:** Avoid using tuples for lookups by value for the same reasons you avoid using lists. Use them when you need a read-only sequence of items or when you need a hashable collection.\n*   **Key Requirements:** Any Python object can be placed in a tuple.\n\n**5.  `collections.Counter`**\n\n*   **How it works:**  It's a subclass of `dict` specifically designed for counting items, so keys are elements and values are counts.\n*  **Efficiency:**\n    *  **Lookup by Key:** O(1) on average.\n    *  **Insertion, Update:** O(1) on average.\n*  **When to use:** Perfect when you need to store frequencies of items, where lookup is based on the element itself.\n*  **Example:**\n\n   ```python\n    from collections import Counter\n    words = [\"apple\", \"banana\", \"apple\", \"orange\", \"banana\"]\n    word_counts = Counter(words)\n    print(word_counts[\"apple\"]) # Output: 2\n   ```\n*   **Key Requirements:** Keys must be hashable.\n\n**6. Specialized Lookups (Less Common)**\n\n*   **Sorted Lists with `bisect`:** If your list is sorted, the `bisect` module in the standard library can do binary search, which gives O(log n) lookup time, much faster than O(n).\n    ```python\n     import bisect\n     sorted_list = [1, 3, 5, 7, 9]\n     index = bisect.bisect_left(sorted_list, 5) # returns 2 (index where 5 is found)\n    ```\n*   **Databases (e.g., SQLite, PostgreSQL):** For very large datasets or persistence between program runs, using a database is often better than storing data in Python directly, since databases are optimized for searching, indexing, and managing large amounts of data.\n\n**Summary Table**\n\n| Data Structure | Lookup by Key (Avg Case) | Lookup by Value (Avg Case) |  Key Requirements  | Use Cases                                      |\n|-----------------|-------------------------|-----------------------------|-------------------|-------------------------------------------------|\n| `dict`        | O(1)                      | N/A (key lookup only)     | Hashable          | General lookups by key, key-value associations |\n| `set`         | O(1)                      | N/A (membership check)     | Hashable          | Membership checks, eliminating duplicates       |\n| `list`        | O(1) (by index)            | O(n)                       | Any object        | Ordered sequences, access by index (avoid value lookups)     |\n| `tuple`       | O(1) (by index)           | O(n)                       | Any object        | Read-only sequences, similar to list      |\n|`collections.Counter`| O(1) | N/A (key lookup only)| Hashable |  Counting element frequencies |\n\n**Key Takeaways**\n\n*   **For most lookup situations, `dict` (dictionaries) are the fastest and should be your default choice.**\n*   Use `set` (sets) when you need to check for the existence of a value and also ensure uniqueness.\n*   Avoid using `list` (lists) for lookups by value (unless the list is very small or you only need lookups by index), they are slow.\n*  If you need to count frequency of items, use `collections.Counter`.\n*  If you have a sorted list, the `bisect` module is an option, providing O(log n) lookup speed.\n* For large datasets that need storage on disk, leverage a database.\n\nRemember to profile your code when necessary to be sure about bottlenecks.  Use tools like the `timeit` module to compare the speed of different data structures if you're unsure which is optimal for your specific situation.\n",
      ],
    },
  ]
)

def gemini_prompt():
    response = chat_session.send_message("What about c#")
    print(response.text)

if __name__ == "__main__":
    try:
        gemini_prompt()
    except Exception as e:
        print(e)