import os

# Create a project folder for project
def create_project_dir(directory):
  if not os.path.exists(directory):
    os.makedirs(directory)
  else:
    return (os.path.getmtime(directory))
#    print(os.path.getmtime(directory))
    # When was file last updated
#    print(directory, 'already exists')
    pass

# Save parsed data to file
def save_project(file_location, row_data):
  if not os.path.isfile(file_location):
    row_data.to_csv(file_location)
  else:
    pass

# Create a new file
def write_file(path, data):
  with open(path, 'wb') as f:
    f.write(data)

# Add data onto an existing file
def append_to_file(path, data):
  with open(path, 'a') as file:
    file.write(data + '\n')

# Each line of xpath # Removes whitespaces and \n
def clean_line(array_lines):
  article_story = []
  for line in array_lines:
    clean_line = (line).replace('\n', '').replace('  ', '')
    article_story.append(clean_line)
    # Each broken down paragraph can be sent to the word analyzer
  print(article_story)
#  article_story.clear()
