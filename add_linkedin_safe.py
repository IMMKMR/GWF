# Safe python script to add linkedin to all cards
import os

filepath = r'd:\WORK\GWF\team_page\index.html'

with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

social_block = [
    '                        <div class="social-links">\n',
    '                            <a href="#" class="social-icon" target="_blank" rel="noopener noreferrer"\n',
    '                                aria-label="LinkedIn">\n',
    '                                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512">\n',
    '                                    <path\n',
    '                                        d="M100.28 448H7.4V148.9h92.88zM53.79 108.1C24.09 108.1 0 83.5 0 53.8a53.79 53.79 0 0 1 107.58 0c0 29.7-24.1 54.3-53.79 54.3zM447.9 448h-92.68V302.4c0-34.7-.7-79.2-48.29-79.2-48.29 0-55.69 37.7-55.69 76.7V448h-92.78V148.9h89.08v40.8h1.3c12.4-23.5 42.69-48.3 87.88-48.3 94 0 111.28 61.9 111.28 142.3V448z" />\n',
    '                                </svg>\n',
    '                            </a>\n',
    '                        </div>\n'
]

out_lines = []
in_card = False
card_lines = []
card_has_social = False
div_depth = 0
is_team_card = False

for line in lines:
    if not in_card:
        if 'class="service-card"' in line or 'class="team-card"' in line:
            in_card = True
            card_lines = [line]
            card_has_social = False
            div_depth = line.count('<div') - line.count('</div')
            is_team_card = 'class="team-card"' in line
        else:
            out_lines.append(line)
    else:
        card_lines.append(line)
        div_depth += line.count('<div') - line.count('</div')
        if 'class="social-links"' in line:
            card_has_social = True
        
        if div_depth == 0:
            if not card_has_social:
                if is_team_card:
                    # team-card structure ends directly with </div>
                    # Insert before the last line (which is </div>)
                    idx = len(card_lines) - 1
                    # Double check it is actually a closing div
                    while idx >= 0 and '</div>' not in card_lines[idx]:
                        idx -= 1
                    for block_line in reversed(social_block):
                        card_lines.insert(idx, block_line)
                else:
                    # service-card has an inner <div class="service-info"> ... </div>
                    # Insert before the second to last </div>
                    found_divs = 0
                    insert_idx = len(card_lines) - 1
                    for i in range(len(card_lines)-1, -1, -1):
                        if '</div>' in card_lines[i]:
                            found_divs += 1
                            if found_divs == 2:
                                insert_idx = i
                                break
                    for block_line in reversed(social_block):
                        card_lines.insert(insert_idx, block_line)
                        
            out_lines.extend(card_lines)
            in_card = False
            card_lines = []

with open(filepath, 'w', encoding='utf-8') as f:
    for line in out_lines:
        f.write(line)

print("Done")
