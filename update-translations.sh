#!/bin/bash

# Add new language Example
# pybabel init -i messages.pot -d app/translations -l <language-tag>

pybabel extract -F babel.cfg -o messages.pot .

head -n 5 messages.pot > messages.pot_
tail -n +7 messages.pot >> messages.pot_
mv messages.pot_ messages.pot

pybabel update -i messages.pot -d app/translations
pybabel compile -d app/translations
