import re

# Read the content from the text file
with open('Political Catechism.txt', 'r', encoding='utf-8') as f:
    txt_content = f.read()

# Read the HTML template
with open('indexDraft.html', 'r', encoding='utf-8') as f:
    html_template = f.read()

# Parse the Q&A from txt_content
# Split into sections starting with Q.
sections = re.split(r'(Q\. \d+\. .+?)(?=\nA\.|\Z)', txt_content, flags=re.DOTALL)

# Process each Q&A pair
processed_content = ''
i = 0
while i < len(sections):
    if sections[i].strip().startswith('Q.'):
        question = sections[i].strip()
        if i + 1 < len(sections):
            answer_section = sections[i + 1].strip()
        else:
            answer_section = ''
        
        # Split answer into body and references
        if '\n[' in answer_section:
            split_result = re.split(r'\n(?=\[)', answer_section, maxsplit=1)
            if len(split_result) == 2:
                answer_body = split_result[0].strip()
                references = split_result[1].strip()
            else:
                answer_body = answer_section
                references = ''
        else:
            answer_body = answer_section
            references = ''
        
        # Process citations in answer_body: convert [1] to superscript ¹
        answer_body = re.sub(r'\[(\d+)\]', r'<sup>\1</sup>', answer_body)
        
        # Format references: each [1] ... on new line with <br>, size 1.05em
        if references:
            ref_lines = re.findall(r'\[\d+\] .*?(?=\[\d+\]|\Z)', references, re.DOTALL)
            formatted_refs = '<div class="proofTexts">' + '<br>'.join(ref.strip() for ref in ref_lines if ref.strip()) + '</div>'
        else:
            formatted_refs = ''
        
        # Style Q as h3 with heavy weight
        processed_content += f'<h3>{question}</h3>\n'
        
        # Style A. prefix heavy, rest light, same size
        if answer_body.startswith('A. '):
            a_prefix = 'A. '
            a_body = answer_body[3:]
        else:
            a_prefix = ''
            a_body = answer_body
        
        processed_content += f'<h3 style="display: inline;">{a_prefix}</h3><span class="answer">{a_body}</span><br><br>\n'
        
        # Add references
        processed_content += formatted_refs + '\n'
        
        i += 2
    else:
        i += 1

# Insert into the .content div
insert_point = html_template.find('<div class="content">') + len('<div class="content">')
html_output = html_template[:insert_point] + processed_content + html_template[insert_point:]

# Write to index.html
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_output)

print("index.html has been created.")