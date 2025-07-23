import os, shutil, sys
from functions import extract_title, markdown_to_html_node

def main():
    basepath = "./"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    copy_content("static", "docs")
    generate_pages_recursive("content", "template.html", basepath)

def copy_content(source, destination):
    if not os.path.exists(destination):
        os.makedirs(destination)
    else:
        shutil.rmtree(destination)
        os.makedirs(destination)

    for item in os.listdir(source):
        print(f"Copying {item} from {source} to {destination}")
        if os.path.isdir(os.path.join(source, item)):
            copy_content(os.path.join(source, item), os.path.join(destination, item))
        else:
            shutil.copy(os.path.join(source, item), os.path.join(destination, item))

def generate_page(from_path, template_path, dest_path):
    #print(f"Generating page from {from_path} to {dest_path} using template {template_path}")
    markdown = None
    with open(from_path, 'r') as f:
        markdown = f.read()
    htmlNode = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    template = None
    with open(template_path, 'r') as f:
        template = f.read()

    html = template.replace("{{ Content }}", htmlNode)
    html = html.replace("{{ Title }}", title)
    # html = html.replace("href=\"/", "href=\"" + dest_path)
    # html = html.replace("src=\"/", "src=\"" + dest_path)
    
    if not os.path.exists(dest_path):
        if os.path.isdir(dest_path):
            os.makedirs(dest_path)
        else:
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, 'w') as f:
        f.write(html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    # working_directory = os.getcwd()
    # content_dir = os.path.join(working_directory, dir_path_content)
    # dest_dir = os.path.join(working_directory, dest_dir_path)
    # fullpath = os.path.join(working_directory, dir_path_content)
    for item in os.listdir(dir_path_content):
        item_path = os.path.join(dir_path_content, item)
        if os.path.isdir(item_path):
            dest_path = os.path.join(dest_dir_path, item)
            generate_pages_recursive(item_path, template_path, dest_path)
        else:
            dest_path = os.path.join(dest_dir_path, item.replace('.md', '.html'))
            print(f"Generating page for {item_path} to {dest_path}")
            generate_page(item_path, template_path, dest_path)
        
main()
