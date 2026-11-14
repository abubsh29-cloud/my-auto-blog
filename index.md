---
layout: default
title: Home
---

# 🤖 Latest AI Articles

<div class="posts-list" style="margin-top: 2rem;">
  {% for post in site.posts %}
    <article style="margin-bottom: 2.5rem; padding-bottom: 1.5rem; border-bottom: 1px solid #e1e4e8;">
      <h2 style="margin-bottom: 0.3rem;">
        <a href="{{ post.url | relative_url }}" style="text-decoration: none; color: #0366d6;">{{ post.title }}</a>
      </h2>
      <p style="color: #586069; font-size: 0.85rem; margin-bottom: 0.8rem;">📅 {{ post.date | date: "%B %d, %Y" }}</p>
      <p style="color: #24292e; line-height: 1.6;">{{ post.excerpt }}</p>
      <a href="{{ post.url | relative_url }}" style="font-weight: 600; text-decoration: none; color: #0366d6;">Read Full Article &rarr;</a>
    </article>
  {% endfor %}
</div>
