---
layout: default
title: TechPulse AI - Newsroom
---

<div class="news-portal" style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;">
  
  <!-- HERO / FEATURED TOP STORY -->
  {% assign hero = site.posts.first %}
  {% if hero %}
  <div class="hero-post" style="border-bottom: 3px solid #cc0000; padding-bottom: 2rem; margin-bottom: 2.5rem;">
    <span style="background: #cc0000; color: white; padding: 3px 10px; font-size: 0.75rem; font-weight: bold; text-transform: uppercase; letter-spacing: 0.5px; border-radius: 2px;">Featured Story</span>
    <h1 style="font-size: 2.2rem; margin: 0.8rem 0; line-height: 1.2;">
      <a href="{{ hero.url | relative_url }}" style="text-decoration: none; color: #111;">{{ hero.title }}</a>
    </h1>
    <p style="color: #666; font-size: 0.85rem; margin-bottom: 1rem;">📅 {{ hero.date | date: "%B %d, %Y" }}</p>
    <p style="color: #333; font-size: 1.05rem; line-height: 1.6;">{{ hero.content | strip_html | truncatewords: 45 }}</p>
    <a href="{{ hero.url | relative_url }}" style="font-weight: bold; color: #cc0000; text-decoration: none; display: inline-block; margin-top: 0.5rem;">Read Full Story &rarr;</a>
  </div>
  {% endif %}

  <!-- NEWS GRID SECTION FOR RECENT ARTICLES -->
  {% if site.posts.size > 1 %}
  <h3 style="border-left: 4px solid #cc0000; padding-left: 10px; margin-bottom: 1.5rem; text-transform: uppercase; font-size: 1.1rem; letter-spacing: 0.5px; color: #111;">Latest Headlines</h3>
  
  <div class="news-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.5rem; margin-bottom: 3rem;">
    {% assign grid_posts = site.posts | slice: 1, 4 %}
    {% for post in grid_posts %}
      <div class="grid-card" style="border: 1px solid #e1e4e8; padding: 1.2rem; border-radius: 6px; background: #fff; display: flex; flex-direction: column; justify-content: space-between; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
        <div>
          <span style="color: #cc0000; font-size: 0.7rem; font-weight: bold; text-transform: uppercase;">News</span>
          <h4 style="margin: 0.5rem 0; font-size: 1.1rem; line-height: 1.3;">
            <a href="{{ post.url | relative_url }}" style="text-decoration: none; color: #111;">{{ post.title }}</a>
          </h4>
          <p style="color: #666; font-size: 0.8rem; margin-bottom: 0.8rem;">{{ post.date | date: "%b %d, %Y" }}</p>
          <p style="color: #444; font-size: 0.9rem; line-height: 1.4;">{{ post.content | strip_html | truncatewords: 20 }}</p>
        </div>
        <a href="{{ post.url | relative_url }}" style="font-size: 0.85rem; font-weight: bold; color: #cc0000; text-decoration: none; margin-top: 1rem;">Read More &rarr;</a>
      </div>
    {% endfor %}
  </div>
  {% endif %}

  <!-- MORE HEADLINES / ARCHIVE TICKER -->
  {% if site.posts.size > 5 %}
  <div class="more-news" style="background: #f8f9fa; padding: 1.5rem; border-radius: 6px; border-top: 3px solid #333; margin-top: 2rem;">
    <h3 style="margin-bottom: 1rem; font-size: 1.1rem; text-transform: uppercase; letter-spacing: 0.5px; color: #333;">More Articles & Archive</h3>
    <ul style="list-style: none; padding: 0; margin: 0;">
      {% assign archive_posts = site.posts | slice: 5, site.posts.size %}
      {% for post in archive_posts %}
        <li style="padding: 0.75rem 0; border-bottom: 1px solid #e1e4e8; display: flex; justify-content: space-between; align-items: center;">
          <a href="{{ post.url | relative_url }}" style="text-decoration: none; color: #111; font-weight: 500; font-size: 0.95rem;">{{ post.title }}</a>
          <span style="color: #777; font-size: 0.8rem; white-space: nowrap; margin-left: 1rem;">{{ post.date | date: "%b %d" }}</span>
        </li>
      {% endfor %}
    </ul>
  </div>
  {% endif %}

</div>
