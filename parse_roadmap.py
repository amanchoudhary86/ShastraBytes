import json

file_path = '/run/media/pranav/New Volume/projects/ShastraBytes/roadmap_repo/src/data/roadmaps/machine-learning/machine-learning.json'

with open(file_path, 'r') as f:
    data = json.load(f)

topics = []
subtopics = []

for node in data['nodes']:
    label = node['data'].get('label', 'No Label').strip()
    if node['type'] == 'topic':
        topics.append(label)
    elif node['type'] == 'subtopic':
        subtopics.append(label)

print("--- Machine Learning Roadmap ---")
print("\nTopics:")
for topic in topics:
    print(f"- {topic}")

print("\nSubtopics:")
for subtopic in subtopics:
    print(f"- {subtopic}")
