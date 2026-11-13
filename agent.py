import datetime
import os
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from groq import Groq

api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
  print("ERROR: GROQ_API_KEY secret is missing!")
  exit(1)

try:
  print("Fetching latest tech headline from Hacker News RSS...")
  rss_url = "https://news.ycombinator.com/rss"
  req = urllib.request.Request(rss_url, headers={"User-Agent": "Mozilla/5.0"})

  topic = "The Future of Artificial Intelligence"  # Default fallback headline
  try:
    with urllib.request.urlopen(req) as response:
      xml_data = response.read()
    root = ET.fromstring(xml_data)
    titles = [
        item.find("title").text
        for item in root.findall(".//item")
        if item.find("title") is not None and item.find("title").text
    ]
    if titles:
      # Pick a headline based on the day of the year
      day_index = datetime.datetime.now().timetuple().tm_yday % len(titles)
      topic = titles[day_index]
  except Exception as rss_err:
    print(f"Could not fetch RSS feed, using default topic. Error: {rss_err}")

  print(f"Selected live topic: {topic}")

  print("Initializing Groq client...")
  client = Groq(api_key=api_key)

  print("Requesting AI-generated blog post from Groq...")
  completion = client.chat.completions.create(
      model="openai/gpt-oss-20b",
      messages=[
          {
              "role": "system",
              "content": (
                  "You are an expert tech blogger. Write an engaging blog post in"
                  " clean Markdown format with a title, intro, subheadings, and"
                  " conclusion based on the provided headline."
              ),
          },
          {
              "role": "user",
              "content": (
                  f"Write a detailed blog post about this trending topic:"
                  f" {topic}"
              ),
          },
      ],
      temperature=0.7,
  )

  blog_content = completion.choices[0].message.content

  # Generate a free header image URL based on the live headline
  encoded_topic = urllib.parse.quote(topic)
  image_url = f"https://image.pollinations.ai/prompt/{encoded_topic}"
  header_image_markdown = f"![Header Image]({image_url})\n\n"

  full_content = header_image_markdown + blog_content
  print("Header image and content combined successfully!")

  # Create a clean URL-friendly filename (capped at 50 chars for safety)
  slug = re.sub(r"[^a-z0-9]+", "-", topic.lower()).strip("-")[:50]
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
