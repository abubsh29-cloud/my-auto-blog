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
  print("Fetching trending tech headlines from RSS feed...")
  # Pulling live headlines from Hacker News RSS feed
  rss_url = "https://news.ycombinator.com/rss"
  req = urllib.request.Request(rss_url, headers={"User-Agent": "Mozilla/5.0"})

  topics = []
  try:
    with urllib.request.urlopen(req) as response:
      xml_data = response.read()
      root = ET.fromstring(xml_data)
      for item in root.findall(".//item"):
        title = item.find("title")
        if title is not None and title.text:
          topics.append(title.text)
  except Exception as e:
    print(f"Warning: Could not fetch RSS feed ({e}), using fallback topics.")

  # Fallback topics if RSS fetch fails
  if not topics:
    topics = [
        "The Future of Renewable Energy",
        "How to Optimize Python Code for Speed",
        "Top 5 Trends in AI Agents",
        "Beginner Guide to Serverless Computing",
    ]

  # Pick a topic based on the day of the year
  day_index = datetime.datetime.now().timetuple().tm_yday % len(topics)
  topic = topics[day_index]
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
                  " conclusion based on the given topic."
              ),
          },
          {
              "role": "user",
              "content": (
                  f"Write an in-depth, professional blog post inspired by this"
                  f" headline/topic: {topic}"
              ),
          },
      ],
      temperature=0.7,
  )

  blog_content = completion.choices[0].message.content

  # Generate a free header image URL based on the topic
  encoded_topic = urllib.parse.quote(topic)
  image_url = f"https://image.pollinations.ai/prompt/{encoded_topic}"
  header_image_markdown = f"![Header Image]({image_url})\n\n"

  full_content = header_image_markdown + blog_content
  print("Header image added successfully!")

  # Create a clean URL-friendly filename (trimmed to avoid long filenames)
  slug = re.sub(r"[^a-z0-9]+", "-", topic.lower()).strip("-")[:50]
  filename = f"posts/{datetime.date.today()}-{slug}.md"

  os.makedirs("posts", exist_ok=True)
  with open(filename, "w", encoding="utf-8") as f:
    f.write(full_content)
  print(f"Saved post to {filename}")

  # Update README.md so visitors see a list of your latest posts
  posts = sorted(os.listdir("posts"), reverse=True)
  with open("README.md", "w",
