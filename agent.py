import datetime
import os
import re
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

topics = [
    "The Future of Renewable Energy",
    "How to Optimize Python Code for Speed",
    "Top 5 Trends in AI Agents",
    "Beginner Guide to Serverless Computing",
]

# Pick a topic based on the day of the year
day_index = datetime.datetime.now().timetuple().tm_yday % len(topics)
topic = topics[day_index]

completion = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "system",
            "content": (
                "You are an expert tech blogger. Write an engaging blog post in"
                " clean Markdown format with a title, intro, subheadings, and"
                " conclusion."
            ),
        },
        {"role": "user", "content": f"Write a blog post about: {topic}"},
    ],
    temperature=0.7,
)

blog_content = completion.choices[0].message.content

# Create a clean URL-friendly filename
slug = re.sub(r"[^a-z0-9]+", "-", topic.lower()).strip("-")
filename = f"posts/{datetime.date.today()}-{slug}.md"

os.makedirs("posts", exist_ok=True)
with open(filename, "w", encoding="utf-8") as f:
  f.write(blog_content)

# Update README.md so visitors see a list of your latest posts
posts = sorted(os.listdir("posts"), reverse=True)
with open("README.md", "w", encoding="utf-8") as f:
  f.write("# My Automated AI Blog\n\n### Latest Posts\n")
  for post in posts:
    if post.endswith(".md"):
      f.write(f"- [{post[:-3]}](posts/{post})\n")
