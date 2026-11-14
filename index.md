---
layout: default
title: Home
---

# 🤖 Latest AI Articles

<div class="posts-list" style="margin-top: 2rem;">
  <!-- Show up to 5 recent posts with full details -->
  {% assign recent_posts = site.posts | slice: 0, 5 %}
  {% for post in recent_posts %}
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

<!-- Previous Articles Archive Section -->
{% if site.posts.size > 5 %}
  <div class="previous-articles" style="margin-top: 3rem; padding-top: 2rem; border-top: 2px solid #eaecef;">
    <h3 style="margin-bottom: 1rem; color: #24292e;">📁 Previous Articles</h3>
    <ul style="list-style-type: none; padding-left: 0;">
      {% assign older_posts = site.posts | slice: 5, site.posts.size %}
      {% for post in older_posts %}
        <li style="margin-bottom: 0.8rem; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px dashed #e1e4e8; padding-bottom: 0.5rem;">
          <a href="{{ post.url | relative_url }}" style="text-decoration: none; color: #0366d6; font-weight: 500;">{{ post.title }}</a>
          <span style="color: #586069; font-size: 0.85rem;">{{ post.date | date: "%b %d, %Y" }}</span>
        </li>
      {% endfor %}
    </ul>
  </div>
{% endif %}
