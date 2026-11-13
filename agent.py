import datetime
import os
import urllib.parse
import re
from groq import Groq

api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
  print("ERROR: GROQ_API_KEY secret is missing!")
  exit(1)

try:
  print("Initializing Groq client...")
  client = Groq(api_key=api_key)

  topics = [
      "The Future of Renewable Energy",
      "How to Optimize Python Code for Speed",
      "Top 5 Trends in AI Agents",
      "Beginner Guide to Serverless Computing",
  ]

  # Pick a topic based on the day of the year
  day_index = datetime.datetime.now().timetuple().tm_yday % len(topics)
  topic = topics[day_index]
  print(f"Selected topic: {topic}")

  print("Requesting AI-generated blog post from Groq...")
  completion = client.chat.completions.create(
      model="openai/gpt-oss-20b",
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

  # Generate a free header image URL based on the topic
  encoded_topic = urllib.parse.quote(topic)
  image_url = f"https://image.pollinations.ai/prompt/{encoded_topic}"
  header_image_markdown = f"![Header Image]({image_url})\n\n"

  # Prepend the image to the top of the blog content
  full_content = header_image_markdown + blog_content
  print("Header image added successfully!")

  # Create a clean URL-friendly filename
  slug = re.sub(r"[^a-z0-9]+", "-", topic.lower()).strip("-")
  filename = f"posts/{datetime.date.today()}-{slug}.md"

  os.makedirs("posts", exist_ok=True)
  with open(filename, "w", encoding="utf-8") as f:
    f.write(full_content)
  print(f"Saved post to {filename}")

  # Update README.md so visitors see a list of your latest posts
  posts = sorted(os.listdir("posts"), reverse=True)
  with open("README.md", "w", encoding="utf-8") as f:
    f.write("# My Automated AI Blog\n\n### Latest Posts\n")
    for post in posts:
      if post.endswith(".md"):
        f.write(f"- [{post[:-3]}](posts/{post})\n")
  print("Updated README.md successfully!")

except Exception as e:
  print(f"CRITICAL ERROR: {e}")
  raise e
