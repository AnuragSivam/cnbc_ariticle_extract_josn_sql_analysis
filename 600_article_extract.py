import random

file_path = "cnbc_links.txt"

with open(file_path, "r") as f:
    urls = [line.strip() for line in f.readlines() if line.strip()]

print("Total URLs:", len(urls))

sections = {
    "world": [],
    "business": [],
    "markets": [],
    "technology": [],
    "politics": [],
    "economy": []
}

# Categorize by URL text
for url in urls:
    lower = url.lower()

    for sec in sections:
        if sec in lower:
            sections[sec].append(url)

sample_size = 100
final_urls = []

for sec in sections:
    links = list(set(sections[sec]))   # remove duplicates

    if len(links) > sample_size:
        selected = random.sample(links, sample_size)
    else:
        selected = links

    final_urls.extend(selected)

    print(sec.upper(), "→", len(selected))

random.shuffle(final_urls)

# Save txt
with open("cnbc_balanced_links1.txt", "w") as f:
    for link in final_urls:
        f.write(link + "\n")

print("Final:", len(final_urls))