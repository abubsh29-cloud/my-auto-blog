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

  topic = "The Future of Artificial Intelligence"
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

  # Generate header image
  encoded_topic = urllib.parse.quote(topic)
  image_url = f"https://image.pollinations.ai/prompt/{encoded_topic}"
  header_image_markdown = f"![Header Image]({image_url})\n\n"

  # Create Jekyll Front Matter so the theme recognizes the post title and date
  today_str = datetime.date.today().isoformat()
  front_matter = (
      "---\nlayout: post\ntitle: \""
      + topic.replace('"', '\\"')
      + f'"\ndate: {today_str} 09:00:00 +0000\n---\n\n'
  )

  full_content = front_matter + header_image_markdown + blog_content
  print("Jekyll front matter and header image added successfully!")

  # Jekyll requires posts to be in the _posts folder with format YYYY-MM-DD-title.md
  slug = re.sub(r"[^a-z0-9]+", "-", topic.lower()).strip("-")[:50]
  filename = f"_posts/{today_str}-{slug}.md"

  os.makedirs("_posts", exist_ok=True)
  with open(filename, "w", encoding="utf-8") as f:
    f.write(full_content)
  print(f"Saved post to {filename}")

except Exception as e:
  print(f"CRITICAL ERROR: {e}")
  raise e
